from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from grader import grade_solution

app = FastAPI()

origins = [
        "http://localhost:5173", 
]

app.add_middleware(
        CORSMiddleware,
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"]
)

class GradeRequest(BaseModel):
    question: str
    answer: str

@app.post("/api/grade")
def grade_code(req: GradeRequest):
    result = grade_solution(req.question, req.answer)
    return result
