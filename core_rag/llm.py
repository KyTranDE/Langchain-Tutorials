from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from config.setting import settings



# llm_groq = ChatGroq(model="llama-3.2-90b-text-preview", temperature=0,api_key=settings.GROQ_API_KEY)

llm_openai = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=settings.OPENAI_API_KEY)