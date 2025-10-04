# Levo Spec-Store API

A FastAPI application to store and retrieve OpenAPI specifications.

## Prerequisites

- Python 3.7+
- pip

## Local Setup

1.  **Clone the repository (or download the files).**

2.  **Navigate to the project directory:**
    ```bash
    cd levo
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application:**
    The application will start a local server, typically on `http://127.0.0.1:8000`.
    ```bash
    uvicorn main:app --reload
    ```

## API Endpoints

The server provides the following endpoints to manage OpenAPI specifications.

### 1. Upload a Specification

Upload a new version of an OpenAPI specification for a given application. The specification can be in JSON or YAML format.

-   **URL:** `/upload/spec`
-   **Method:** `POST`
-   **Form Data:**
    -   `application_name` (string, required): The name of the application.
    -   `file` (file, required): The OpenAPI spec file (`.json` or `.yaml`).

-   **Example using `curl`:**
    ```bash
    curl -X POST "http://127.0.0.1:8000/upload/spec" \
         -H "Content-Type: multipart/form-data" \
         -F "application_name=my-awesome-app" \
         -F "file=@/path/to/your/openapi.json"
    ```

### 2. Get the Latest Specification

Retrieve the most recently uploaded specification for a specific application.

-   **URL:** `/get/latest-spec`
-   **Method:** `GET`
-   **Query Parameters:**
    -   `application_name` (string, required): The name of the application.

-   **Example using `curl`:**
    ```bash
    curl -X GET "http://127.0.0.1:8000/get/latest-spec?application_name=my-awesome-app"
    ```

### 3. Get a Specific Specification by Version

Retrieve a specific version of a specification for a given application using its version ID.

-   **URL:** `/get/spec`
-   **Method:** `GET`
-   **Query Parameters:**
    -   `application_name` (string, required): The name of the application.
    -   `version` (integer, required): The version ID of the specification to retrieve.

-   **Example using `curl`:**
    ```bash
    curl -X GET "http://127.0.0.1:8000/get/spec?application_name=my-awesome-app&version=1"
    ```
