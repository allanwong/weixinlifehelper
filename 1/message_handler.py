#coding: utf-8
import time, baidu_map_api
import weixin_message
import mysql_utils
import json, urllib, urllib2

class MessageHandlerStore(object):
    @staticmethod
    def create_message_handler(message):
        self_module = __import__("message_handler")
        class_name = "%sMessageHandler" % message.message_type.capitalize()
        return getattr(self_module, class_name)(message)

class MessageHandler(object):
    def __init__(self, message): self.message = message

class LocationMessageHandler(MessageHandler):
    def save_location_message(self):
        db = mysql_utils.conn_open()
        cursor = db.cursor()
        cursor.execute("SELECT count(*) FROM `members` WHERE `from_username` = '%s'" % self.message.from_user_name)
        rows = cursor.fetchall()
        if rows[0][0] == 0: 
            to_sql = """
            INSERT INTO `members` (`from_username`, `location_x`, `location_y`) VALUES ('%s', '%s', '%s') 
            """ % (self.message.from_user_name, self.message.location_x, self.message.location_y)
        else:
            to_sql = """
            UPDATE `members` SET `location_x` = '%s', `location_y` = '%s' where  `from_username`='%s'
            """ % (self.message.location_x, self.message.location_y, self.message.from_user_name)
        cursor.execute(to_sql)
        cursor.close()
        db.commit()
        db.close()

    def handle(self):
        self.save_location_message()

class TextMessageHandler(MessageHandler):
    def __init__(self, message):
        MessageHandler.__init__(self, message)
        self.location_info = self.get_user_location()

    def life_help(self):
        items = [
            [["Title", "生活助手帮助信息"],
             ["Description", ""],
             ["PicUrl", ""],
             ["Url", ""]],
            [["Title", "在利用下面的功能之前，请确保你利用微信的“位置”按钮，上传你当前的位置。"], 
             ["Description", ""],
             ["PicUrl", ""],
             ["Url", ""]],
            [["Title", "周边地址信息服务:\n您可以以这样的格式来获取周边的信息:查<关键字> <页数>\n(如果是第一页的话可以省略 1)\n比如：查酒店、查美食 2"], 
             ["Description", ""],
             ["PicUrl", ""],
             ["Url", ""]],
            [["Title", "周边团购信息服务:\n您可以以这样的格式来获取周边的信息:团<关键字>/<页数>\n(如果是第一页同理可以省略 1)\n比如：团美食、团酒店 3"], 
             ["Description", ""],
             ["PicUrl", ""],
             ["Url", ""]]
        ]
        return weixin_message.WeixinNewsMessage.create_news_reply_message(
            self.message.to_user_name, self.message.from_user_name, items
        )        
    
    def create_text_message(self, content):
        return weixin_message.WeixinTextMessage.create_text_reply_message(
            self.message.to_user_name, self.message.from_user_name, content
        )

    def get_user_location(self):
        info = mysql_utils.get_info_from_db(
            "SELECT * FROM `members` WHERE `from_username` = '%s'" % self.message.from_user_name
        )
        return info
        
    def search_addresses(self, key):
        if not self.location_info: return self.create_text_message("你如果需要查询一些东西的话，请先上传你的位置信息吧")
        lat, lng = float(self.location_info[0][2]), float(self.location_info[0][3])
        try: key, page = key.split(' ')
        except: key, page = key, 1 
        items = baidu_map_api.map_poi_search(key, lat, lng, int(page)-1)
        return weixin_message.WeixinNewsMessage.create_news_reply_message(
            self.message.to_user_name, self.message.from_user_name, items
        )

    def search_groupon(self, key):
        if not self.location_info: 
            return self.create_text_message("你如果需要查询一些东西的话，请先上传你的位置信息吧")
        lat, lng = float(self.location_info[0][2]), float(self.location_info[0][3])
        city = baidu_map_api.gecoder_search(lat, lng)
        try: key, page = key.split(' ')
        except: key, page = key, 1
        items = baidu_map_api.groupon_search(key, lat, lng, city, int(page)-1)
        return weixin_message.WeixinNewsMessage.create_news_reply_message(
            self.message.to_user_name, self.message.from_user_name, items
        )
        
    def handle(self):
        content = self.message.content.strip()
        if content.startswith(u"查"): return self.search_addresses(content[1:].strip())
        elif content.startswith(u"团"): return self.search_groupon(content[1:].strip())
        else: return self.life_help()
