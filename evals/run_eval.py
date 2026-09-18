"""Run document analysis evaluations."""

import json
from collections.abc import Iterator
from pathlib import Path
from time import perf_counter

from pydantic import BaseModel, ValidationError

from app.domain import DocumentCategory
from app.llm.mock_provider import MockLLMProvider
from app.llm.provider import LLMProvider
from app.models.document import Document
from app.schemas.analysis import ProviderResult


class EvalDocument(BaseModel):
    title: str
    content: str


class EvalCase(BaseModel):
    id: str
    document: EvalDocument
    expected_category: DocumentCategory


def load_cases(path: Path) -> Iterator[EvalCase]:
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                raw_case = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON in line {line_number}") from error

            try:
                yield EvalCase.model_validate(raw_case)
            except ValidationError as error:
                raise ValueError(
                    f"Invalid evaluation case in line {line_number}"
                ) from error


def run_case(case: EvalCase, provider: LLMProvider) -> bool:
    document = Document(
        title=case.document.title,
        content=case.document.content,
    )

    started_at = perf_counter()

    try:
        provider_result: ProviderResult = provider.analyze(document)
        output = provider_result.output
        input_tokens = provider_result.input_tokens
        output_tokens = provider_result.output_tokens
    # Keep the evaluation run alive and record unexpected provider failures.
    except Exception as error:  # noqa: BLE001
        print(f"{case.id} FAIL [provider_error]: {error}")
        return False

    latency_ms = (perf_counter() - started_at) * 1000

    if output.category != case.expected_category:
        print(
            f"{case.id} FAIL [classification_error] "
            f"expected={case.expected_category.value} "
            f"actual={output.category.value} "
            f"input_tokens={input_tokens} "
            f"output_tokens={output_tokens}"
        )
        return False

    print(
        f"{case.id} PASS ({latency_ms:.2f} ms, "
        f"input_tokens={input_tokens}, output_tokens={output_tokens})"
    )
    return True


def main() -> None:
    cases_path = Path(__file__).with_name("cases.jsonl")
    provider: LLMProvider = MockLLMProvider()

    total_cases = 0
    passed_cases = 0

    print(f"Provider: {provider.name}")
    print(f"Model: {provider.model}")
    print()

    for case in load_cases(cases_path):
        total_cases += 1

        if run_case(case, provider):
            passed_cases += 1

    success_rate = passed_cases / total_cases * 100

    print()
    print(f"{passed_cases} / {total_cases} passed")
    print(f"Success rate: {success_rate:.1f}%")


if __name__ == "__main__":
    main()
