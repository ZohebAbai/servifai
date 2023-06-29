from pathlib import Path
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    LLMPredictor,   
    ServiceContext,
    StorageContext,
    PromptHelper,
)
from llama_index.vector_stores import ChromaVectorStore
from llama_index.indices.keyword_table import SimpleKeywordTableIndex
from llama_index.indices.composability import ComposableGraph
from llama_index.indices.query.query_transform.base import DecomposeQueryTransform
from llama_index.query_engine.transform_query_engine import TransformQueryEngine
from llama_index.langchain_helpers.agents import LlamaToolkit, IndexToolConfig

from servifai.memory.chroma import ChromaDB
from servifai.llms.openai import OpenAILLM


class VectorKnowledgeBase:
    def __init__(self, vector_indices, index_summaries, service_context):
        self._indices = vector_indices
        self._summaries = index_summaries
        self._service_context = service_context

    def as_tool(self, title):
        index = self._indices [title]
        summary = self._summaries[title]
        query_engine = index.as_query_engine(service_context=self._service_context, similarity_top_k=3)
        return IndexToolConfig(query_engine=query_engine, name=f"Knowledge Vector Index {title}",
                            description=f"useful for when you want to answer queries about the {summary}",
                            tool_kwargs={"return_direct": True}
                            )


class KnowledgeGraphs:
    def __init__(self, vector_indices, index_summaries, service_context, llm_predictor):
        self._indices = vector_indices
        self._summaries = index_summaries
        self._service_context = service_context
        self._llm_pred = llm_predictor
        self._graph = None
        self._custom_query_engines = {}
        self._query_engine = self._create_graph_qe()

    def _create_graph_qe(self):
        self._graph = ComposableGraph.from_indices(
            SimpleKeywordTableIndex,
            [index for _, index in self._indices.items()],
            [summary for _, summary in self._summaries.items()],
            max_keywords_per_chunk=50
        )
        decompose_transform = DecomposeQueryTransform(self._llm_pred, verbose=True)

        for index in self._indices.values():
            query_engine = index.as_query_engine(service_context=self._service_context)
            transform_extra_info = {'index_summary': index.index_struct.summary}
            tranformed_query_engine = TransformQueryEngine(query_engine, decompose_transform,
                                                            transform_metadata=transform_extra_info)
            self._custom_query_engines[index.index_id] = tranformed_query_engine

        self._custom_query_engines[self._graph.root_index.index_id] = self._graph.root_index.as_query_engine(
                                    retriever_mode='simple',
                                    response_mode='tree_summarize',
                                    service_context=self._service_context,
                                    )
        return self._graph.as_query_engine(custom_query_engines=self._custom_query_engines)

    def as_tool(self, about):
        return IndexToolConfig(
                        query_engine=self._query_engine, 
                        name="Knowledge Graph Index",
                        description=f"useful for when you want to answer queries that require comparing, contrasting or analyzing over multiple sources or periods of {about}",
                        tool_kwargs={"return_direct": True}
        )   


class KnowledgeBase:
    def __init__(self, vdb_dir, data_dir, about, text, llm):
        self.vdb_dir = vdb_dir
        self.data_dir = data_dir
        self.about = about
        self.max_input_size = int(text['max_input_size'])
        self.num_outputs = int(text['num_outputs'])
        self.max_chunk_overlap = float(text['max_chunk_overlap'])
        self.chunk_size_limit = int(text['chunk_size_limit'])
        self.llm = llm
        self.oaillm = OpenAILLM(llm, text)  
        self.llm_predictor = LLMPredictor(llm=self.oaillm.model)
        self.vectorstore = self._initiate_vectorstore()
        self.service_context = self._initiate_contexts()[0]
        self.storage_context = self._initiate_contexts()[1]
        self.titles = []
        self.indices = self._create_indices()[0]
        self.index_summaries = self._create_indices()[1]
        self.qe_tools = self._get_query_engine_tools()
    
    def _initiate_vectorstore(self):
        vectordb = ChromaDB(self.vdb_dir, self.llm['org'])
        return ChromaVectorStore(chroma_collection=vectordb.collection)

    def _initiate_contexts(self):
        prompt_helper = PromptHelper(self.max_input_size, 
                                    self.num_outputs, 
                                    self.max_chunk_overlap, 
                                    chunk_size_limit=self.chunk_size_limit)
        self.service_context = ServiceContext.from_defaults(llm_predictor=self.llm_predictor, prompt_helper=prompt_helper)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vectorstore)
        return self.service_context, self.storage_context

    def _create_indices(self):
        """
        Loads the data, chunks it, create embedding for each chunk
        and then stores the embedding to a vector database.

        Args:
            data_dir (str): the directory containing the data
        """
        ext = '.pdf'
        docs = {}
        indices = {}
        index_summaries = {}

        for dbb in Path(self.data_dir).glob(f'*{ext}'):
            print(dbb)
            title = dbb.stem
            self.titles.append(title)
            docs[title] = SimpleDirectoryReader(input_files=[str(dbb)],
                                                    recursive=True,
                                                    exclude_hidden=True,
                                                    required_exts=[ext]).load_data()
            indices[title] = VectorStoreIndex.from_documents(docs[title],
                                                            service_context=self.service_context,
                                                            storage_context=self.storage_context
                                                            )
            index_summaries[title] = f"single source on {self.about} for particular {' '.join(title.split('-'))}"
        return indices, index_summaries


    def _get_query_engine_tools(self):
        vectorkb_tools = []
        for title in self.titles:
            vectorkb_configs = VectorKnowledgeBase(self.indices,
                                                self.index_summaries,
                                                self.service_context).as_tool(title)
            vectorkb_tools.append(vectorkb_configs)

        kg_tool = KnowledgeGraphs(self.indices,
                                self.index_summaries,
                                self.service_context,
                                self.llm_predictor).as_tool(self.about)
        return vectorkb_tools + [kg_tool]
        

    def as_tool(self):
        return LlamaToolkit(index_configs=self.qe_tools)