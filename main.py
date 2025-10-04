import asyncio
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
from validator import ParserFactory, SpecValidator
from database import (
    insert_file,
    init_db,
    close_connection,
    get_latest_file,
    get_spec_by_version_and_application,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(init_db)
    yield
    await asyncio.to_thread(close_connection)


app = FastAPI(lifespan=lifespan)


@app.post("/upload/spec")
async def upload_spec(application_name: str = Form(...), file: UploadFile = File(...)):

    try:
        file_name = file.filename
        content = await file.read()

        parser = ParserFactory.get_parser(file_name)
        validator = SpecValidator(parser)
        validator.validate(content.decode("utf-8"))

        insert_file(
            application_name, file_name, file_name.split(".")[-1].lower(), content
        )

        return JSONResponse(
            {"message": "File Uploaded succssfully", "application": application_name},
            200,
        )
    except ValueError as e:
        return JSONResponse({"message": f"Error occurred: {e}"}, 400)
    except Exception as e:
        return JSONResponse(
            {"message": f"Error occurred while uploading file.{e}"}, 500
        )


@app.get("/get/latest-spec")
async def get_latest_spec(application_name: str):
    try:
        latest_file = get_latest_file(application_name)

        if not latest_file:
            return JSONResponse(
                {"message": "No files found for the application."}, status_code=404
            )

        file_data = latest_file["file_data"].decode("utf-8")

        return JSONResponse(
            {
                "message": "Latest file retrieved successfully",
                "application_name": latest_file["application_name"],
                "version_id": latest_file["version"],
                "file_data": file_data,
                "filename": latest_file["filename"],
                "content_type": latest_file["content_type"],
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            {"message": "Error occurred while retrieving file", "error": str(e)},
            status_code=400,
        )


@app.get("/get/spec")
async def get_spec_by_version(application_name: str, version: int):

    try:

        file = get_spec_by_version_and_application(application_name, version)

        if not file:
            return JSONResponse(
                {
                    "message": "No file found with the specified application name and version id"
                },
                400,
            )

        file_data = file["file_data"].decode("utf-8")

        return JSONResponse(
            {
                "message": "File retrieved successfully",
                "application_name": file["application_name"],
                "version_id": file["version"],
                "filename": file["filename"],
                "file_data": file_data,
                "content_type": file["content_type"],
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            {"message": "Error occurred while retrieving file", "error": str(e)},
            status_code=400,
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

