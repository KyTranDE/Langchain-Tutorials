
from core_rag.llm import llm_openai
from core_rag.prompt import SYSTEM_GRADE_DOCUMENT, SYSTEM_MERGE_DOCUMENT, SYSTEM_GENARATE_ANSWER
from core_rag.vector_store import vector_store



from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

from pydantic import BaseModel, Field

#=================================RETRIEVAL=============================================


retriever = vector_store.as_retriever(
    search_kwargs={"k": 25}
)
model = HuggingFaceCrossEncoder(model_name="itdainb/PhoRanker")
compressor = CrossEncoderReranker(model=model, top_n=5)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

# ================================GRADE DOCUMENTS=============================================
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    id: str = Field(description="Document ID")
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )
    more_data: str = Field(
        description="More data (next or prev) for answer the user question, 'next', 'prev', or ''")



grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_GRADE_DOCUMENT),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader = grade_prompt | llm_openai.with_structured_output(GradeDocuments)


#==================================MERGE DOCUMENTS=============================================
class DocMergeRespone(BaseModel):
    document: str = Field(
        description="Document merge response"
    )
    
merge_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MERGE_DOCUMENT),
        ("human", "Documents: {documents}"),
    ]
)


merge_pipeline = merge_prompt | llm_openai.with_structured_output(DocMergeRespone)


class GeneratorResponse(BaseModel):
    answer: str = Field(
        description="Answer of the question"
    )
    

generator_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_GENARATE_ANSWER+"\n\nContext: {context} \n"),
        MessagesPlaceholder("history"),
        ("human",
            """Question: {question}"""),
    ]
)



generator_pipeline = generator_prompt | llm_openai


