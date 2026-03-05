from fastapi import FastAPI
from pydantic import BaseModel
from graph.workflow import build_workflow

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    workflow = build_workflow()

    result = workflow.invoke({
        "messages": [
            {"role": "user", "content": req.message}
        ]
    })

    return {
        "response": result["messages"][-1].content
    }
