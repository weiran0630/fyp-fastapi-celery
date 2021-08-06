import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def preprocessing(data):
    # 載入必要 worksheets
    grad = pd.read_excel("app/celery_queue/transform/hi_sch_grad.xlsx")
    uni = pd.read_excel("app/celery_queue/transform/uni.xlsx")
    fac = pd.read_excel("app/celery_queue/transform/fac.xlsx")

    data = data.copy(deep=True)  # 複製 dataframe 防止修改原來資料

    mask = ["序號", "性別", "畢業年度", "國數自", "居住地區", "英", "社", "通過篩選志願數", "科大志願數(國立)"]
    data.drop(mask, axis=1, inplace=True)

    mask = {
        "一": "學校1",
        "Unnamed: 14": "科系1",
        "二": "學校2",
        "Unnamed: 16": "科系2",
        "Unnamed: 18": "科系3",
        "Unnamed: 20": "科系4",
        "Unnamed: 22": "科系5",
        "Unnamed: 24": "科系6",
        "Unnamed: 26": "科系7",
        "Unnamed: 28": "科系8",
        "Unnamed: 30": "科系9",
        "三": "學校3",
        "四": "學校4",
        "五": "學校5",
        "六": "學校6",
        "國立科大(一)": "學校7",
        "國立科大(二)": "學校8",
        "國立科大(三)": "學校9",
    }
    data.rename(columns=mask, inplace=True)

    for i in range(0, len(data)):
        for j in range(0, len(grad)):
            if data.loc[i, "畢業學校"] == grad.loc[j, "畢業學校"]:
                data.loc[i, "畢業學校X"] = grad.loc[j, "X"]
                data.loc[i, "畢業學校Y"] = grad.loc[j, "Y"]

    for i in range(1, 10):
        for j in range(0, len(data)):
            for k in range(0, len(uni)):
                if data.loc[j, "學校" + str(i)] is np.nan:
                    data.loc[j, "學校" + str(i) + "X"] = 0
                    data.loc[j, "學校" + str(i) + "Y"] = 0
                    data.loc[j, "學校" + str(i)] = 200
                if data.loc[j, "學校" + str(i)] == uni.loc[k, "學校更新"]:
                    data.loc[j, "學校" + str(i)] = uni.loc[k, "編號"]
                    data.loc[j, "學校" + str(i) + "X"] = uni.loc[k, "X"]
                    data.loc[j, "學校" + str(i) + "Y"] = uni.loc[k, "Y"]
                    break
            for k in range(0, len(fac)):
                if data.loc[j, "科系" + str(i)] is np.nan:
                    data.loc[j, "科系" + str(i)] = 100
                    break
                if data.loc[j, "科系" + str(i)] == fac.loc[k, "科系"]:
                    data.loc[j, "科系" + str(i)] = fac.loc[k, "編號"]
                    break
                if k == len(fac) - 1 and data.loc[j, "科系" + str(i)] != fac.loc[k, "編號"]:
                    data.loc[j, "科系" + str(i)] = 90

    mask = [
        "國",
        "數",
        "自",
        "學校1",
        "科系1",
        "學校1X",
        "學校1Y",
        "學校2",
        "科系2",
        "學校2X",
        "學校2Y",
        "學校3",
        "科系3",
        "學校3X",
        "學校3Y",
        "學校4",
        "科系4",
        "學校4X",
        "學校4Y",
        "學校5",
        "科系5",
        "學校5X",
        "學校5Y",
        "學校6",
        "科系6",
        "學校6X",
        "學校6Y",
        "學校7",
        "科系7",
        "學校7X",
        "學校7Y",
        "學校8",
        "科系8",
        "學校8X",
        "學校8Y",
        "學校9",
        "科系9",
        "學校9X",
        "學校9Y",
    ]
    data.reindex(mask)

    mask = [
        "畢業學校",
        "學校1",
        "學校2",
        "學校3",
        "學校4",
        "學校5",
        "學校6",
        "學校7",
        "科系7",
        "學校7X",
        "學校7Y",
        "學校8",
        "科系8",
        "學校8X",
        "學校8Y",
        "學校9",
        "科系9",
        "學校9X",
        "學校9Y",
    ]
    data.drop(
        columns=mask,
        inplace=True,
    )

    data = data.fillna(0)

    minmax_scale = MinMaxScaler(feature_range=(0, 1))
    scaled_data = minmax_scale.fit_transform(data)

    return scaled_data
