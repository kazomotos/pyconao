from pyconao.naopandas import NaoPandas


Nao = NaoPandas(host="",email="",password="")

assets = Nao.getAssets()
print(assets)

instances = Nao.getInstances()
print(instances)

series = Nao.getSeries()
print(series)

dataframe = Nao.getSeriesData(series[:350],interval="1d")
print(dataframe)



print("end")