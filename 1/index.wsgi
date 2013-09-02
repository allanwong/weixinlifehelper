#coding: utf-8 

from bottle import Bottle, run, request, template

import sae, hashlib, urllib, urllib2
import weixin_message, message_handler
import sae.const
import baidu_map_api

app = Bottle()

def check_token_valid(callback):
    def _():
        query_params = request.GET    
        info_sha1 = hashlib.sha1()
        info_sha1.update("".join(sorted([str(query_params.get('nonce')), str(query_params.get("timestamp")), "weixinget"])))
        info_sha1_digest = info_sha1.hexdigest()
        return callback() if query_params.get("signature") == info_sha1_digest else "Are You SB ma?"
    return _

@app.route('/weixin', method="get")
@check_token_valid
def weixin_get(): return request.GET.get("echostr")


@app.route('/weixin', method="post")
@check_token_valid
def weixin_post():     
    message_store = weixin_message.WeixinMessageStore(request.body.read())
    message = message_store.create_message()    
    real_message_handler = message_handler.MessageHandlerStore.create_message_handler(message)
    return real_message_handler.handle()

@app.route('/address', method="get")
def address_detail():    
    center = request.GET.get("origin")
    lat, lng = center.split(",")
    result = baidu_map_api.poi_detail_search(request.GET.get("uid"))
    city = baidu_map_api.gecoder_search(lat, lng)
    destination = str(result["location"]["lat"]) + "," + str(result["location"]["lng"])
    line_result = baidu_map_api.address_step_search(request.GET.get("mode", "walking"), center, destination, city)
    return template("address_detail", result=result, line_result=line_result, origin="%s,%s" % (lng, lat))

@app.route('/groupon', message="get")
def groupon_detail():
    result = baidu_map_api.groupon_detail_search(request.GET.get("uid"))
    return template("groupon_detail", result=result)

application = sae.create_wsgi_app(app)
