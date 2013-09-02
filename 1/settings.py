#coding: utf-8

DOMAIN_URL = ""

BAIDU_APP_KEY = ""

try: from settings_local import *
except: pass

#获取周围地址
POSI_SEARCH_POINTS_RADIUS = "http://api.map.baidu.com/place/v2/search?ak=" + BAIDU_APP_KEY + "&output=json&query=%s&scope=2&location=%s,%s&page_size=8&page_num=%s&radius=1000&filter=sort_name:distance"

#获取一个地址的详细信息
POSI_SEARCH_POINTS_DETAIL = "http://api.map.baidu.com/place/v2/detail?uid=%s&ak=" + BAIDU_APP_KEY + "&output=json&scope=2"

#获取团购地址
GROUPON_SEARCH_INFOS = "http://api.map.baidu.com/place/v2/eventsearch?query=%s&event=groupon&location=%s,%s&radius=1000&output=json&page_size=8&ak=" + BAIDU_APP_KEY + "&region=%s&scope=2&&page_num=%s&filter=sort_name:distance"

#一个团购详细信息
GROUPON_DETAIL_SEARCH_INFOS = "http://api.map.baidu.com/place/v2/eventdetail?uid=%s&output=json&ak=" + BAIDU_APP_KEY

#坐标转换成地理位置
GECODER_SEARCH_INFO = "http://api.map.baidu.com/geocoder/v2/?ak=" + BAIDU_APP_KEY + "&location=%s,%s&output=json&pois=0"

#获取一个
POINT_SEARCH_IMAGE_URL = "http://api.map.baidu.com/staticimage?center=%s,%s&markers=%s&width=%s&height=%s&zoom=%s&markerStyles=l,A|m,B|l,C|l,D|m,E|,|l,G|m,H"

#方向接口
ADDRESS_STEP_SEARCH_URL = "http://api.map.baidu.com/direction/v1?mode=%s&origin=%s&destination=%s&region=%s&output=json&ak=" + BAIDU_APP_KEY
