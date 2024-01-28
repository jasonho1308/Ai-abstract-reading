from typing import List
from openai import OpenAI
from dotenv import dotenv_values


class MyGPT:
    def __init__(self, instruction: str, prompt: str) -> None:
        config = dotenv_values(".env")

        self.client = OpenAI(api_key=config["OPENAI_API_KEY"])
        self.instruction = instruction
        self.prompt = prompt

    def get_result(self, abstract: List[dict], model: str):

        messages = [
            {"role": "system", "content": self.instruction},
            {"role": "user", "content": self.prompt + abstract},
        ]

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=model,
        )

        return chat_completion
