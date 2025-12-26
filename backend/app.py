from fastapi import FastAPI
from pydantic import BaseModel
from grader import grade_solution

app = FastAPI()

class GradeRequest(BaseModel):
    question: str
    answer: str

@app.post("/api/grade")
def grade_code(req: GradeRequest):
    result = grade_solution(req.question, req.answer)
    return result
