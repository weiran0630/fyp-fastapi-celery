from celery import Celery
import os
import pandas as pd
from .transform import preprocessing
from tensorflow.keras.models import load_model

# 初始化 Celery 實例，提供 REDIS_URL 作爲 Celery 的 broker 以及 backend
celery = Celery(
    __name__,
    broker=os.environ["REDIS_URL"],
    backend=os.environ["REDIS_URL"],
)


@celery.task(name="create_task", track_started=True)
def create_task(data_serialized):
    model = load_model("app/celery_queue/model_20210326.h5")  # 載入 Tensorflow 模型
    try:
        data = pd.read_json(data_serialized)  # 還原序列化 (json -> pandas Dataframe)

        transformed_data = preprocessing(data)  # .transform.preprocessing() 前處理，不更動原資料回傳處理後的資料

        # model.predict() 預測
        # flatten() 將預測結果降維
        # pd.Series() 轉換爲 pandas Series
        probability = pd.Series(model.predict(transformed_data, verbose=1).flatten())

        result = pd.concat([data, probability], axis=1)  # 連接 (concat) 原來的資料和預測結果
        result.columns = [*result.columns[:-1], "預測結果"]

        return result.to_json(force_ascii=False)  # 回傳序列化結果

    except Exception as err:
        print(err)
        return err  # 例外處理，出現 Exception 時回傳錯誤訊息
