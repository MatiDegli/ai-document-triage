"""DeepSeek provider implementation."""

import os

from dotenv import load_dotenv
from openai import OpenAI

from app.llm.exceptions import ProviderError
from app.llm.provider import LLMProvider
from app.models.document import Document
from app.schemas.analysis import AnalysisOutput, ProviderResult


class DeepSeekLLMProvider(LLMProvider):
    name = "deepseek"
    model = "deepseek-v4-flash"
    prompt_version = "v1"
    schema_version = "v1"

    def __init__(self) -> None:
        load_dotenv()
        self.client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com",
        )

    def analyze(self, document: Document) -> ProviderResult:
        response = self.client.responses.parse(
            model=self.model,
            instructions="Analyze the document and return structured JSON.",
            input=document.content,
            text_format=AnalysisOutput,
            max_output_tokens=800,
        )

        output = response.output_parsed

        if output is None:
            raise ProviderError("Provider returned empty content")

        usage = response.usage

        return ProviderResult(
            output=output,
            input_tokens=usage.input_tokens if usage is not None else None,
            output_tokens=usage.output_tokens if usage is not None else None,
        )
