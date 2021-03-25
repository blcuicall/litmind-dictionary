from flask import Flask, jsonify, request
import random
import hashlib
import json

from common.utils import gen_special_img, get_captcha_text
from common.email_utils import send_email
from common.response_bean import ResponseBean, CodeConst
from common.base_handler import BaseHandler
from common.utils import clean_space
from common.utils import index_of_str
from common.utils import deleteFullpointOfChinaExplain
import sys
import tornado.web

from server.home_server import HomeService
import requests
from corenlp_client import CoreNLP

sys.path.append('../')


class HomeSearchHandler(BaseHandler):
    homeService = HomeService()

    def post(self):

        # 获取参数
        param = json.loads(self.request.body.decode('utf-8'))
        print(param)

        # 参数为空 textType  inputExample  inputWord
        if param['inputWord'].strip() == '' or param['inputExample'].strip() == '' or param['textType'].strip() == '':
            result = ResponseBean.set_status_code(CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            self.write(json.dumps(result, ensure_ascii=False))
            return

        # 将参数封装成元组形式
        #  input_data 为列表，列表中每项为 (词语, 例句) 二元组
        #     input_data = [
        #                    ('investigate', 'The FBI has been called in to investigate.')
        #                   ]

        paramTuple = (param['inputWord'], param['inputExample'])
        print(type(paramTuple))
        paramList = [paramTuple]
        paramData = {"param": paramList}
        print(paramData)

        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        # 1. 对传入的例句进行分词

        # 1.1，判断 输入的词 是否在这个列表中
        # 如果在 就进入下一步，不在 就直接返回提示 "输入的词语必须在例句中"

        # 1.2，判断 输入的词 是否是人名，如果是，就直接按照表格返回结果

        spicleNameDict = {

            "PERSON": {"zh": "姓名", "en": "Name"},
            "STATE_OR_PROVINCE": {"zh": "州或省", "en": "State or province"},
            "CITY": {"zh": "城市名", "en": "City"},
            "GPE": {"zh": "地名", "en": "Location"},
            "COUNTRY": {"zh": "国家名", "en": "Country"},
            "LOCATION": {"zh": "地名", "en": "Location"},
            "ORGANIZATION": {"zh": "组织或机构名", "en": "Organization"},
            "NUMBER": {"zh": "数字", "en": "Number"},
            "ORDINAL": {"zh": "序数词", "en": "Ordinal."},
            "PERCENT": {"zh": "百分比", "en": "Percent"},
            "DATE": {"zh": "日期", "en": "Date"},
            "TIME": {"zh": "时间", "en": "Time"}
        }
        # "1" 中中 "3" 英英 ：调齐楠的模型        "2" 中英 调存良的模型
        lastData = []
        spicleNameStr = ""
        if param['textType'] == "2":
            # 1 先分词
            with CoreNLP(url="http://202.112.194.61:8085/", lang="zh") as annotator:
                begSeg_s = annotator.tokenize(param['inputWord'])
                begSeg_s = begSeg_s[0]

                # 2 再循环调模型
                allData = []
                for segCi in begSeg_s:
                    curCiDict = {}
                    # 获取 中英 例句
                    curCiDict = {}
                    # 获取 中文例句
                    # data = json.dumps({"word":segCi, "page_size":10, "page_off_set":1})
                    # r = requests.post(url="http://39.98.52.179:8685/word/getWordSentenceExample", data=data)
                    exampleParamData = {}
                    exampleParamData.setdefault("word", segCi)
                    exampleParamData.setdefault("lang", "zh")
                    r = requests.post('http://127.0.0.1:6889/api/ExampleSearch', data=exampleParamData)
                    exampleResult = json.loads(r.content)

                    if len(exampleResult) == 0:
                        exampleResult.append({"contentQian": "暂无例句"})
                        curCiDict.setdefault("examples", exampleResult)
                    else:
                        lastExexamples = []
                        for exmStr in exampleResult:

                            # ret = clean_space(ret)
                            tpmStr = exmStr["content"]
                            tpmStr = clean_space(tpmStr)
                            index = index_of_str(tpmStr, segCi)[0]
                            ciLen = len(segCi)
                            strOne = tpmStr[0:index]
                            strTwo = tpmStr[index + ciLen:]
                            lastExampleStr = strOne + "<span>" + segCi + "</span>" + strTwo

                            sourceStr = ""
                            if exmStr["source"]:
                                sourceStr = exmStr["source"]
                            else:
                                sourceStr = "书名：暂无"
                            example = {
                                "content": lastExampleStr,
                                "contentQian": strOne,
                                "contentZhong": segCi,
                                "contentHou": strTwo,
                                "source": sourceStr
                            }
                            lastExexamples.append(example)
                        curCiDict.setdefault("examples", lastExexamples)

                    paramTuple = (segCi, param['inputExample'])
                    paramList = [paramTuple]
                    paramData = {"param": paramList}
                    anno = annotator.annotate(param['inputExample'])
                    seg_s = annotator.tokenize(segCi)
                    seg_l = annotator.tokenize(param['inputExample'])

                    seg_s = " ".join(seg_s[0])
                    seg_l = " ".join(seg_l[0])
                    isIn = param['inputExample'].find(segCi)
                    print("是否在例句中#################3")
                    print(isIn)
                    # 判断是否在例句中
                    if isIn != -1:
                        print("在例句中")
                        # 判断是否是 命名实体，是就直接返回，不是就调模型
                        namedEntityList = anno.entities[0]
                        print(namedEntityList)
                        if len(namedEntityList):
                            print("有命名实体")
                            wordIsEntity = 0  # 看命名实体中是否有 输入的词
                            for tem in namedEntityList:
                                if segCi == tem["text"]:
                                    print(tem["text"])
                                    print(tem["ner"])
                                    spicleNameStr = tem["ner"]
                                    if spicleNameStr in spicleNameDict.keys():
                                        curCiDict.setdefault("explain", segCi)
                                        curCiDict.setdefault("explain2", spicleNameDict[spicleNameStr]["en"])
                                        allData.append(curCiDict)
                                        print(lastData)
                                        wordIsEntity = 1  # 1 代表有
                                        break;
                            if wordIsEntity == 0:
                                print("不是---命名实体")
                                paramData.setdefault("language", "zh")
                                r = requests.post('http://202.112.194.62:10119/getdefkcl', data=json.dumps(paramData),
                                                  headers=headers)
                                result = json.loads(r.text)
                                for ret in result:
                                    ret = clean_space(ret)

                                curCiDict.setdefault("explain", segCi)
                                curCiDict.setdefault("explain2", ret)
                                allData.append(curCiDict)

                        else:
                            print("没有---命名实体")
                            paramData.setdefault("language", "zh")
                            r = requests.post('http://202.112.194.62:10119/getdefkcl', data=json.dumps(paramData),
                                              headers=headers)
                            result = json.loads(r.text)

                            curCiDict.setdefault("explain", segCi)
                            curCiDict.setdefault("explain2", result)
                            allData.append(curCiDict)


                    else:
                        print("不---在例句中")
                        # allData.append("notin")
                        curCiDict = {}
                        curCiDict.setdefault("explain", "notin")
                        curCiDict.setdefault("explain2", "")
                        curCiDict.setdefault("examples", [])
                        allData.append(curCiDict)
                        break;

                # print(anno.entities) # openie
                lastData.append(allData)

        elif param['textType'] == "1":

            # 1 先分词
            with CoreNLP(url="http://202.112.194.61:8085/", lang="zh") as annotator:
                begSeg_s = annotator.tokenize(param['inputWord'])
                begSeg_s = begSeg_s[0]

                # 2 再循环调模型
                allData = []
                for segCi in begSeg_s:

                    curCiDict = {}
                    # 获取 中文例句
                    # data = json.dumps({"word":segCi, "page_size":10, "page_off_set":1})
                    # r = requests.post(url="http://39.98.52.179:8685/word/getWordSentenceExample", data=data)
                    exampleParamData = {}
                    exampleParamData.setdefault("word", segCi)
                    exampleParamData.setdefault("lang", "zh")
                    r = requests.post('http://127.0.0.1:6889/api/ExampleSearch', data=exampleParamData)
                    exampleResult = json.loads(r.content)

                    if len(exampleResult) == 0:
                        exampleResult.append({"contentQian": "暂无例句"})
                        curCiDict.setdefault("examples", exampleResult)
                    else:
                        lastExexamples = []
                        for exmStr in exampleResult:

                            # ret = clean_space(ret)
                            tpmStr = exmStr["content"]
                            tpmStr = clean_space(tpmStr)
                            index = index_of_str(tpmStr, segCi)[0]
                            ciLen = len(segCi)
                            strOne = tpmStr[0:index]
                            strTwo = tpmStr[index + ciLen:]
                            lastExampleStr = strOne + "<span>" + segCi + "</span>" + strTwo

                            sourceStr = ""
                            if exmStr["source"]:
                                sourceStr = exmStr["source"]
                            else:
                                sourceStr = "书名：暂无"
                            example = {
                                "content": lastExampleStr,
                                "contentQian": strOne,
                                "contentZhong": segCi,
                                "contentHou": strTwo,
                                "source": sourceStr
                            }
                            lastExexamples.append(example)
                        curCiDict.setdefault("examples", lastExexamples)

                    paramTuple = (segCi, param['inputExample'])
                    paramList = [paramTuple]
                    paramData = {"param": paramList}
                    anno = annotator.annotate(param['inputExample'])
                    seg_s = annotator.tokenize(segCi)
                    seg_l = annotator.tokenize(param['inputExample'])
                    seg_s = " ".join(seg_s[0])
                    seg_l = " ".join(seg_l[0])
                    isIn = param['inputExample'].find(segCi)
                    print("是否在例句中#################3")
                    print(isIn)
                    # 判断是否在例句中
                    if isIn != -1:
                        print("在例句中")
                        # 判断是否是 命名实体，是就直接返回，不是就调模型
                        namedEntityList = anno.entities[0]
                        print("命名实体#################5")
                        print(segCi)

                        if len(namedEntityList):
                            print("有命名实体")
                            wordIsEntity = 0  # 看命名实体中是否有 输入的词
                            for tem in namedEntityList:
                                if segCi == tem["text"]:
                                    spicleNameStr = tem["ner"]
                                    if spicleNameStr in spicleNameDict.keys():
                                        curCiDict.setdefault("explain", segCi)

                                        curCiDict.setdefault("explain2", spicleNameDict[spicleNameStr]["zh"])
                                        allData.append(curCiDict)
                                        wordIsEntity = 1  # 1 代表有
                                        break;
                            if wordIsEntity == 0:
                                print("不是---命名实体")
                                paramData.setdefault("language", "zh")
                                r = requests.post('http://202.112.194.62:10120/getdeffqn', data=json.dumps(paramData),
                                                  headers=headers)
                                result = json.loads(r.text)

                                for ret in result:
                                    ret = clean_space(ret)

                                curCiDict.setdefault("explain", segCi)
                                curCiDict.setdefault("explain2", deleteFullpointOfChinaExplain(ret))
                                allData.append(curCiDict)

                        else:
                            print("没有---命名实体")
                            paramData.setdefault("language", "zh")
                            r = requests.post('http://202.112.194.62:10120/getdeffqn', data=json.dumps(paramData),
                                              headers=headers)
                            result = json.loads(r.text)
                            for ret in result:
                                ret = clean_space(ret)

                            curCiDict.setdefault("explain", segCi)
                            curCiDict.setdefault("explain2", deleteFullpointOfChinaExplain(ret))
                            allData.append(curCiDict)


                    else:
                        print("不---在例句中")
                        curCiDict = {}
                        curCiDict.setdefault("explain", "notin")
                        curCiDict.setdefault("explain2", "")
                        curCiDict.setdefault("examples", [])
                        allData.append(curCiDict)
                        # break;

                lastData.append(allData)


        else:

            # 判断是否在例句中
            if param['inputWord'] in param['inputExample']:
                curCiDict = {}
                exampleParamData = {}
                exampleParamData.setdefault("word", param['inputWord'])
                exampleParamData.setdefault("lang", "en")
                r = requests.post('http://127.0.0.1:6889/api/ExampleSearch', data=exampleParamData)
                exampleResult = json.loads(r.content)
                print("英文例句是##################")

                if len(exampleResult) == 0:
                    exampleResult.append({"contentQian": "There is no example for the time being."})
                    curCiDict.setdefault("examples", exampleResult)
                else:
                    lastExexamples = []
                    for exmStr in exampleResult:
                        index = exmStr["content"].index(param['inputWord'])
                        ciLen = len(param['inputWord'])
                        strOne = exmStr["content"][0:index]
                        strTwo = exmStr["content"][index + ciLen:]
                        lastExampleStr = strOne + "<span>" + param['inputWord'] + "</span>" + strTwo
                        sourceStr = ""
                        if exmStr["source"]:
                            sourceStr = exmStr["source"]
                        else:
                            sourceStr = "None"
                        example = {
                            "content": lastExampleStr,
                            "contentQian": strOne,
                            "contentZhong": param['inputWord'],
                            "contentHou": strTwo,
                            "source": "书名：" + sourceStr
                        }
                        lastExexamples.append(example)
                    curCiDict.setdefault("examples", lastExexamples)
                paramData.setdefault("language", "en")
                r = requests.post('http://202.112.194.62:10120/getdeffqn', data=json.dumps(paramData), headers=headers)
                result = json.loads(r.text)

                curCiDict.setdefault("explain", param['inputWord'])
                curCiDict.setdefault("explain2", result[0])

                lastData.append([curCiDict])
            else:
                print("不---在例句中")
                curCiDict = {}
                curCiDict.setdefault("explain", "notin")
                curCiDict.setdefault("explain2", "")
                curCiDict.setdefault("examples", [])
                lastData.append([curCiDict])

        # 如果没有搜索过  就通过模型获取，然后插入数据库
        ipStr = self.request.headers.get('X-Forwarded-For')
        # ipStr = "127.0.0.1"
        print(ipStr)
        # if ipStr == None or ipStr == " ":
        #     print("ip是空的")
        # else:
        #     print("ip是", ipStr)
        #     ipStr = ipStr.split(',')[0]

        # 组装结果
        lastResArr = []
        print("组装结果 -----###################")

        for tmpData in lastData[0]:

            tmDict = {
                "explain": tmpData["explain"],
                "explain2": tmpData["explain2"],
                "examples": tmpData["examples"]
            }
            lastResArr.append(tmDict)

            # 插入数据库 userId ,wordk,sentence,explain,
            # praise,step_on,modify,type_id,create_time
            expStr = ""
            if tmpData["explain"] == "notin":
                if param['textType'] == "1":
                    expStr = "暂无解释"
                else:
                    expStr = "There is no explanation for the moment."
            else:

                if tmpData["explain2"]:
                    print(tmpData["explain"])
                    print(tmpData["explain2"])
                    expStr = tmpData["explain"] + " " + tmpData["explain2"]
                else:
                    if param['textType'] == "1":
                        expStr = tmpData["explain"] + " " + "暂无解释"
                    else:
                        expStr = tmpData["explain"] + " " + "There is no explanation for the moment."
            self.homeService.insert_userIp(ipStr, param['inputWord'], param['inputExample'], expStr, param['textType'])

        result = ResponseBean.set_data(lastResArr)

        self.write(json.dumps(result, ensure_ascii=False))

        return

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


class HomeSearchGetUserIPHandler(BaseHandler):
    homeService = HomeService()

    def get(self):
        # 获取参数
        data = self.homeService.get_use_ip()

        # 组装结果
        result = ResponseBean.set_data(data)
        self.write(json.dumps(result, ensure_ascii=False))
        return

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


# 点赞 踩 修改意见 更新
class UpdataExplianByUserIPHandler(BaseHandler):
    homeService = HomeService()

    def post(self):
        # 获取参数
        param = json.loads(self.request.body.decode('utf-8'))
        print(param)

        # 参数为空 useripStr,explain,praiseStr,steponStr,modifyStr
        if param['explain'].strip() == '' or param['praiseStr'].strip() == '' or param['steponStr'].strip() == '' or \
                param['modifyStr'].strip() == '':
            result = ResponseBean.set_status_code(CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            self.write(json.dumps(result, ensure_ascii=False))
            return

        # 获取用户ip
        ipStr = self.request.headers.get('X-Forwarded-For')
        # ipStr = "127.0.0.1"
        print(ipStr)
        if ipStr == None or ipStr == " ":
            print("ip是空的")
        else:
            print("ip是", ipStr)
            ipStr = ipStr.split(',')[0]
            data = self.homeService.updata_search_info(ipStr, param['explain'], param['praiseStr'], param['steponStr'],
                                                       param['modifyStr'])
        # 组装结果
        result = ResponseBean.set_data(data)
        self.write(json.dumps(result, ensure_ascii=False))
        return

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


# 反馈意见
class FeedbackByUserIPHandler(BaseHandler):
    homeService = HomeService()

    def post(self):
        # 获取参数
        param = json.loads(self.request.body.decode('utf-8'))
        print(param)

        # 参数为空 feedStr
        if param['feedStr'].strip() == '':
            result = ResponseBean.set_status_code(CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            self.write(json.dumps(result, ensure_ascii=False))
            return

        # 获取用户ip
        ipStr = self.request.headers.get('X-Forwarded-For')
        # ipStr = "127.0.0.1"
        print(ipStr)
        if ipStr == None or ipStr == " ":
            print("ip是空的")
        else:
            print("ip是", ipStr)
            ipStr = ipStr.split(',')[0]
            data = self.homeService.insert_feedback_by_userIp(ipStr, param['feedStr'])
        # 组装结果
        result = ResponseBean.set_data(data)
        self.write(json.dumps(result, ensure_ascii=False))
        return

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


# 反向词典 查询结果
class RedictSearchHandler(BaseHandler):
    homeService = HomeService()

    def post(self):

        # 获取参数
        param = json.loads(self.request.body.decode('utf-8'))
        print(param)

        # 参数为空 textType  inputExample  inputWord
        if param['inputExample'].strip() == '' or param['textType'].strip() == '':
            result = ResponseBean.set_status_code(CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            self.write(json.dumps(result, ensure_ascii=False))
            return

        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        lastData = []
        # 如果没有搜索过  就通过模型获取，然后插入数据库
        ipStr = self.request.headers.get('X-Forwarded-For')
        # ipStr = "127.0.0.1"
        if param['textType'] == "1":  # 1 是中文
            paramData = {}
            paramData.setdefault("user_input", param['inputExample'])
            paramData.setdefault("lang", "zh")
            r = requests.post('http://202.112.194.62:6881/api/ReverseDict', data=paramData)
            result = json.loads(r.content)
            if len(result) > 10:
                result = result[:10]

            allData = []
            for segCi in result:
                curCiDict = {}
                # 获取 中文例句
                # data = json.dumps({"word":segCi, "page_size":10, "page_off_set":1})
                # r = requests.post(url="http://39.98.52.179:8685/word/getWordSentenceExample", data=data)
                exampleParamData = {}
                exampleParamData.setdefault("word", segCi)
                exampleParamData.setdefault("lang", "zh")
                r = requests.post('http://127.0.0.1:6889/api/ExampleSearch', data=exampleParamData)
                exampleResult = json.loads(r.content)
                # print(exampleResult)

                if len(exampleResult) == 0:
                    exampleResult.append({"contentQian": "暂无例句"})
                    curCiDict.setdefault("examples", exampleResult)
                else:
                    lastExexamples = []
                    for exmStr in exampleResult:

                        # ret = clean_space(ret)
                        tpmStr = exmStr["content"]
                        # tpmStr = clean_space(tpmStr)
                        index = index_of_str(tpmStr, segCi)[0]
                        ciLen = len(segCi)
                        strOne = tpmStr[0:index]
                        strTwo = tpmStr[index + ciLen:]
                        lastExampleStr = strOne + "<span>" + segCi + "</span>" + strTwo
                        # print(lastExampleStr)
                        sourceStr = ""
                        if exmStr["source"]:
                            sourceStr = exmStr["source"]
                        else:
                            sourceStr = "书名：暂无"
                        example = {
                            "content": lastExampleStr,
                            "contentQian": strOne,
                            "contentZhong": segCi,
                            "contentHou": strTwo,
                            "source": sourceStr
                        }
                        lastExexamples.append(example)
                    curCiDict.setdefault("examples", lastExexamples)

                # 2.调解释模型
                paramTuple = (segCi, param['inputExample'])
                paramList = [paramTuple]
                paramData = {"param": paramList}
                paramData.setdefault("language", "zh")
                r = requests.post('http://202.112.194.62:10120/getdeffqn', data=json.dumps(paramData),
                                  headers=headers)
                result = json.loads(r.text)

                for ret in result:
                    ret = clean_space(ret)

                curCiDict.setdefault("explain", segCi)
                curCiDict.setdefault("explain2", ret)
                expStr = segCi + " " + ret
                if ipStr == None or ipStr == " ":
                    print("ip是空的")
                else:
                    print("ip是", ipStr)
                    ipStr = ipStr.split(',')[0]
                    self.homeService.insert_redict_userIp(ipStr, param['inputExample'], expStr, param['textType'])
                allData.append(curCiDict)

            lastData = allData


        else:  # 3 是英文

            paramData = {}
            paramData.setdefault("user_input", param['inputExample'])
            paramData.setdefault("lang", "en")
            r = requests.post('http://202.112.194.62:6881/api/ReverseDict', data=paramData)
            result = json.loads(r.content)
            if len(result) > 10:
                result = result[:10]

            allData = []
            for segCi in result:

                curCiDict = {}
                exampleParamData = {}
                exampleParamData.setdefault("word", segCi)
                exampleParamData.setdefault("lang", "en")
                r = requests.post('http://127.0.0.1:6889/api/ExampleSearch', data=exampleParamData)
                exampleResult = json.loads(r.content)

                print("英文例句是##################")

                if len(exampleResult) == 0:
                    exampleResult.append({"contentQian": "There is no example for the time being."})
                    curCiDict.setdefault("examples", exampleResult)
                else:
                    lastExexamples = []
                    for exmStr in exampleResult:
                        index = exmStr["content"].index(segCi)
                        ciLen = len(segCi)
                        strOne = exmStr["content"][0:index]
                        strTwo = exmStr["content"][index + ciLen:]
                        lastExampleStr = strOne + "<span>" + segCi + "</span>" + strTwo

                        sourceStr = ""
                        if exmStr["source"]:
                            sourceStr = exmStr["source"]
                        else:
                            sourceStr = "None"

                        example = {
                            "content": lastExampleStr,
                            "contentQian": strOne,
                            "contentZhong": segCi,
                            "contentHou": strTwo,
                            "source": "书名：" + sourceStr
                        }
                        lastExexamples.append(example)
                    curCiDict.setdefault("examples", lastExexamples)
                paramTuple = (segCi, param['inputExample'])
                paramList = [paramTuple]
                paramData = {"param": paramList}
                paramData.setdefault("language", "en")
                r = requests.post('http://202.112.194.62:10120/getdeffqn', data=json.dumps(paramData), headers=headers)
                result = json.loads(r.text)

                curCiDict.setdefault("explain", segCi)
                curCiDict.setdefault("explain2", result[0])
                expStr = segCi + " " + result[0]
                if ipStr == None or ipStr == " ":
                    print("ip是空的")
                else:
                    print("ip是", ipStr)
                    ipStr = ipStr.split(',')[0]
                    self.homeService.insert_redict_userIp(ipStr, param['inputExample'], expStr, param['textType'])

                allData.append(curCiDict)

            lastData = allData

        result = ResponseBean.set_data(lastData)

        self.write(json.dumps(result, ensure_ascii=False))

        return

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


# 获取方向词典 用户ip 列表
class RedictSearchGetUserIPHandler(BaseHandler):
    homeService = HomeService()

    def get(self):
        # 获取参数
        data = self.homeService.get_redict_use_ip()

        # 组装结果
        result = ResponseBean.set_data(data)
        self.write(json.dumps(result, ensure_ascii=False))
        return

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


