from fastapi import FastAPI, File, UploadFile, HTTPException
from tempfile import NamedTemporaryFile
from fastapi.responses import FileResponse
import os
from converter import load_config, convert_md_to_df, convert_df_to_excel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/markdown/")
async def convert_file(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False) as temp_file:
        # 受け取ったファイルの内容を一時ファイルに書き込みます
        contents = await file.read()
        temp_file.write(contents)
        temp_file.flush()

        # 一時ファイルのパスを取得します
        temp_file_path = temp_file.name
        config = load_config();
        
        output_file_name = os.path.splitext(file.filename)[0] + ".xlsx"
        
        df = convert_md_to_df(temp_file_path, config["md"])
        convert_df_to_excel(df, config["excel"], output_file_name, True)

        # 一時ファイルをレスポンスとして返します
        return FileResponse(output_file_name, filename= 'sample_data.xlsx', media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')