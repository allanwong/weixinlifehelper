#coding: utf-8
import urllib, json, settings

def construct_location_items(results, lat, lng, stype="address"):
    items, location_points = [], ["%s,%s" % (lng, lat),]
    for index, result in enumerate(results):
        location = result["location"]
        telephone = result["telephone"].encode("utf-8") if "telephone" in result else "暂无电话"
        address = result["address"].encode("utf-8") if "address" in result else "暂无地址"
        contact_info = "\n地址:%s\n电话:%s\n" % (address.strip("\n"), telephone.strip("\n"))
        url = "%s%s?uid=%s&origin=%s,%s" % (settings.DOMAIN_URL, stype, result["uid"], lat, lng) if "uid" in result else ""
        try: contact_info += ("共%s个团购" % len(result["events"]))
        except: pass
        try: 
            detail_info = "距离:%s米\n评分:%s" % (
                result["detail_info"]["distance"], 
                result["detail_info"]["overall_rating"].encode("utf-8")
            )
        except: detail_info = ""
        try: purl = urllib.unquote(result["events"][0]["groupon_image"])
        except: purl = ""
        items.append([
            ["Title", chr(66+index) +". " + result["name"].encode("utf-8") + contact_info + detail_info], 
            ["Description", contact_info],
            ["PicUrl", purl],
            ["Url", url]
        ])
        location_points.append(str(location["lng"]) + "," + str(location["lat"]))
    
    pic_url = settings.POINT_SEARCH_IMAGE_URL % (str(lng), str(lat), "%7C".join(location_points), "640", "320", "16")
    url = settings.POINT_SEARCH_IMAGE_URL % (str(lng), str(lat), "%7C".join(location_points), "640", "640", "16")
    items.insert(0, [
        ["Title", "地图标记"], 
        ["Description", "附近周围没有你选择的地点"],
        ["PicUrl", pic_url],
        ["Url", url]
    ])
    return items

def fetch_json_of_api_url(url_str):
    def deco(callback):
        def _(*args, **kwargs):
            url = url_str % tuple(args)
            try: 
                json_result = json.loads(urllib.urlopen(url.encode("utf-8")).read())
                kwargs["json_result"] = json_result
                return callback(*args, **kwargs)
            except Exception, e: return []
        return _
    return deco

@fetch_json_of_api_url(settings.POSI_SEARCH_POINTS_RADIUS)
def map_poi_search(key, lat, lng, page, json_result=None):
    return construct_location_items(json_result["results"], lat, lng)

@fetch_json_of_api_url(settings.GROUPON_SEARCH_INFOS)    
def groupon_search(key, lat, lng, region, page, json_result=None):
    return construct_location_items(json_result["results"], lat, lng, "groupon")

@fetch_json_of_api_url(settings.POSI_SEARCH_POINTS_DETAIL)
def poi_detail_search(uid, json_result=None): 
    return json_result["result"]

@fetch_json_of_api_url(settings.GROUPON_DETAIL_SEARCH_INFOS)
def groupon_detail_search(uid, json_result=None):
    return json_result["result"]

@fetch_json_of_api_url(settings.GECODER_SEARCH_INFO)
def gecoder_search(lat, lng, json_result=None):
    address_component = json_result["result"]["addressComponent"]
    province, city, district = address_component["province"], address_component["city"], address_component["district"]
    return city

@fetch_json_of_api_url(settings.ADDRESS_STEP_SEARCH_URL)
def address_step_search(mode, origin, destination, origin_region, json_result=None):
    return json_result["result"]
