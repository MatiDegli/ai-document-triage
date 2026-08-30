import dotenv

from app.models.document import Document
from app.schemas.analysis import AnalysisOutput
from openai import OpenAI


def analyze(document: Document) -> AnalysisOutput:
    return ...