'Autor: Rupert Wieser -- Naotilus -- 20230414'
import pandas as pd
from typing import Literal, Union, Annotated
from .naoapp import NaoApp
from datetime import datetime
import re

class NaoPandas(NaoApp):

    def __init__(self, host:str, email:str, password:str, local:bool=False):
        super().__init__(host,email,password,local)
        self.assets = {NaoPandas.NAME_WORKSPACE:[],NaoPandas.NAME_WORKSPACE_ID:[],NaoPandas.NAME_ASSET:[],NaoPandas.NAME_ASSET_ID:[]}
        self.instances = {
            NaoPandas.NAME_WORKSPACE:[],NaoPandas.NAME_WORKSPACE_ID:[],NaoPandas.NAME_ASSET:[],
            NaoPandas.NAME_ASSET_ID:[],NaoPandas.NAME_INSTANCE:[],NaoPandas.NAME_INSTANCE_ID:[]
        }
        self.series = {
            NaoPandas.NAME_WORKSPACE:[],NaoPandas.NAME_WORKSPACE_ID:[],NaoPandas.NAME_ASSET:[],NaoPandas.NAME_ASSET_ID:[],
            NaoPandas.NAME_INSTANCE:[],NaoPandas.NAME_INSTANCE_ID:[],NaoPandas.NAME_SERIES:[],NaoPandas.NAME_SERIES_ID:[]
        }
        self.organization = super().getWorkspace().get(NaoPandas.NAME_RESULTS)[0][NaoPandas.NAME_ORGANIZATION_ID] #type:ignore

    def getAssets(self) -> pd.DataFrame:
        if len(self.assets[NaoPandas.NAME_ASSET]) == 0:
            workspaces = {}
            for worksp in super().getWorkspace().get(NaoPandas.NAME_RESULTS):workspaces[worksp[NaoPandas.NAME_ID_ID]]=worksp[NaoPandas.NAME_NAME] #type:ignore
            for asset in super().getAssets().get(NaoPandas.NAME_RESULTS): #type:ignore
                self.assets[NaoPandas.NAME_ASSET].append(asset[NaoPandas.NAME_NAME])
                self.assets[NaoPandas.NAME_ASSET_ID].append(asset[NaoPandas.NAME_ID_ID])
                self.assets[NaoPandas.NAME_WORKSPACE].append(workspaces[asset[NaoPandas.NAME_WORKSPACE_ID]])
                self.assets[NaoPandas.NAME_WORKSPACE_ID].append(asset[NaoPandas.NAME_WORKSPACE_ID])
        return(pd.DataFrame(self.assets))

    def getInstances(self) -> pd.DataFrame:
        if len(self.instances[NaoPandas.NAME_ASSET]) == 0:
            add = {}
            for adds in self.instances.keys():add[adds]=add[adds]= self.instances[adds].append
            workspaces = {}
            assets = {}
            for worksp in super().getWorkspace().get(NaoPandas.NAME_RESULTS):workspaces[worksp[NaoPandas.NAME_ID_ID]]=worksp[NaoPandas.NAME_NAME] #type:ignore
            for asset in super().getAssets().get(NaoPandas.NAME_RESULTS):assets[asset[NaoPandas.NAME_ID_ID]]=[asset[NaoPandas.NAME_NAME],asset[NaoPandas.NAME_WORKSPACE_ID]] #type:ignore
            for instance in super().getInstances().get(NaoPandas.NAME_RESULTS): #type:ignore
                add[NaoPandas.NAME_ASSET](assets[instance[NaoPandas.NAME_ASSET_ID]][0])
                add[NaoPandas.NAME_ASSET_ID](instance[NaoPandas.NAME_ASSET_ID])
                add[NaoPandas.NAME_WORKSPACE](workspaces[assets[instance[NaoPandas.NAME_ASSET_ID]][1]])
                add[NaoPandas.NAME_WORKSPACE_ID](assets[instance[NaoPandas.NAME_ASSET_ID]][1])
                add[NaoPandas.NAME_INSTANCE](instance[NaoPandas.NAME_NAME])
                add[NaoPandas.NAME_INSTANCE_ID](instance[NaoPandas.NAME_ID_ID])
        return(pd.DataFrame(self.instances))

    #M_ROUTE_SERIES = "/instance/internal/all" ?query=datapoints._point=in$%s&select=_id"
    def getSeries(self) -> pd.DataFrame:
        if len(self.series[NaoPandas.NAME_ASSET]) == 0:
            add = {}
            workspaces = {}
            assets = {}
            for adds in self.series.keys():add[adds]=add[adds]= self.series[adds].append
            for worksp in super().getWorkspace().get(NaoPandas.NAME_RESULTS):workspaces[worksp[NaoPandas.NAME_ID_ID]]=worksp[NaoPandas.NAME_NAME] #type:ignore
            for asset in super().getAssets().get(NaoPandas.NAME_RESULTS):assets[asset[NaoPandas.NAME_ID_ID]]=[asset[NaoPandas.NAME_NAME]] #type:ignore
            for _asset in assets: 
                asset = super().getSeries(_asset,select=[
                    NaoPandas.NAME_INSTANCES,
                    NaoPandas.NAME_WORKSPACE_ID,
                    NaoPandas.NAME_ASSET_ID,
                    NaoPandas.NAME_INSTANCES
                    # NaoPandas.NAME_ACTORS,
                    # NaoPandas.NAME_METERS,
                    # NaoPandas.NAME_SENSORS,
                    # NaoPandas.NAME_SETPOINTS
                ])
                instances = super().getInstances(**{NaoPandas.NAME_ASSET_ID:_asset})[NaoPandas.NAME_RESULTS]
                for instance in instances: #type:ignore
                    for type_s in [NaoPandas.NAME_METERS, NaoPandas.NAME_SENSORS, NaoPandas.NAME_SETPOINTS, NaoPandas.NAME_ACTORS]:
                        for serie in asset[type_s]:
                            add[NaoPandas.NAME_ASSET](assets[_asset][0])
                            add[NaoPandas.NAME_ASSET_ID](_asset)
                            add[NaoPandas.NAME_WORKSPACE](workspaces[instance[NaoPandas.NAME_WORKSPACE_ID]])
                            add[NaoPandas.NAME_WORKSPACE_ID](instance[NaoPandas.NAME_WORKSPACE_ID])
                            add[NaoPandas.NAME_INSTANCE](instance[NaoPandas.NAME_NAME])
                            add[NaoPandas.NAME_INSTANCE_ID](instance[NaoPandas.NAME_ID_ID])
                            add[NaoPandas.NAME_SERIES](serie[NaoPandas.NAME_NAME])
                            add[NaoPandas.NAME_SERIES_ID](serie[NaoPandas.NAME_ID_ID])
        return(pd.DataFrame(self.series))
    
    def getSeriesData(self,series:pd.DataFrame,start:datetime=datetime.fromisoformat("2021-12-31 23:00:00"),stop:datetime=datetime.fromisoformat("2022-01-30 23:00:00"),validate=True,interval:str="15m",aggregate:Literal["mean","median","max","min","last","first"]="mean", tz="UTC") -> pd.DataFrame:
        if not re.match(r"^\d+[s,m,h,d]$", interval):
            raise ValueError("only s, m, h, or d (seconds, minutes, hours, days) afterwards a int possible")
        if aggregate not in ["mean","median","max","min","last","first"]:
            raise ValueError("only 'mean','median','max','min','last','first' possible for aggregate")
        if (stop-start).total_seconds() < 0:
            raise ValueError("stop must be greater than start")
        # if len(series)>150:
        #     raise ValueError("maximal 150 series per call")
        if (stop-start).total_seconds()/self._intervalToSec(interval)*len(series) > 10000000:
            raise ValueError("maximal 10.000.000 measurment data per call")
        param={
            NaoPandas.NAME_PLOT:{
                NaoPandas.NAME_TIME:NaoPandas.STANDARD_TIMEFORMAT,
                NaoPandas.NAME_TRACES: [],
                NaoPandas.NAME_TYPE: NaoPandas.STANDARD_SERIESTYPE
            },
            NaoPandas.NAME_SELECT:{
                NaoPandas.NAME_ORGANIZATIONID:self.organization,
                NaoPandas.NAME_POINTS: [],
                NaoPandas.NAME_RANGE: {
                    NaoPandas.NAME_START:str(start).replace(" ", "T")+"Z",
                    NaoPandas.NAME_STOP:str(stop).replace(" ", "T")+"Z"
                },
                NaoPandas.NAME_VALIDATES:validate
            },            
            NaoPandas.NAME_AGGREGATE_WINDOW:{
                NaoPandas.NAME_INTERVAL:interval,
                NaoPandas.NAME_METHOD: aggregate
            }
        }
        add_point = param[NaoPandas.NAME_SELECT][NaoPandas.NAME_POINTS].append
        add_traces = param[NaoPandas.NAME_PLOT][NaoPandas.NAME_TRACES].append
        names = []
        add_name = names.append
        for idx in series.index:
            name = "" 
            for idy in idx: name+=idy+"."
            add_name(name[:-1])
        for idx in range(len(series)):
            point={
                NaoPandas.NAME_ASSET: series[NaoPandas.NAME_ASSET_ID][idx],
                NaoPandas.NAME_INSTANCE: series[NaoPandas.NAME_INSTANCE_ID][idx],
                NaoPandas.NAME_SERIES: series[NaoPandas.NAME_SERIES_ID][idx],
            }
            add_traces({
                NaoPandas.NAME_ID:names[idx],
                NaoPandas.NAME_Y:{
                    NaoPandas.NAME_POINT:point
                }
            })
            add_point(point)
        raw_frame = {}
        data=self.getPlotformatetTimeseries(param)
        if data==-1:return(pd.DataFrame())
        for dat in data[NaoPandas.NAME_RESULT][NaoPandas.NAME_TRACES]:
            raw_frame[dat[NaoPandas.NAME_ID]] = dat[NaoPandas.NAME_Y]
        frame = pd.DataFrame(raw_frame)
        if tz == None:
            frame.index = pd.DatetimeIndex(data[NaoPandas.NAME_RESULT][NaoPandas.NAME_TIME], dtype='datetime64[ns, Europe/Berlin]').tz_convert("UTC").tz_convert(None)
        else:
            frame.index = pd.DatetimeIndex(data[NaoPandas.NAME_RESULT][NaoPandas.NAME_TIME], dtype='datetime64[ns, Europe/Berlin]').tz_convert(tz)
        return(frame)

    def _intervalToSec(self, interval:str) -> float:
        if interval[-1] == "s":
            return(float(interval[:-1]))
        elif interval[-1] == "m":
            return(float(interval[:-1])*60)
        elif interval[-1] == "h":
            return(float(interval[:-1])*3600)
        elif interval[-1] == "d":
            return(float(interval[:-1])*86400)
        elif interval[-1] == "w":
            return(float(interval[:-1])*604800)
        else:
            return(1)