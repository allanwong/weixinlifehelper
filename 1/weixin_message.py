#coding: utf-8

import xml.dom.minidom, time

class WeixinMessageStore(object):
    def __init__(self, xml_string):
        print xml_string
        self.root = xml.dom.minidom.parseString(xml_string).documentElement
        self.message_type = self.root.getElementsByTagName("MsgType")[0].firstChild.wholeText
        
    def create_message(self):
        class_name = "Weixin%sMessage" % self.message_type.capitalize()
        self_module = __import__('weixin_message')
        return getattr(self_module, class_name)(self.root, self.message_type)

class WeixinMessage(object):
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'xml', None)

    def __init__(self, root, message_type):
        self.root = root        
        self.message_type = message_type
        self.from_user_name = self._get_text_from_element("FromUserName")
        self.to_user_name = self._get_text_from_element("ToUserName")

    def _get_text_from_element(self, key):
        try: return self.root.getElementsByTagName(key)[0].firstChild.wholeText
        except: return ""

    @staticmethod
    def create_reply_common_message(text_message_infos, message_type):
        #创建一个公共的回复消息xml
        root = WeixinMessage.dom.createElement('xml')
        text_message_infos["MsgType"] = message_type
        for key, item in text_message_infos.items():
            element = WeixinMessage.dom.createElement(key)
            element.appendChild(WeixinMessage.dom.createCDATASection(str(item)))
            root.appendChild(element)
        return root

class WeixinTextMessage(WeixinMessage):
    def __init__(self, root, message_type):
        WeixinMessage.__init__(self, root, message_type)
        self.content = self._get_text_from_element("Content")

    @staticmethod
    def create_text_reply_message(from_user_name, to_user_name, content):
        dicts = {
            "ToUserName": to_user_name,
            "FromUserName": from_user_name,
            "CreateTime": int(time.time()),
            "Content": content
        }
        root = WeixinMessage.create_reply_common_message(dicts, "text")
        return root.toxml()


class WeixinLocationMessage(WeixinMessage):
    def __init__(self, root, message_type):
        WeixinMessage.__init__(self, root, message_type)        
        self.location_x = self._get_text_from_element("Location_X")
        self.location_y = self._get_text_from_element("Location_Y")
        self.location_label = self._get_text_from_element("Label")
        

class WeixinNewsMessage(WeixinMessage):
    @staticmethod
    def create_news_reply_message(from_user_name, to_user_name, items):
        dicts = {
            "ToUserName": to_user_name,
            "FromUserName": from_user_name,
            "CreateTime": int(time.time()),
            "ArticleCount": int(len(items))
        }
        root = WeixinMessage.create_reply_common_message(dicts, "news")
        articles = WeixinMessage.dom.createElement("Articles")        
        for point in items:
            item = WeixinMessage.dom.createElement("item")
            for index, w_item in enumerate(point):
                element = WeixinMessage.dom.createElement(w_item[0])
                element.appendChild(WeixinMessage.dom.createCDATASection(str(w_item[1])))
                item.appendChild(element)
            articles.appendChild(item)
        root.appendChild(articles)
        return root.toxml()
