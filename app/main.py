from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, List
import base64

# Import your QA logic from qa_engine.py
from app.qa_engine import get_answer

app = FastAPI()

# Root GET route for testing
@app.get("/")
def read_root():
    return {"message": "Virtual TA running!"}

# Define the structure of the incoming request
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 image (optional)

# Define the structure of the response
class AnswerLink(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[AnswerLink]

# Main POST route for answering questions
@app.post("/post/answer", response_model=AnswerResponse)
async def answer_question(req: QuestionRequest):
    question = req.question
    image_data = req.image

    # If image is present, decode it (you can pass it to OCR later if needed)
    if image_data:
        try:
            image_bytes = base64.b64decode(image_data)
            # TODO: Send image_bytes to OCR if needed
        except Exception as e:
            return {"answer": "Invalid image format.", "links": []}

    # Get answer from your QA engine
    try:
        answer_text, reference_links = get_answer(question)
    except Exception as e:
        return {
            "answer": f"An error occurred while processing your question: {str(e)}",
            "links": []
        }

    # Structure the response
    return {
        "answer": answer_text,
        "links": reference_links
    }
