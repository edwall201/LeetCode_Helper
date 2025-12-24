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

Grade the answer on these criteria (0-10, where 10 is the best):
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

Grade the answer on these criteria (0-10, where 10 is the best):
- Logic: correctness, edge cases, and whether it actually solves the problem
- Efficiency: time/space complexity relative to the optimal approach
- Readability: clarity, code quality, code organization, naming, comments
""" 


class SolutionFeedback(BaseModel):
    logic: int
    efficiency: int
    readability: int

response = client.responses.parse(
        model = MODEL,
        input = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TESTING},
        ],
        text_format = SolutionFeedback,
)
