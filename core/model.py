from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools
from core.config import settings

def get_model():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0
    )
    return model.bind_tools(tools)
