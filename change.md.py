# coding=utf-8
import os
import re
import random
import sys
import time
from datetime import datetime

post_time_data = {}


def write_file(filename, content):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except Exception as e:
            print(e)
    fd = os.open("{}".format(filename), os.O_RDWR | os.O_CREAT)
    os.write(fd, str(content).encode("utf-8"))
    os.close(fd)


def get_file_lines(filename):
    file = open(filename, encoding="utf-8")
    lines = file.readlines()
    file.close()
    return lines


def get_file_content(filename):
    return '\n'.join(get_file_lines(filename))


def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def is_contain_chinese(strs):
    for ch in strs:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def get_post_time(url):
    global post_time_data
    if len(post_time_data) <= 0:

        post_time_list = '''
gmail-can-not-identify-device	1649770883
set-windows-default-email	1648659278
recover-hotmail-email	1648774988
howto-edm-by-sendinblue	1648702416
how-to-prevent-gmail-bans	1648829614
oversea-account-blocked	1648660507
remove-gmail-account	1648775779
email-pay-faq	1648659770
outlook-common-tips	1648658865
register-a-gmail	1648659233
import-gmail-contacts-to-outlook	1649863512
howto-prevent-emails-be-spam	1648660629
how-to-check-gmail-reg-ip	1649770897
outlook-hotmail-question	1649687293
yandex-mail-register-method	1648657277
gmail-change-password	1648660538
reg-gmail-without-phone	1648660675
gmail-account-sale	1648775054
how-to-find-gmail-email	1648659743
how-to-keep-google-voice-account	1648658750
gmail-notice-phone-sms	1646493975
change-gmail-language	1648660968
app-go-outsite	1648660569
amazon-up	1648657820
gmail-vs-outlook-which-better	1649770856
top-gmail-extensions-in-2022	1647208344
top-email-templates-in-2022	1648779608
introduce-yourself-in-email	1648658237
gmail-statistics-trend	1649770837
best-free-bulkemail-providers	1649687264
outlook-hotmail-account-sale	1648783159
howto-bulkemail-email-with-gmail	1649770760
the-best-send-email-time	1648657931
howto-change-gmail-address	1648574426
howto-set-gmail-auto-reply	1648659261
top-youtube-chrome-extensions	1648658606
useful-temp-email-generators	1648658272
how-does-gmail-spam-filter-work	1649770813
create-a-professional-email-address	1648657596
register-outlook-jump-phone-verify	1648910666
register-outlook-without-phonenumber	1650720256
how-to-change-gmail-background	1649761488
top-google-docs-extensions	1649495375
how-to-free-us-phone-number	1649687273
how-to-register-yahoo-email-without-phone-number	1649603139
how-to-register-google-voice	1649687268
how-to-register-whatsapp-without-phone	1649690209
how-to-change-whatsapp-phone-number	1649690659
iphone-backup-whatsapp-2-icloud	1649777945
how-to-recover-permanently-deleted-emails-outlook	1649863922
how-to-recall-sent-email-in-gmail	1649932717
how-to-transfer-contacts-to-gmail	1650379289
get-a-free-google-drive-account	1650026352
listen-whatsapp-audio-without-sender-know	1650030625
add-whatsapp-friends-without-saving-2-contacts	1650083409
how-to-save-whatsapp-photos-to-pc	1650084328
how-to-stop-autoplay-videos-twitter	1650165313
    '''

        post_times = post_time_list.split("\n")
        for line in post_times:
            line = line.strip()
            if len(line) <= 0:
                continue
            url_short, timestamp = list(line.split("\t"))
            post_time_data[url_short] = time.localtime(int(timestamp))

    return post_time_data[url]


if __name__ == '__main__':
    _publish_dir = "./_posts"
    _post_md_dir = "./posts-md"

    file_list = os.listdir(_post_md_dir)
    for _f in file_list:
        if _f.startswith('2022-'):
            continue

        file_path = "{}/{}".format(_post_md_dir, _f)
        lines = get_file_lines(file_path)
        _lines = []

        title = lines[0].replace("# ", "").strip().replace("\n", "")

        del lines[0]

        tmp = 0
        content = "".join(lines)
        content = content.replace("\n\n", "\n").replace("\r\r", "\n")
        pattern = re.compile(r'\[(.*?)\]')

        tags = set()
        _tags = re.findall(pattern, content)
        url = _tags[len(_tags) - 1]
        url = str(url).replace("https://www.henduohao.com/a/", "")

        # if _f.__contains__("如何创建一个属于你的Gmail邮箱"):
        #     pass
        enum_tags = "POP3,Amazon,企业邮箱,临时邮箱,YouTube,Live,Chrome,谷歌邮箱,Twitter,Facebook,Google Voice,IMAP,SMTP,Google,Google Docs,Skype,TextNow,WhatsApp,G​​oogle Drive,Yahoo邮箱,Outlook购买,雅虎邮箱购买,购买亚马逊账号,谷歌账号购买,微软邮箱购买,Live邮箱购买,Gmail,Hotmail,亚马逊账号,Gmail购买,邮箱购买,邮箱批发,跨境电商,邮件营销,EDM,Outlook,Yandex,Aol"
        enum_tags = enum_tags.split(",")
        for _tag in _tags:
            _tag = str(_tag)
            if not enum_tags.__contains__(_tag):
                continue
            tags.add(_tag)

        categories = random.choice(["跨境出海", "邮箱小号", "实战技巧", "实用工具"])
        header = '''---
layout: post  
author: "Martin Lee"  
title:  "{}"  
date:   {} +0800  
permalink: /posts/{}.html  
tags: [{}]  
categories: [{}]  
---
'''

        post_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_prefix = datetime.now().strftime('%Y-%m-%d')
        _post_time = get_post_time(url)
        if _post_time:
            post_time = time.strftime("%Y-%m-%d %H:%M:%S", _post_time)
            date_prefix = time.strftime("%Y-%m-%d", _post_time)

        generate_md = "{}/{}-{}.md".format(_publish_dir, date_prefix, url)
        header = header.format(title, post_time, url, ','.join(tags), categories)

        content = header + content
        write_file(generate_md, content)
        print(generate_md)
        # print(content)
