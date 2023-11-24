'Autor: Rupert Wieser -- Naotilus -- 20220219'
import http.client
from math import ceil
from copy import copy
from json import dumps, loads
from random import random
from time import sleep, time_ns
from urllib.parse import quote
from .param import NaoConnect as Param


class NaoApp(Param):
    STADARTD_DATA_PER_TELEGRAF = 10000

    def __init__(self, host, email, password, local=False): # type: ignore
        self.auth = {
            NaoApp.NAME_HOST:host,
            NaoApp.NAME_PAYLOAD:NaoApp.NAME_EMAIL+"="+quote(email)+"&"+NaoApp.NAME_PASSWD+"="+quote(password)
        }
        self.headers = NaoApp.QUERY_TRANSFERHEADER
        self._conneciton = None # type: ignore
        self.local=local

    def sendTelegrafData(self, payload):
        ''' 
        [ '<twin>,instance=<insatance>, <measurement>=<value> <timestamp>' ] 
                                      or
          '<twin>,instance=<insatance>, <measurement>=<value> <timestamp>'
        '''
        if type(payload) != list:
            return(self._sendTelegrafData(payload=payload))
        else:
            if len(payload) > NaoApp.STADARTD_DATA_PER_TELEGRAF:
                last_idx = 0
                for idx in range(int(ceil(len(payload)/NaoApp.STADARTD_DATA_PER_TELEGRAF))-1):
                    last_idx = idx
                    sta = self._sendTelegrafData(payload[int(idx*NaoApp.STADARTD_DATA_PER_TELEGRAF):int(idx*NaoApp.STADARTD_DATA_PER_TELEGRAF)+NaoApp.STADARTD_DATA_PER_TELEGRAF])
                    if sta != 204:
                        return(sta)
                    sleep(1+idx*0.07)
                return(self._sendTelegrafData(payload[int(last_idx*NaoApp.STADARTD_DATA_PER_TELEGRAF):]))
            else:
                return(self._sendTelegrafData(payload))

    def _sendTelegrafData(self, payload):
        if type(payload) == list:
            payload = NaoApp.FORMAT_TELEGRAFFRAMESEPERATOR*len(payload) % tuple(payload)
        try:
            self._conneciton.request(NaoApp.NAME_POST, NaoApp.URL_TELEGRAF, payload, self.headers) # type: ignore
            status = self._conneciton.getresponse().status # type: ignore
            self._conneciton.close() # type: ignore
        except:
            self._loginNao()
            self._conneciton.request(NaoApp.NAME_POST, NaoApp.URL_TELEGRAF, payload, self.headers) # type: ignore
            status = self._conneciton.getresponse().status # type: ignore
            self._conneciton.close() # type: ignore
        return(status)

    def _sendDataToNaoJson(self, method, url, payload) -> dict:
        header = copy(self.headers)
        header[NaoApp.NAME_CONTENT_HEADER] = NaoApp.QUERY_HEADER_JSON
        if payload != None:
            payload = dumps(payload)
        try:
            self._conneciton.request(method, url, payload, header) # type: ignore
            data = self._conneciton.getresponse().read() # type: ignore
            self._conneciton.close() # type: ignore
        except:
            self._loginNao()
            header = copy(self.headers)
            header[NaoApp.NAME_CONTENT_HEADER] = NaoApp.QUERY_HEADER_JSON
            self._conneciton.request(method, url, payload, header) # type: ignore
            data = self._conneciton.getresponse().read() # type: ignore
            self._conneciton.close() # type: ignore
        if data == b'':
            return('') # type: ignore
        else:
            try:
                return(loads(data))
            except:
                return(-1) # type: ignore
        
    def sendNewInstance(self, asset, name, discription, geolocation=None):
        data = {
            NaoApp.NAME_NAME: name,
            NaoApp.NAME_DESCRIPTION: discription,
            NaoApp.NAME_ASSET_ID: asset
        }
        if geolocation != None:
            data[NaoApp.NAME_GEOLOCATION] = geolocation
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_INSTANCE, data)[NaoApp.NAME_ID_ID])

    def sendInstanceInputMany(self, data_list:list):
        '''
        [[<value>, <input_id>, <instance_id>], ...]
        '''
        data = []
        data_add = data.append
        for data_set in data_list:
            data_add({
            NaoApp.NAME_VALUE: data_set[0],
            NaoApp.NAME_INPUT_ID: data_set[1],
            NaoApp.NAME_RELATION_ID: data_set[2]
            })
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_INPUTS, data))

    def sendInstanceInput(self,value,input_id,instance_id):
        data = {
          NaoApp.NAME_VALUE: value,
          NaoApp.NAME_INPUT_ID: input_id,
          NaoApp.NAME_RELATION_ID: instance_id
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_INPUT, data))

    def _loginNaoLocal(self):
        try:
            self._conneciton = http.client.HTTPConnection(self.auth[NaoApp.NAME_HOST])
            self._conneciton.request(NaoApp.NAME_POST, NaoApp.URL_LOGIN, self.auth[NaoApp.NAME_PAYLOAD], NaoApp.QUERY_LOGINHEADER)
            res = self._conneciton.getresponse()
            data = loads(res.read().decode(NaoApp.NAME_UTF8))
            self.headers[NaoApp.NAME_WEBAUTH] = NaoApp.QUERY_BEARER + data[NaoApp.NAME_TOKENAC]
        except:
            sleep(1) # type: ignore
            self._conneciton = http.client.HTTPConnection(self.auth[NaoApp.NAME_HOST])
            self._conneciton.request(NaoApp.NAME_POST, NaoApp.URL_LOGIN, self.auth[NaoApp.NAME_PAYLOAD], NaoApp.QUERY_LOGINHEADER)
            res = self._conneciton.getresponse()
            data = loads(res.read().decode(NaoApp.NAME_UTF8))
            self.headers[NaoApp.NAME_WEBAUTH] = NaoApp.QUERY_BEARER + data[NaoApp.NAME_TOKENAC]


    def _loginNaoCloud(self):
        try:
            self._conneciton = http.client.HTTPSConnection(self.auth[NaoApp.NAME_HOST])
            self._conneciton.request(NaoApp.NAME_POST, NaoApp.URL_LOGIN, self.auth[NaoApp.NAME_PAYLOAD], NaoApp.QUERY_LOGINHEADER)
            res = self._conneciton.getresponse()
            data = loads(res.read().decode(NaoApp.NAME_UTF8))
            self.headers[NaoApp.NAME_WEBAUTH] = NaoApp.QUERY_BEARER + data[NaoApp.NAME_TOKENAC]
        except:
            sleep(1) # type: ignore
            self._conneciton = http.client.HTTPSConnection(self.auth[NaoApp.NAME_HOST])
            self._conneciton.request(NaoApp.NAME_POST, NaoApp.URL_LOGIN, self.auth[NaoApp.NAME_PAYLOAD], NaoApp.QUERY_LOGINHEADER)
            res = self._conneciton.getresponse()
            data = loads(res.read().decode(NaoApp.NAME_UTF8))
            self.headers[NaoApp.NAME_WEBAUTH] = NaoApp.QUERY_BEARER + data[NaoApp.NAME_TOKENAC]

    def _loginNao(self):
        if self.local:
            self._loginNaoLocal()
        else:
            self._loginNaoCloud()

    def createWorkspace(self, name, avatar=None, tagitems=[]):
        payload = {
            NaoApp.NAME_NAME: name,
            NaoApp.NAME_AVATAR_ID: avatar,
            NaoApp.NAME_TAGITEMS_ID: tagitems
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_WORKSPACE, payload))

    def createAsset(self, name, _workspace, description="", baseInterval="1m", useGeolocation=True, avatar=None, tagitems=[]):
        payload = {
            NaoApp.NAME_WORKSPACE_ID: _workspace,
            NaoApp.NAME_NAME: name,
            NaoApp.NAME_DESCRIPTION: description,
            NaoApp.NAME_AVATAR_ID: avatar,
            NaoApp.NAME_BASE_INTERVAL: baseInterval,
            NaoApp.NAME_USE_GEOLOCATION: useGeolocation
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_ASSET, payload))

    def createPath(self, name, _asset, description="", color="#02c1de", _parent=None):
        payload = {
            NaoApp.NAME_ASSET_ID: _asset,
            NaoApp.NAME_NAME: name,
            NaoApp.NAME_DESCRIPTION: description,
            NaoApp.NAME_COLOR: color,
            NaoApp.NAME_PARENT_ID: _parent
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_PATH, payload))

    def createInputcontainer(self, name, _asset, description="", color="#02c1de"):
        payload = {
            NaoApp.NAME_RELATION_ID: _asset,
            NaoApp.NAME_NAME: name,
            NaoApp.NAME_DESCRIPTION: description,
            NaoApp.NAME_COLOR: color
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_INPUTCONTAINER, payload))

    def patchIpuntsInputcontainer(self, _inputcontainer, _inputs):
        payload = {
            NaoApp.NAME_INPUTS_ID: _inputs
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_PATCH, NaoApp.URL_INPUTCONTAINER+"/"+_inputcontainer, payload))

    def createInput(self, name, _asset, value="", description="", component="input-text-field", props={}, rules={}):
        payload = {
            NaoApp.NAME_RELATION_ID: _asset,
            NaoApp.NAME_COMPONENT: component,
            NaoApp.NAME_VALUE: value,
            NaoApp.NAME_NAME: name,
            NaoApp.NAME_DESCRIPTION: description,
            NaoApp.NAME_PROPS: props,
            NaoApp.NAME_RULES: rules,
            NaoApp.NAME_FIELD: "8ee"+str(time_ns())[-5:]+"-513b-11ed-98eb-5dac241cd04e"
        }
        sleep(0.01)
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_INPUT_DESC, payload))

    def createUnit(self, name):
        payload = {
            NaoApp.NAME_NAME: name
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_UNITS, payload))

    def createSeries(self, type, name, description, _asset, _part, _unit, max, min, fill, fillValue, color="#02c1de", _tagitems=None):
        if not isinstance(fill, (float, int)):
            fill = "null"
        if not isinstance(fillValue, (float, int)):
            fillValue = None
        if not isinstance(max, (float, int)):
            max = None
        if not isinstance(min, (float, int)):
            min = None
        payload = {
            NaoApp.NAME_COLOR: color,
            NaoApp.NAME_DESCRIPTION: description,
            NaoApp.NAME_FILL: fill,
            NaoApp.NAME_FILL_VALUE: fillValue,
            NaoApp.NAME_MAX_VALUE: max,
            NaoApp.NAME_MIN_VALUE: min,
            NaoApp.NAME_NAME: name,
            NaoApp.NAME_ASSET_ID: _asset,
            NaoApp.NAME_PART_ID: _part,
            NaoApp.NAME_TAGITEMS_ID: _tagitems,
            NaoApp.NAME_UNIT_ID: _unit
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_SERIES + type, payload))

    def createInstance(self, name, description, _asset, geolocation=[], _tagitems=[]):
        payload = {
            NaoApp.NAME_NAME: name,
            NaoApp.NAME_DESCRIPTION: description,
            NaoApp.NAME_GEOLOCATION: geolocation,
            NaoApp.NAME_ASSET_ID: _asset,
            NaoApp.NAME_TAGITEMS_ID: _tagitems
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_INSTANCE, payload))
        
    def createInstancePerPayload(self,payload:dict):
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_INSTANCE, payload))

    def patchEnpointConifg(self, conf:dict, _instance=None, _series=None, _asset=None, **args):
        """
        _asset (id), _instance (id) and _series (id) can be used as arguments \n
        or \n
        _endpoint (id) (actual instance-series) \n
        -->\n
        if no endpoint in NAO you can fix it with give args _asset, _instance, _series and series_type
        --> series_type can be Meter, Sensor, Actor or Setpoint
        """
        if args.get(NaoApp.NAME_ENDPOINT_ID):
            try:
                return(self._sendDataToNaoJson("PATCH", NaoApp.URL_SERIES+args[NaoApp.NAME_ENDPOINT_ID], dumps(
                    {NaoApp.NAME_CONFIG: dumps(conf)}
                )))
            except:
                raise Exception("no _endpoint in NAO, fix with give args _asset, _instance, _series and series-type")
        if _series == None and _instance == None:
            raise Exception("_series, _instance (or _endpoint) is missing")
        result = self._sendDataToNaoJson(NaoApp.NAME_GET, NaoApp.URL_SERIES+NaoApp.QUERY_GET_ENDPOINT%(_instance,_series), None)
        if result[NaoApp.NAME_RESULTS] == []:
            if _asset == None or args.get(NaoApp.NAME_POINT_MODEL):
                raise Exception("_asset or series_type is missing")
            return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_SERIES,{
                NaoApp.NAME_INSTANCE_ID:_instance,
                NaoApp.NAME_ASSET_ID:_asset,
                NaoApp.NAME_POINT_ID:_series,
                NaoApp.NAME_POINT_MODEL:args[NaoApp.NAME_SERIES_TYPE],
                NaoApp.NAME_CONFIG:dumps(conf)
            })[NaoApp.NAME_ID_ID])
        else:
            return(self._sendDataToNaoJson("PATCH", NaoApp.URL_SERIES+result[NaoApp.NAME_RESULTS][0][NaoApp.NAME_ID_ID], dumps(
                    {NaoApp.NAME_CONFIG: dumps(conf)}
            )))

    def postEnpointConifg(self, conf:dict, _instance=None, _series=None, _asset=None):
        """
        _asset (id), _instance (id) and _series (id) can be used as arguments \n
        """
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_SERIES,{
            NaoApp.NAME_INSTANCE_ID:_instance,
            NaoApp.NAME_ASSET_ID:_asset,
            NaoApp.NAME_POINT_ID:_series,
            NaoApp.NAME_CONFIG:dumps(conf)
        })[NaoApp.NAME_ID_ID])

    def getEndpoints(self, **args):
        if len(args) > 0:
            query = NaoApp.QUERY_GET
            for arg in args:
                query += arg + "=" + args[arg] + ","
            query = query[:-1]
        else:
            query = ""
        return(self._sendDataToNaoJson(NaoApp.NAME_GET, NaoApp.URL_SERIES+query, {}))

    def deleteEndpoint(self, _endpoint):
        self._sendDataToNaoJson(NaoApp.NAME_DELETE, NaoApp.URL_SERIES+_endpoint, {})
        return(NaoApp.NAME_DELETE)
    
    def getWorkspace(self, **args):
        if len(args) > 0:
            query = NaoApp.QUERY_GET
            for arg in args:
                query += arg + "=" + args[arg] + ","
            query = query[:-1]
        else:
            query = ""
        return(self._sendDataToNaoJson(NaoApp.NAME_GET, NaoApp.URL_WORKSPACE+query, {}))
    
    def getAssets(self, **args):
        if len(args) > 0:
            query = NaoApp.QUERY_GET
            for arg in args:
                query += arg + "=" + args[arg] + ","
            query = query[:-1]
        else:
            query = ""
        return(self._sendDataToNaoJson(NaoApp.NAME_GET, NaoApp.URL_ASSET+query, {}))

    def getInstances(self, **args):
        if len(args) > 0:
            query = NaoApp.QUERY_GET
            for arg in args:
                query += arg + "=" + args[arg] + ","
            query = query[:-1]
        else:
            query = ""
        return(self._sendDataToNaoJson(NaoApp.NAME_GET, NaoApp.URL_INSTANCE+query, {}))
    
    def getInput(self, input_id, instance_id, **args):
        query = NaoApp.QUERY_GET
        query += NaoApp.NAME_RELATION_ID+"="+instance_id+","+NaoApp.NAME_INPUT_ID+"="+input_id+","
        for arg in args:
            query += arg + "=" + args[arg] + ","
        query = query[:-1]
        return(self._sendDataToNaoJson(NaoApp.NAME_GET, NaoApp.URL_INPUT+query, {}))

    def patchInstance(self, dict_instance, instance_id):
        return(self._sendDataToNaoJson(NaoApp.NAME_PATCH, NaoApp.URL_INSTANCE+"/"+instance_id, dict_instance))
    
    def getSeries(self, asset, select=[]):
        if len(select) > 0:
            select_q = NaoApp.QUERY_SELECT
            for arg in select:
                select_q += arg + ","
            select_q = select_q[:-1]
        else:
            select_q = ""
        return(self._sendDataToNaoJson(NaoApp.NAME_GET, NaoApp.URL_SERIES%(asset)+select_q, {}))

    def getUnits(self, **args):
        if len(args) > 0:
            query = NaoApp.QUERY_GET
            for arg in args:
                query += arg + "=" + args[arg] + ","
            query = query[:-1]
        else:
            query = ""
        return(self._sendDataToNaoJson(NaoApp.NAME_GET, NaoApp.URL_UNITS+query, {}))

    def getSingelValues(self, organizationId, first_time="-365d", last_time="now()", points=[{"id":"all"}], validates=False, aggregate="mean"):
        '''
        points ->   {
                        "id": str,
                        "asset": str,
                        "instance": str,
                        "series": str,
                    }
        '''
        payload = {
            NaoApp.NAME_SELECT:{
                NaoApp.NAME_ORGANIZATIONID:organizationId,
                NaoApp.NAME_POINTS:points,
                NaoApp.NAME_RANGE: {
                    NaoApp.NAME_START:first_time,
                    NaoApp.NAME_STOP:last_time
                },
                NaoApp.NAME_VALIDATES:validates,
            },
            NaoApp.NAME_AGGREGATE:aggregate
        }
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_SINGELVALUES, payload=payload))

    def getPlotformatetTimeseries(self, select):
        return(self._sendDataToNaoJson(NaoApp.NAME_POST, NaoApp.URL_PLOTTIMESERIES, payload=select))
