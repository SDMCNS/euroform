"""Tests for EuroForm FastAPI endpoints."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from euroform.api.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_api_index_html(client: TestClient):
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "EuroForm" in response.text
    assert "Drop your Formex XML file here" in response.text


def test_api_index_json(client: TestClient):
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    data = response.json()
    assert data["name"] == "EuroForm API"
    assert "convert" in data["endpoints"]


def test_api_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "euroform"


def test_api_schema(client: TestClient):
    response = client.get("/schema")
    assert response.status_code == 200
    schema = response.json()
    assert schema["title"] == "Parsed Formex document"
    assert "format" in schema["properties"]


def test_api_convert_file_multipart(client: TestClient, basic_act_xml: str):
    response = client.post(
        "/convert",
        files={"file": ("act.fmx.xml", basic_act_xml.encode("utf-8"), "application/xml")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "formex"
    assert "Regulation (EU) 2024/123" in data["title"]
    assert data["metadata"]["language"] == "EN"


def test_api_convert_file_as_text(client: TestClient, basic_act_xml: str):
    response = client.post(
        "/convert?output_format=text",
        files={"file": ("act.fmx.xml", basic_act_xml.encode("utf-8"), "application/xml")},
    )
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "Regulation (EU) 2024/123" in response.text
    assert "Article 1" in response.text


def test_api_convert_raw_xml(client: TestClient, basic_act_xml: str):
    response = client.post(
        "/convert",
        content=basic_act_xml.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["root"] == "ACT"


def test_api_convert_json_payload(client: TestClient, basic_act_xml: str):
    response = client.post(
        "/convert",
        json={"xml": basic_act_xml, "keep_toc": False, "include_metadata": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["root"] == "ACT"


def test_api_dedicated_convert_endpoints(client: TestClient, basic_act_xml: str):
    # Dedicated /convert/file
    res_file = client.post(
        "/convert/file",
        files={"file": ("test.xml", basic_act_xml.encode("utf-8"), "application/xml")},
    )
    assert res_file.status_code == 200
    assert res_file.json()["root"] == "ACT"

    # Dedicated /convert/raw
    res_raw = client.post(
        "/convert/raw",
        content=basic_act_xml.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
    )
    assert res_raw.status_code == 200
    assert res_raw.json()["root"] == "ACT"

    # Dedicated /convert/json
    res_json = client.post(
        "/convert/json",
        json={"xml": basic_act_xml},
    )
    assert res_json.status_code == 200
    assert res_json.json()["root"] == "ACT"


def test_api_convert_batch(client: TestClient, basic_act_xml: str, table_act_xml: str):
    files = [
        ("files", ("doc1.xml", basic_act_xml.encode("utf-8"), "application/xml")),
        ("files", ("doc2.xml", table_act_xml.encode("utf-8"), "application/xml")),
    ]
    response = client.post("/convert/batch", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["successful"] == 2
    assert data["failed"] == 0
    assert len(data["results"]) == 2
    assert data["results"][0]["filename"] == "doc1.xml"
    assert data["results"][1]["filename"] == "doc2.xml"


def test_api_invalid_xml_error(client: TestClient, invalid_xml: str):
    response = client.post(
        "/convert",
        content=invalid_xml.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
    )
    assert response.status_code == 400
    err = response.json()
    assert "Invalid XML syntax" in err["detail"]
    assert err["error_type"] == "XMLParseError"


def test_api_empty_file_error(client: TestClient):
    response = client.post(
        "/convert",
        files={"file": ("empty.xml", b"", "application/xml")},
    )
    assert response.status_code == 400
    err = response.json()
    assert "empty" in err["detail"].lower()
