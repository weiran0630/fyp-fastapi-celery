import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def preprocessing(data):
    # 載入必要 worksheets
    grad = pd.read_excel("app/celery_queue/transform/hi_sch_grad.xlsx")
    uni = pd.read_excel("app/celery_queue/transform/uni_v2.xlsx")
    fac = pd.read_excel("app/celery_queue/transform/fac.xlsx")

    data = data.copy(deep=True)  # 複製 dataframe 防止修改原來資料

    mask = ["序號", "性別", "畢業年度", "國數自", "居住地區",
            "英", "社", "通過篩選志願數", "科大志願數(國立)"]
    data.drop(mask, axis=1, inplace=True)

    for i in range(0, len(data)):
        for j in range(0, len(grad)):
            if data.loc[i, "畢業學校"] == grad.loc[j, "畢業學校"]:
                data.loc[i, "畢業學校X"] = grad.loc[j, "X"]
                data.loc[i, "畢業學校Y"] = grad.loc[j, "Y"]

    for i in range(1, 9):
        for j in range(0, len(data)):
            for k in range(0, len(uni)):
                if data.loc[j, "學校" + str(i)] is np.nan:
                    data.loc[j, "學校" + str(i) + "X"] = 0
                    data.loc[j, "學校" + str(i) + "Y"] = 0
                    # data.loc[j, "學校" + str(i)] = 200
                if data.loc[j, "學校" + str(i)] == uni.loc[k, "學校名稱"]:
                    # data.loc[j, "學校" + str(i)] = uni.loc[k, "學校代碼"]
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
        "科系1",
        "學校1X",
        "學校1Y",
        "科系2",
        "學校2X",
        "學校2Y",
        "科系3",
        "學校3X",
        "學校3Y",
        "科系4",
        "學校4X",
        "學校4Y",
        "科系5",
        "學校5X",
        "學校5Y",
        "科系6",
        "學校6X",
        "學校6Y",
        "科系7",
        "學校7X",
        "學校7Y",
        "科系8",
        "學校8X",
        "學校8Y",
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
        "科系9"
    ]
    data.drop(
        columns=mask,
        inplace=True,
    )

    data = data.fillna(0)

    minmax_scale = MinMaxScaler(feature_range=(0, 1))
    scaled_data = minmax_scale.fit_transform(data)

    return scaled_data
