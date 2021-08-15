from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from starlette.background import BackgroundTask
from .celery_queue.worker import create_task
from time import time
import pandas as pd
import os

# 初始化 FastAPI 實例
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000", "https://mcu-ai-admission-predict.vercel.app"],
    allow_methods=["GET, POST"],
)


# http://example.com/
@app.get("/")
async def root():
    return {"message": "Hello World"}


# http://example.com/predict
# 請求文件方法參考官方docs https://fastapi.tiangolo.com/zh/tutorial/request-files/?h=file
@app.post("/predict", status_code=201)
async def predict(uploadfile: UploadFile = File(...)):
    file = await uploadfile.read()
    df_json_str = pd.read_excel(file).to_json(force_ascii=False)  # 以 pd.read_excel() 讀取檔案後將 Dataframe JSON序列化

    task = create_task.delay(df_json_str)  # 把工作分發到 Celery worker

    return {"task_id": task.id}  # 回應客戶端工作實例的id (task_id)


# http://example.com/predict/{task_id}
@app.get("/tasks/{task_id}")
async def get_status(task_id):
    task = create_task.AsyncResult(task_id)  # 獲取和 task_id 相應的工作實例

    if not task.ready():
        return JSONResponse(status_code=202, content={"task_id": task_id, "status": task.status})  # 若工作尚未結束，回傳當前工作的狀態

    result = task.get()  # 工作完成，獲取工作實例的結果 （result）
    try:
        file_path = f"{int(time())}.xlsx"  # {timestamp}.xlsx
        pd.read_json(result).to_excel(file_path)  # 將工作結果還原序列化然後產生 excel檔到 file_path

        return FileResponse(
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            path=file_path,
            filename=file_path,
            background=BackgroundTask(os.remove, file_path),  # 客戶端下載檔案後移除伺服器中的檔案
        )
    except Exception as e:
        print(e)
        return {"error": "unknown error occurred"}  # 例外處理，出現 Exception 時回傳錯誤訊息
