import os
import random
import shutil

from django.contrib.sites import requests
from django.http import HttpResponse



class dataGet:
    def __init__(self, path, start, end):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        }
        self.start = start
        self.end = end
        temp = random.randint(1, 1000)
        self.path = path + "/" + str(temp)
        if os.path.exists(self.path):
            os.remove(self.path)
        os.mkdir(self.path)
        self.file_path = path

    def Get(self, url):
        res = requests.get(url, headers=self.header)
        if res.status_code == 200:
            return res.text
        return False

    def POST(self, url, data):
        res = requests.post(url, headers=self.header, json=data)

        if res.status_code == 200:
            return res.text
        return False

    def get_list(self):
        url = "https://anli.court.gov.cn/sfalw/search/alk/aljs/search"
        start = 0
        while 1:
            data = {"advs": [{"cpksrq": self.start, "cpjsrq": self.end, "ajlb": {"words": "", "type": "", "name": ""},
                              "ayfb": {"words": "", "type": "", "name": ""},
                              "bgfb": {"words": "", "type": "", "name": ""},
                              "jylb": {"words": "", "type": "", "name": ""},
                              "bgfl": {"words": "", "type": "", "name": ""},
                              "ayfl": {"words": "", "type": "", "name": ""}}], "from": start, "limit": 10, "query": [],
                    "sort": 0, "pxfs": 1}
            info = self.POST(url, data)
            if not info:
                break
            jsonData = json.loads(info)
            parseDatas = jsonData["data"]["dataItem"]["resultList"]
            if len(parseDatas) == 0:
                break
            for i in parseDatas:
                self.detail(i['id'])
            start += 10
            if start > 40:
                break
        self.zip_files()
        return True

    def detail(self, id):
        url = 'https://anli.court.gov.cn/sfalw/case/altx/cases/detail/{0}'.format(str(id))

        info = self.Get(url)
        if not info:
            return
        data = json.loads(info)
        text = ''
        try:
            data = data["data"]
            data = data["dataItem"]
            text += data["name"] + ','
            text += data["tqsj"] + ','
            text += data["userName"] + ','
            text += data["tjly"] + ','
            text += data["ajBasicInfo"]['am'] + ','
            text += data["ajBasicInfo"]['ah'] + ','
            text += data["ajBasicInfo"]['ajlb'] + ','
            text += data["ajBasicInfo"]['ay'] + ','
            text += data["ajBasicInfo"]['slfy'] + ','
            text += data["ajBasicInfo"]['cprq'] + ','
            try:
                text += data["gjc"] + ','
            except:
                pass
            text += data["jbaq"] + ','
            text += data["zyjd"] + ','
            text += data["cpyd"] + ','
            self.write(data['name'], text)
        except:
            pass

def DataGet(request):
    start = request.POST.get('start')
    end = request.POST.get('end')
    l = dataGet("static/getData", start.split("T")[0], end.split("T")[0])
    l.get_list()
    file = open("static/getData/data.zip", 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={0}'.format('data.zip')
    return response