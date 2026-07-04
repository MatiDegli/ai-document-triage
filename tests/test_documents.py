from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_example():
    return client.post("/documents", json={"title": "Example", "content": "Hello"})


def test_get_document_empty():
    response = client.get("/documents")

    assert response.status_code == 200
    assert response.json() == []


def test_list_documents_includes_created_document():
    create_response = create_example()

    assert create_response.status_code == 201

    created = create_response.json()

    list_response = client.get("/documents")

    assert list_response.status_code == 200

    documents: list[dict[str, object]] = list_response.json()

    assert isinstance(documents, list)
    assert len(documents) == 1
    assert documents[0]["id"] == created["id"]
    assert documents[0]["title"] == "Example"
    assert documents[0]["content"] == "Hello"


def test_get_document_id():
    create_response = create_example()

    assert create_response.status_code == 201

    created: dict[str, object] = create_response.json()

    response = client.get(f"/documents/{created['id']}")

    assert response.status_code == 200

    document: dict[str, object] = response.json()

    assert isinstance(document, dict)
    assert document["id"] == created["id"]


def test_get_document_non_existent():
    response = client.get("/documents/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Document not found"}
