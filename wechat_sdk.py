# -*- coding:utf-8 -*-
import json
import requests
from conf import CORPID, CORPSECRET

class ErrorCode(object):
    SUCCESS = 0


class WeChatEnterprise(object):

    def __init__(self, agentid=1):
        """
            document address: http://qydev.weixin.qq.com/wiki/index.php?title=%E9%A6%96%E9%A1%B5
        """
        self.corpid = CORPID
        self.corpsecret = CORPSECRET
        self.agentid = agentid
        self.url_prefix = "https://qyapi.weixin.qq.com/cgi-bin"
        self.access_token = self.__get_access_token()

    def __get_access_token(self):
        # access_token 有效期为 7200秒
        # todo 缓存access_token
        url = "%s/gettoken?corpid=%s&corpsecret=%s" % (self.url_prefix, self.corpid, self.corpsecret)
        res = requests.get(url)
        access_token = res.json().get("access_token")
        return access_token

    @staticmethod
    def __response(res):
        errcode = res.get("errcode")
        # errmsg = res.get("errmsg")
        if errcode is ErrorCode.SUCCESS:
            return True, res
        else:
            return False, res

    def __post(self, url, data):
        res = requests.post(url, data=json.dumps(data).decode('unicode-escape').encode("utf-8")).json()
        return self.__response(res)

    def __get(self, url):
        res = requests.get(url).json()
        return self.__response(res)

    def __post_file(self, url, media_file):
        res = requests.post(url, file=media_file).json()
        return self.__response(res)

    # 部门管理
    def create_department(self, name, parentid=1, order=None):
        """
            创建部门
            name    : 部门名称。长度限制为1~64个字符
            parentid: 父亲部门id。根部门id为1
            order   : 在父部门中的次序。从1开始，数字越大排序越靠后
        """
        url = "%s/department/create?access_token=%s" % (self.url_prefix, self.access_token)
        data = {
            "name": name,
            "parentid": parentid,
        }
        if order is not None:
            data["order"] = order
        status, res = self.__post(url, data)
        return status, res

    def update_department(self, department_id, **kwargs):
        """
            更新部门

            参数	必须	说明
            access_token	是	调用接口凭证
            id	是	部门id
            name	否	更新的部门名称。长度限制为1~64个字符。修改部门名称时指定该参数
            parentid	否	父亲部门id。根部门id为1
            order	否	在父部门中的次序。从1开始，数字越大排序越靠后
        """
        url = "%s/department/update?access_token=%s" % (self.url_prefix, self.access_token)
        data = {
            "id": department_id,
        }
        data.update(kwargs)
        status, res = self.__post(url, data)
        return status, res

    def delete_department(self, department_id):
        """
            删除部门
            参数	必须	说明
            access_token	是	调用接口凭证
            id	是	部门id。（注：不能删除根部门；不能删除含有子部门、成员的部门）
        """
        url = "%s/department/delete?access_token=%s&id=%s" % (self.url_prefix, self.access_token, department_id)
        status, res = self.__get(url)
        return status, res

    def get_department_list(self):
        """
            获取部门列表
            参数	必须	说明
            access_token	是	调用接口凭证
        """
        url = "%s/department/list?access_token=%s" % (self.url_prefix, self.access_token)
        status, res = self.__get(url)
        return status, res

    # 成员管理
    def create_user(self, data):
        """
            创建用户
            参数	必须	说明
            access_token	是	调用接口凭证
            userid	是	员工UserID。对应管理端的帐号，企业内必须唯一。长度为1~64个字符
            name	是	成员名称。长度为1~64个字符
            department	是	成员所属部门id列表。注意，每个部门的直属员工上限为1000个
            position	否	职位信息。长度为0~64个字符
            mobile	否	手机号码。企业内必须唯一，mobile/weixinid/email三者不能同时为空
            email	否	邮箱。长度为0~64个字符。企业内必须唯一
            weixinid	否	微信号。企业内必须唯一。（注意：是微信号，不是微信的名字）
            extattr	否	扩展属性。扩展属性需要在WEB管理端创建后才生效，否则忽略未知属性的赋值
        """
        url = "%s/user/create?access_token=%s" % (self.url_prefix, self.access_token)
        if data.get("userid") and data.get("name"):
            status, res = self.__post(url, data)
        else:
            status = False
            res = u"userid 或者 name 为空"
        return status, res

    def update_user(self, userid, **kwargs):
        """
            更新成员
            参数	必须	说明
            access_token	是	调用接口凭证
            userid	是	员工UserID。对应管理端的帐号，企业内必须唯一。长度为1~64个字符
            name	否	成员名称。长度为0~64个字符
            department	否	成员所属部门id列表。注意，每个部门的直属员工上限为1000个
            position	否	职位信息。长度为0~64个字符
            mobile	否	手机号码。企业内必须唯一，mobile/weixinid/email三者不能同时为空
            email	否	邮箱。长度为0~64个字符。企业内必须唯一
            weixinid	否	微信号。企业内必须唯一。（注意：是微信号，不是微信的名字）
            enable	否	启用/禁用成员。1表示启用成员，0表示禁用成员
            extattr	否	扩展属性。扩展属性需要在WEB管理端创建后才生效，否则忽略未知属性的赋值
        """
        url = "%s/user/update?access_token=%s" % (self.url_prefix, self.access_token)
        data = {"userid": userid}
        data.update(kwargs)
        status, res = self.__post(url, data=data)
        return status, res

    def delete_user(self, userid):
        """
            删除成员
            参数	必须	说明
            access_token	是	调用接口凭证
            userid	是	员工UserID。对应管理端的帐号
        """
        url = "%s/user/delete?access_token=%s&userid=%s" % (self.url_prefix, self.access_token, userid)
        status, res = self.__get(url)
        return status, res

    def multi_delete_user(self, useridlist):
        """
            批量删除成员
            参数	必须	说明
            access_token	是	调用接口凭证
            useridlist	是	员工UserID列表。对应管理端的帐号
        """
        url = "%s/user/batchdelete?access_token=%s" % (self.url_prefix, self.access_token)
        data = {"useridlist": useridlist}
        status, res = self.__post(url, data=data)
        return status, res

    def get_user(self, userid):
        """
            获取成员
            参数	必须	说明
            access_token	是	调用接口凭证
            userid	是	员工UserID。对应管理端的帐号

        """
        url = "%s/user/get?access_token=%s&userid=%s" % (self.url_prefix, self.access_token, userid)
        status, res = self.__get(url)
        return status, res

    def get_users_in_department(self, department_id, fetch_child=0, status=0):
        """
            获取部门成员
            参数	必须	说明
            access_token	是	调用接口凭证
            department_id	是	获取的部门id
            fetch_child	否	1/0：是否递归获取子部门下面的成员
            status	否	0获取全部员工，1获取已关注成员列表，2获取禁用成员列表，4获取未关注成员列表。status可叠加
        """
        url = "%s/user/simplelist?access_token=%s&department_id=%s&fetch_child=%s&status=%s" \
              % (self.url_prefix, self.access_token, department_id, fetch_child, status)
        status, res = self.__get(url)
        return status, res

    def get_users_in_department_detail(self, department_id, fetch_child=0, status=0):
        """
            获取部门成员(详情)
            参数	必须	说明
            access_token	是	调用接口凭证
            department_id	是	获取的部门id
            fetch_child	否	1/0：是否递归获取子部门下面的成员
            status	否	0获取全部员工，1获取已关注成员列表，2获取禁用成员列表，4获取未关注成员列表。status可叠加
        """
        url = "%s/user/list?access_token=%s&department_id=%s&fetch_child=%s&status=%s" \
              % (self.url_prefix, self.access_token, department_id, fetch_child, status)
        status, res = self.__get(url)
        return status, res

    def invite_attention_to_user(self, userid, invite_tips=None):
        """
            邀请用户关注
            参数	必须	说明
            access_token	是	调用接口凭证
            userid	是	用户的userid
            invite_tips	否	推送到微信上的提示语（只有认证号可以使用）。当使用微信推送时，该字段默认为“请关注XXX企业号”，邮件邀请时，该字段无效。
        """
        url = "%s/invite/send?access_token=%s" % (self.url_prefix, self.access_token)
        data = {
            "userid": userid
        }
        if invite_tips is not None:
            data["invite_tips"] = invite_tips
        status, res = self.__post(url, data)
        return status, res

    # 管理标签
    def create_tag(self, tagname):
        """
            创建标签
            参数	必须	说明
            access_token	是	调用接口凭证
            tagname	是	标签名称。长度为1~64个字符，标签不可与其他同组的标签重名，也不可与全局标签重名
        """
        url = "%s/tag/create?access_token=%s" % (self.url_prefix, self.access_token)
        data = {"tagname": tagname}
        status, res = self.__post(url, data)
        return status, res

    def update_tag(self, tagid, tagname):
        """
            更新标签名字
            参数	必须	说明
            access_token	是	调用接口凭证
            tagid	是	标签ID
            tagname	是	标签名称。长度为1~64个字符，标签不可与其他同组的标签重名，也不可与全局标签重名
        """
        url = "%s/tag/update?access_token=%s" % (self.url_prefix, self.access_token)
        data = {"tagid": tagid, "tagname": tagname}
        status, res = self.__post(url, data)
        return status, res

    def delete_tag(self, tagid):
        """
            删除标签
            参数	必须	说明
            access_token	是	调用接口凭证
            tagid	是	标签ID
        """
        url = "%s/tag/delete?access_token=%s&tagid=%s" % (self.url_prefix, self.access_token, tagid)
        status, res = self.__get(url)
        return status, res

    def get_user_from_tag(self, tagid):
        """
            获取标签成员
            参数	必须	说明
            access_token	是	调用接口凭证
            tagid	是	标签ID
        """
        url = "%s/tag/get?access_token=%s&tagid=%s" % (self.url_prefix, self.access_token, tagid)
        status, res = self.__get(url)
        return status, res

    def add_users_to_tag(self, tagid, userlist, partylist):
        """
            增加标签成员
            参数	必须	说明
            access_token	是	调用接口凭证
            tagid	是	标签ID
            userlist	否	企业员工ID列表，注意：userlist、partylist不能同时为空
            partylist	否	企业部门ID列表，注意：userlist、partylist不能同时为空
        """
        url = "%s/tag/addtagusers?access_token=%s" % (self.url_prefix, self.access_token)
        data = {"tagid": tagid, "userlist": userlist, "partylist": partylist}
        status, res = self.__post(url, data=data)
        return status, res

    def delete_user_in_tag(self, tagid, userlist, partylist):
        """
            删除标签成员
            参数	必须	说明
            access_token	是	调用接口凭证
            tagid	是	标签ID
            userlist	否	企业员工ID列表，注意：userlist、partylist不能同时为空
            partylist	否	企业部门ID列表，注意：userlist、partylist不能同时为空
        """
        url = "%s/tag/deltagusers?access_token=%s" % (self.url_prefix, self.access_token)
        data = {"tagid": tagid, "userlist": userlist, "partylist": partylist}
        status, res = self.__post(url, data=data)
        return status, res

    def get_tag_list(self):
        """
            获取标签列表
            参数	必须	说明
            access_token	是	调用接口凭证
        """
        url = "%s/tag/list?access_token=%s" % (self.url_prefix, self.access_token)
        status, res = self.__get(url)
        return status, res

    # 管理多媒体文件
    def upload_media(self, media_type, media_file):
        """
            上传媒体文件
            参数	必须	说明
            access_token	是	调用接口凭证
            type	是	媒体文件类型，分别有图片（image）、语音（voice）、视频（video），普通文件(file)
            media	是	form-data中媒体文件标识，有filename、filelength、content-type等信息
        """
        url = "%s/media/upload?access_token=%s&type=%s" % (self.url_prefix, self.access_token, media_type)
        data = {"media": media_file}
        status, res = self.__post_file(url, data)
        return status, res

    def get_media(self, media_id):
        """
            获取媒体文件
            参数	必须	说明
            access_token	是	调用接口凭证
            media_id	是	媒体文件id
        """
        url = "%s/media/get?access_token=%s&media_id=%s" % (self.url_prefix, self.access_token, media_id)
        media_file = requests.get(url)
        return media_file

    # 发送消息
    def send_msg_to_user(self, content, touser=None, toparty=None, totag=None, safe=0, msgtype="text", **kwargs):
        """
            发送消息到用户
            text消息
                参数	必须	说明
                touser	否	员工ID列表（消息接收者，多个接收者用‘|’分隔）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
                toparty	否	部门ID列表，多个接收者用‘|’分隔。当touser为@all时忽略本参数
                totag	否	标签ID列表，多个接收者用‘|’分隔。当touser为@all时忽略本参数
                msgtype	是	消息类型，此时固定为：text
                agentid	是	企业应用的id，整型。可在应用的设置页面查看
                content	是	消息内容
                safe	否	表示是否是保密消息，0表示否，1表示是，默认0
                其他消息参考： http://qydev.weixin.qq.com/wiki/index.php?
                    title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
        """
        url = "%s/message/send?access_token=%s" % (self.url_prefix, self.access_token)
        data = {
            "safe": safe,
            "msgtype": msgtype,
            "agentid": self.agentid
        }
        if msgtype == "text":
            data["text"] = {"content": content}
        if msgtype == "image":
            data["image"] = {"media_id": kwargs.get("media_id")}
        if msgtype == "voice":
            data["voice"] = {"media_id": kwargs.get("media_id")}
        if msgtype == "video":
            data["video"] = {
                "media_id": kwargs.get("media_id"),
                "title": kwargs.get("title"),
                "description": kwargs.get("description")
            }
        if msgtype == "file":
            data["file"] = {
                "media_id": kwargs.get("media_id")
            }
        if msgtype == "news":
            #   {
            #       "articles":[
            #           {
            #               "title": "Title",
            #               "description": "Description",
            #               "url": "URL",
            #               "picurl": "PIC_URL"
            #           },
            #           {
            #               "title": "Title",
            #               "description": "Description",
            #               "url": "URL",
            #               "picurl": "PIC_URL"
            #           }
            #       ]
            #   }
            data["news"] = kwargs
        if msgtype == "mpnews":
            #{
            #   "articles":[
            #       {
            #           "title": "Title",
            #           "thumb_media_id": "id",
            #           "author": "Author",
            #           "content_source_url": "URL",
            #           "content": "Content",
            #           "digest": "Digest description",
            #           "show_cover_pic": "0"
            #       },
            #       {
            #           "title": "Title",
            #           "thumb_media_id": "id",
            #           "author": "Author",
            #          "content_source_url": "URL",
            #           "content": "Content",
            #           "digest": "Digest description",
            #           "show_cover_pic": "0"
            #       }
            #   ]
            #}
            data["mpnews"] = kwargs

        if touser is None:
            to_user = "@all"
        else:
            to_user = '|'.join(touser)
        data["touser"] = to_user
        if toparty is not None:
            data["toparty"] = toparty

        if totag is not None:
            data["totag"] = totag
        status, res = self.__post(url, data)
        return status, res

    # 二次验证
    def second_validation(self, userid):
        """
            二次验证
            参数	必须	说明
            access_token	是	调用接口凭证
            userid	是	员工UserID
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/authsucc?access_token=%s&userid=%s" \
              % (self.access_token, userid)
        status, res = self.__get(url)
        return status, res