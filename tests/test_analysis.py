from fastapi.testclient import TestClient

from app.domain import DocumentCategory
from app.main import app
from app.schemas.analysis import AnalysisRead

client = TestClient(app)


def create_example_document() -> dict[str, object]:
    response = client.post(
        "/documents",
        json={
            "title": "Python document",
            "content": "Python FastAPI application using PostgreSQL.",
        },
    )

    assert response.status_code == 201
    return response.json()


def test_analyze_document(mock_provider: None) -> None:

    document_json = create_example_document()
    document_id = document_json["id"]

    response = client.post(f"/documents/{document_id}/analyze")

    assert response.status_code == 201

    analysis = AnalysisRead.model_validate(response.json())

    assert analysis.document_id == document_id
    assert analysis.category is DocumentCategory.TECHNICAL
    assert analysis.confidence == 0.9
    assert analysis.provider == "mock"


def test_analyze_nonexistant_document(mock_provider: None) -> None:

    response = client.post("/documents/999/analyze")

    assert response.status_code == 404
    assert response.json() == {"detail": "Document not found"}


def test_get_analysis(mock_provider: None) -> None:

    document_json = create_example_document()
    document_id = document_json["id"]

    analysis_response = client.post(f"/documents/{document_id}/analyze")

    assert analysis_response.status_code == 201

    analysis = AnalysisRead.model_validate(analysis_response.json())
    analysis_id = analysis.id

    get_response = client.get(f"/analyses/{analysis_id}")

    assert get_response.status_code == 200

    retrieved = AnalysisRead.model_validate(get_response.json())

    assert retrieved.id == analysis.id
    assert retrieved.document_id == analysis.document_id


def test_get_document_analyses(mock_provider: None) -> None:

    document_json = create_example_document()
    document_id = document_json["id"]

    response1 = client.post(f"/documents/{document_id}/analyze")
    response2 = client.post(f"/documents/{document_id}/analyze")

    assert response1.status_code == 201
    assert response2.status_code == 201

    analysis1 = AnalysisRead.model_validate(response1.json())
    analysis2 = AnalysisRead.model_validate(response2.json())

    list_response = client.get(f"/documents/{document_id}/analyses")

    assert list_response.status_code == 200

    analysis_list = [AnalysisRead.model_validate(item) for item in list_response.json()]

    assert len(analysis_list) == 2
    assert {analysis.id for analysis in analysis_list} == {
        analysis1.id,
        analysis2.id,
    }
