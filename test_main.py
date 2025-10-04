import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client



@patch("main.insert_file")  
def test_upload_spec(mock_insert_file, client):

    mock_insert_file.return_value = None


    file_content = b'{"openapi": "3.0.0", "info": {"title": "Test API", "version": "1.0"}, "paths": {}}'
    response = client.post(
        "/upload/spec",
        data={
            "application_name": "test_app",
        },
        files={"file": ("openapi.json", file_content, "application/json")},
    )


    assert response.status_code == 200
    assert response.json() == {"message": "File Uploaded succssfully", "application": "test_app"}



@patch("main.get_latest_file")
def test_get_latest_spec(mock_get_latest_file, client):

    mock_get_latest_file.return_value = {
        "application_name": "test_app",
        "version": 1,
        "filename": "openapi.json",
        "content_type": "json",
        "file_data": b'{"openapi": "3.0.0", "info": {"title": "Test API", "version": "1.0"}}'
    }

    response = client.get("/get/latest-spec?application_name=test_app")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Latest file retrieved successfully",
        "application_name": "test_app",
        "version_id": 1,
        "file_data": '{"openapi": "3.0.0", "info": {"title": "Test API", "version": "1.0"}}',
        "filename": "openapi.json",
        "content_type": "json"
    }



@patch("main.get_spec_by_version_and_application")
def test_get_spec_by_version(mock_get_spec_by_version_and_application, client):

    mock_get_spec_by_version_and_application.return_value = {
        "application_name": "test_app",
        "version": 1,
        "filename": "openapi.json",
        "content_type": "json",
        "file_data": b'{"openapi": "3.0.0", "info": {"title": "Test API", "version": "1.0"}}'
    }

    response = client.get("/get/spec?application_name=test_app&version=1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "File retrieved successfully",
        "application_name": "test_app",
        "version_id": 1,
        "filename": "openapi.json",
        "file_data": '{"openapi": "3.0.0", "info": {"title": "Test API", "version": "1.0"}}',
        "content_type": "json"
    }



@patch("main.insert_file")
def test_upload_spec_invalid_json(mock_insert_file, client):
    mock_insert_file.return_value = None


    file_content = b'{"openapi": "3.0.0", "info": {"title": "Test API", "version": "1.0"'
    response = client.post(
        "/upload/spec",
        data={"application_name": "test_app"},
        files={"file": ("openapi.json", file_content, "application/json")},
    )

    assert response.status_code == 400
    assert response.json() == {"message": "Error occurred: Invalid OpenAPI Spec"}



@patch("main.get_latest_file")
def test_get_latest_spec_not_found(mock_get_latest_file, client):
    mock_get_latest_file.return_value = None

    response = client.get("/get/latest-spec?application_name=test_app")

    assert response.status_code == 404
    assert response.json() == {"message": "No files found for the application."}
