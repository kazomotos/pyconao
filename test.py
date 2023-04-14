from pyconao.naopandas import NaoPandas
from datetime import datetime

Nao = NaoPandas(host="",email="",password="")

assets = Nao.getAssets()
print(assets)

instances = Nao.getInstances()
print(instances)

series = Nao.getSeries()
print(series)

dataframe = Nao.getSeriesData(
    series=series[:350],
    interval="1d",
    aggregate="mean",
    validate=True,
    start=datetime.fromisoformat("2021-12-31 23:00:00"),
    stop=datetime.fromisoformat("2022-01-30 23:00:00")
)
print(dataframe)



print("end")