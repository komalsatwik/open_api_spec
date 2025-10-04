import asyncio
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
from validator import ParserFactory, SpecValidator
from database import insert_file,init_db,close_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(init_db)
    yield
    await asyncio.to_thread(close_connection)

app = FastAPI(lifespan=lifespan)


@app.post("/upload/spec")
async def upload_spec(application_name:str = Form(...),
                file:UploadFile = File(...)):
    
    try:
        file_name = file.filename
        content = await file.read()

        parser = ParserFactory.get_parser(file_name)
        validator = SpecValidator(parser)
        validator.validate(content)

        insert_file(application_name,file_name, file_name.split(".")[-1].lower(), content)

        return JSONResponse({"message":"File Uploaded succssfully", "application":application_name},200)
    except Exception as e:
        print(e)
        return JSONResponse({"message":"Error occurred while uploading file"},400)



if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)