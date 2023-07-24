'Autor: Rupert Wieser -- Naotilus -- 202202122'

class Param():
    FORMAT_TELEGRAFFRAMESEPERATOR = "%s\n"
    FORMAT_TELEGRAFFRAMESTRUCT = "%s,instance=%s %s=%f %.0f"
    FORMAT_TELEGRAFFRAMESTRUCT3 = ",instance="
    FORMAT_TELEGRAFFRAMESTRUCT2 = "%s,instance=%s %s="
    NAME_ENDPOINT_ID = "_endpoint"
    NAME_GET = "GET"
    NAME_POST = "POST"
    NAME_PATCH = "PATCH"
    NAME_DELETE = "DELETE"
    NAME_RESULTS = "results"
    NAME_RESULT = "result"
    NAME_LASTTIME = "last_timestamp"
    NAME_INTERVAL = "interval"
    NAME_VALUE = "value"
    NAME_VARIABLE = "variable"
    NAME_TIMESTAP = "timestamp"
    NAME_HOST = "host"
    NAME_COUNT = "count"
    NAME_WEBAUTH = "Authorization"
    NAME_TELEGRAF = "telegraf"
    NAME_UTF8 = "utf-8"
    NAME_TOKENAC = "accessToken"
    NAME_TOKENRE = "refreshToken"
    NAME_COOKIE = "Cookie"
    NAME_EMAIL = "email"
    NAME_PASSWD = "password"
    NAME_PAYLOAD = "payload"
    NAME_TYPE = "type"
    NAME_CHANNEL = "channel"
    NAME_UNIT = "unit"
    NAME_TRANSFERCHANNELS = "transfer_channels"
    NAME_POINT = "point"
    NAME_POINT_ID = "_point"
    NAME_ASSET = "asset"
    NAME_INSTANCE = "instance"
    NAME_INSTANCES = "instances"
    NAME_INSTANCE_ID = "_instance"
    NAME_SERIES = "series"
    NAME_SERIES_ID = "_series"
    NAME_CONTENT_HEADER = "Content-Type"
    NAME_ASSET_ID = "_asset"
    NAME_WORKSPACE = "workspace"
    NAME_WORKSPACE_ID = "_workspace"
    NAME_NAME = "name"
    NAME_DESCRIPTION = "description"
    NAME_GEOLOCATION = "geolocation"
    NAME_ID_ID = "_id"
    NAME_ID = "id"
    NAME_INPUT_ID = "_input"
    NAME_INPUTS_ID = "_inputs"
    NAME_RELATION_ID = "_relation"
    NAME_PROPS = "props"
    NAME_RULES = "rules"
    NAME_FIELD = "field"
    NAME_COLOR = "color"
    NAME_FILL = "fill"
    NAME_FILL_VALUE = "fillValue"
    NAME_MAX_VALUE = "max"
    NAME_MIN_VALUE = "min"
    NAME_NAME = "name"
    NAME_PART_ID = "_part"
    NAME_TAGITEMS_ID = "_tagitems"
    NAME_UNIT_ID = "_unit"
    NAME_PARENT_ID = "_parent"
    NAME_BASE_INTERVAL = "baseInterval"
    NAME_USE_GEOLOCATION = "useGeolocation"
    NAME_AVATAR_ID = "_avatar"
    NAME_COMPONENT = "component"
    NAME_POINT_MODEL = "pointModel"
    NAME_CONFIG = "config"
    NAME_SELECT = "select"
    NAME_POINTS = "points"
    NAME_RANGE = "range"
    NAME_VALIDATES = "validates"
    NAME_AGGREGATE = "aggregate"
    NAME_START = "start"
    NAME_STOP = "stop"
    NAME_ORGANIZATIONID = "organizationId"
    NAME_ORGANIZATION_ID = "_organization"
    NAME_TIME = "time"
    NAME_CNFIG = "config"
    NAME_INPUT = "input"
    NAME_TIME = "time"
    NAME_SERIES_TYPE = "series_type"
    NAME_AGGREGATE_WINDOW = "aggregatewindow"
    NAME_METHOD = "method"
    NAME_POINTS = "points"
    NAME_Y = "y"
    NAME_PLOT = "plot"
    NAME_TRACES = "traces"
    NAME_TRACE = "trace"
    NAME_METERS = "meters"
    NAME_ACTORS = "actors"
    NAME_SETPOINTS = "setpoints"
    NAME_SENSORS = "sensors"

class Labling(Param):
    ASSET = "asset"
    LABLING_SERIES = "labling_series"
    NAO_INSTANCE = "instance_in_nao"
    LABLING_INPUT = "labling_input"
    WORKSPACE = "workspace"
    INSTANCE = "instance"
    DISCRIPTION = "discription"
    DESCRIPTION = "description"
    UNIT = "unit"
    COMPONENT_0 = "component_0"
    SENSOR_TYPE = "sensor_type"
    NAME = "name"
    FILL_METHOD = "fill_method"
    FILL_VALUE = "fill_value"
    MIN_VALUE = "min_value"
    MAX_VALUE = "max_value"
    COLOR = "color"
    TAG_GROUPE_0 = "tag_groupe_0"
    TAG_NAME_0 = "tag_name_0"
    TAG_VALUE_0 = "tag_value_0"
    MONISOFT_ID = "monisoft_id"
    CONFIG =  "config"
    ID = "id"
    CHANNELS_IN_NAO = "channels_in_nao"

class NaoConnect(Param):
    URL_LOGIN = "/api/user/auth/login"
    URL_TELEGRAF = "/api/telegraf"
    URL_INSTANCE = "/api/nao/instance"
    URL_INPUT = "/api/nao/inputvalue"
    URL_INPUT_DESC = "/api/nao/input"
    URL_INPUTCONTAINER = "/api/nao/inputcontainer"
    URL_INPUTS = "/api/nao/inputvalue/many"
    URL_WORKSPACE = "/api/nao/workspace"
    URL_ASSET = "/api/nao/asset"
    URL_PATH = "/api/nao/part"
    URL_UNITS = "/api/nao/units"
    URL_SERIES = "/api/nao/asset/more/%s"
    URL_SINGELVALUES = "/api/series/data/singlevalues"
    URL_PLOTTIMESERIES = "/api/series/data/plot"
    URL_CONSOLIDATE = "template"
    QUERY_GET_ENDPOINT = "?query=_instance=%s,_point=%s"
    QUERY_GET = "?query="
    QUERY_SELECT = "?select="
    QUERY_HEADER_JSON = 'application/json'
    QUERY_BEARER = "Bearer "
    QUERY_LOGINHEADER = {'Content-Type': 'application/x-www-form-urlencoded'}
    QUERY_TRANSFERHEADER = {"Authorization": "", 'Content-Type': 'text/plain', 'Cookie': ""}
    STANDARD_TIMEFORMAT = {"datetimeformat": "datetime"}
    STANDARD_SERIESTYPE = "timeseries"