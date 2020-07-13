#!/usr/bin/python
# coding:utf8
import sys
import hashlib
import os
import urllib2
import json

# import time
# import urllib
# import socket

# import pickle to store lists
# noinspection PyBroadException
try:
    from cPickle import load, dump
except ImportError:
    from pickle import load, dump

# Initial the Python coding
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

dbPath = str(os.path.split(os.path.realpath(sys.argv[0]))[0]) + '/md5sum.db'
corpId = 'xxxid' //把xxx替换成微信告警接口的ID
corpSecret = 'xxxsec' //把xxxsec替换成微信告警接口的密码


def md5_check_sum(file_path):
    with open(file_path, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def get_token(corp_id, corp_secret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corp_id + '&corpsecret=' + corp_secret
    try:
        token_file = urllib2.urlopen(gettoken_url)
    except urllib2.HTTPError as e:
        print e.code
        print e.read().decode("utf8")
        sys.exit()
    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token


def sending_data(access_token, content):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "touser": "xxxxxxx",
        "toparty": "1",
        "msgtype": "text",
        "agentid": "1",
        "text": {
            "content": content
        },
        "safe": "0"
    }
    send_data = json.dumps(send_values, ensure_ascii=False)
    send_request = urllib2.Request(send_url, send_data)
    response = json.loads(urllib2.urlopen(send_request).read())
    print str(response)


def build_db(prefix, checklist):
    lines = open(checklist)
    db_dict = {}
    for line in lines:
        line = str(line.strip('\n'))
        full_filename = prefix + line
        if not os.path.exists(full_filename):
            print "file no exist."
            pass
        else:
            db_dict[line] = md5_check_sum(full_filename)
        dump(db_dict, open(dbPath, 'w'), 1)
    lines.close()


def check_files(prefix):
    if not os.path.exists(dbPath):
        print "db is not exist."
        pass
    else:
        db_dicts = load(open(dbPath, 'r'))
        for filename in db_dicts:
            dst_file = prefix + filename
            if not os.path.exists(dst_file):
                print "%s no exist." % filename
                pass
            else:
                dst_md5 = md5_check_sum(dst_file)
                if db_dicts[filename] == dst_md5:
                    pass
                    # print "%s is ok" % file
                else:
                    content = "%s %s => %s" % (dst_file, db_dicts[filename], dst_md5)
                    print content
                    access_token = get_token(corpId, corpSecret)
                    sending_data(access_token, content)



if len(sys.argv) < 2:
    sys.exit('Usage: %s Action(buildDb/checkFiles) Parameter(Directories or Files)' % sys.argv[0])
if sys.argv[1] == 'checkFiles' or sys.argv[1] == 'c':
    check_files(sys.argv[2])
elif sys.argv[1] == 'buildDb' or sys.argv[1] == 'b':
    build_db(sys.argv[2], sys.argv[3])
else:
    sys.exit('Usage: %s Action(buildDb/checkFiles) Parameter(Directory or File)' % sys.argv[0])

