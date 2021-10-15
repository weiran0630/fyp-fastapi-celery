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
    allow_origins=["https://mcu-ai-admission-predict.vercel.app"],
    allow_methods=["GET, POST"],
)


# http://example.com/
@app.get("/")
async def root():
    return {"message": "Hello World"}


# http://example.com/predict
# 請求文件方法參考官方docs https://fastapi.tiangolo.com/zh/tutorial/request-files/?h=file
@app.post("/predict")
async def predict(uploadfile: UploadFile = File(...)):
    file = await uploadfile.read()
    # 以 pd.read_excel() 讀取檔案後將 Dataframe JSON序列化
    df_json_str = pd.read_excel(file).to_json(force_ascii=False)

    task = create_task.delay(df_json_str)  # 把工作分發到 Celery worker

    # 回應客戶端工作實例的id (task_id)
    return JSONResponse(status_code=201, content={"task_id": task.id})


@app.get("/file")
async def get_sample_file():
    file_path = "app/sample_file.xlsx"

    return FileResponse(
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        path=file_path,
        filename=file_path
    )


@app.get("/file/{task_id}")
async def get_predicted_file(task_id):
    if os.path.isfile(f"{task_id}.xlsx") == False:
        return JSONResponse(status_code=404, content={"message": "File not found!"})
    else:
        file_path = f"{task_id}.xlsx"

        return FileResponse(
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            path=file_path,
            filename=file_path,
            background=BackgroundTask(
                os.remove, file_path),  # 客戶端下載檔案後移除伺服器中的檔案
        )


# http://example.com/predict/{task_id}
@app.get("/tasks/{task_id}")
async def get_status(task_id):
    task = create_task.AsyncResult(task_id)  # 獲取和 task_id 相應的工作實例

    if not task.ready():
        # 若工作尚未結束，回傳當前工作的狀態
        return JSONResponse(status_code=202, content={"task_id": task_id, "status": task.status})

    result = task.get()  # 工作完成，獲取工作實例的結果 （result）
    try:
        file_path = f"{task_id}.xlsx"

        # 將工作結果還原序列化然後產生 excel檔到 file_path
        pd.read_json(result).to_excel(file_path)

        return JSONResponse(result)  # 回傳資料到前端

    except Exception as e:
        # 例外處理，出現 Exception 時回傳錯誤訊息
        return JSONResponse(status_code="500", content={"error": "unknown error occurred"})
