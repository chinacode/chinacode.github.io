# coding=utf-8
import os
import re
import random
import sys

from datetime import datetime


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


if __name__ == '__main__':
    _publish_dir = "./_posts"
    _post_md_dir = "_site/posts-md"

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

        generate_md = "{}/{}-{}.md".format(_publish_dir, date_prefix, url)
        header = header.format(title, post_time, url, ','.join(tags), categories)

        content = header + content
        write_file(generate_md, content)
        print(generate_md)
        # print(content)
