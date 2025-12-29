from typing import Dict
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

MODEL = "gpt-4.1-nano"
SYSTEM_PROMPT = (
    "You are a strict coding interviewer."
    "Given a LeetCode-style problem and a candidate's solution, "
    "return ONLY a JSON object that conforms exactly to the provided schema."
)
USER_PROMPT_TEMPLATE = """Leetcode Question:
{question}

Candidate Answer (verbatim):
{answer}

Grade the answer on these criteria (0-100, where 100 is the best):
- Logic: correctness, edge cases, and whether it actually solves the problem
- Efficiency: time/space complexity relative to the optimal approach
- Readability: clarity, code quality, code organization, naming, comments
"""
USER_PROMPT_TESTING = """Leetcode Question:
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Candidate Answer (verbatim):
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        m = {}
        for i in range(n):
            diff = target - nums[i]
            if diff in m:
                return [i, m[diff]]
            m[nums[i]] = i

Grade the answer on these criteria (0-100, where 100 is the best):
- Logic: correctness, edge cases, and whether it actually solves the problem
- Efficiency: time/space complexity relative to the optimal approach
- Readability: clarity, code quality, code organization, naming, comments
""" 


class SolutionFeedback(BaseModel):
    logic: int
    efficiency: int
    readability: int

def grade_solution(ques: str, ans: str) -> Dict[str, float]:
    user_prompt = USER_PROMPT_TEMPLATE.format(question = ques, answer = ans)
    
    response = client.responses.parse(
        model = MODEL,
        input = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        text_format = SolutionFeedback,
    )

    data = response.output_parsed
    if data is None:
        raise ValueError(f"Failed to parse response:\n{response.output_text}")
    return data.model_dump()

response = client.responses.parse(
        model = MODEL,
        input = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TESTING},
        ],
        text_format = SolutionFeedback,
)

data = response.output_parsed
if data is None:
    raise ValueError(f"Failed to parse response:\n{response.output_text}")

print(f"{data.logic}/10")
print(f"{data.efficiency}/10")
print(f"{data.readability}/10")
