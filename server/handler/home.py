import json

from common.response_bean import ResponseBean, CodeConst

from common.base_handler import BaseHandler
from common.utils import clean_space
from common.utils import index_of_str
from common.utils import deleteFullpointOfChinaExplain
import sys

from server.home_server import HomeService
import requests
from corenlp_client import CoreNLP

sys.path.append('../')


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
        if param['explain'].strip() == '' or param['praiseStr'].strip(
        ) == '' or param['steponStr'].strip(
        ) == '' or param['modifyStr'].strip() == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
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
            data = self.homeService.updata_search_info(ipStr, param['explain'],
                                                       param['praiseStr'],
                                                       param['steponStr'],
                                                       param['modifyStr'])
        # 组装结果
        result = ResponseBean.set_data(data)
        self.write(json.dumps(result, ensure_ascii=False))
        return

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


# 对正向词典 解释 提出反馈修改意见
class InsertExplianFeedbackByUserIPHandler(BaseHandler):
    homeService = HomeService()

    def post(self):
        # 获取参数
        param = json.loads(self.request.body.decode('utf-8'))
        print(param)

        # 参数为空 useripStr,explain,praiseStr,steponStr,modifyStr
        if param['wordStr'].strip() == '' or param['sententStr'].strip(
        ) == '' or param['explainStr'].strip(
        ) == '' or param['feedbackStr'].strip() == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            self.write(json.dumps(result, ensure_ascii=False))
            return

        # 获取用户ip
        ipStr = self.request.headers.get('X-Forwarded-For')
        # ipStr = "127.0.0.1"

        if ipStr == None or ipStr == " ":
            print("ip是空的")
        else:
            print("ip是", ipStr)
            ipStr = ipStr.split(',')[0]
            data = self.homeService.insert_explain_feedback_by_userIp(
                ipStr, param['wordStr'], param['sententStr'],
                param['explainStr'], param['feedbackStr'])
        # 组装结果
        result = ResponseBean.set_data(data)
        self.write(json.dumps(result, ensure_ascii=False))
        return

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')


# 对正向词典 解释 点赞
class UpExplianZanByUserIPHandler(BaseHandler):
    homeService = HomeService()

    def post(self):
        # 获取参数
        param = json.loads(self.request.body.decode('utf-8'))
        print(param)

        # 参数为空 useripStr,explain,praiseStr,steponStr,modifyStr
        if param['explainStr'].strip() == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            self.write(json.dumps(result, ensure_ascii=False))
            return

        # 获取用户ip
        ipStr = self.request.headers.get('X-Forwarded-For')
        ipStr = '144.52.166.105'

        # if ipStr == None or ipStr == " ":
        #     print("ip是空的")
        # else:
        #     print("ip是", ipStr)
        #     ipStr = ipStr.split(',')[0]

        # 1. 获取解释当前点赞数最大的 一条 数据
        explainData = self.homeService.get_explain_info_by_use_ip(
            ipStr, param['explainStr'])
        print("################")
        print(explainData)
        # 2。更新点赞数

        # data = self.homeService.insert_explain_feedback_by_userIp(ipStr,param['wordStr'],param['sententStr'],param['explainStr'],param['feedbackStr'])
        # 组装结果
        result = ResponseBean.set_data(explainData)
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
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
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
            data = self.homeService.insert_feedback_by_userIp(
                ipStr, param['feedStr'])
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
        if param['inputExample'].strip() == '' or param['textType'].strip(
        ) == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            self.write(json.dumps(result, ensure_ascii=False))
            return

        headers = {
            'content-type':
            'application/json',
            'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
        }

        lastData = []
        # 如果没有搜索过  就通过模型获取，然后插入数据库
        ipStr = self.request.headers.get('X-Forwarded-For')
        # ipStr = "127.0.0.1"
        if param['textType'] == "1":  # 1 是中文
            paramData = {}
            paramData.setdefault("user_input", param['inputExample'])
            paramData.setdefault("lang", "zh")
            r = requests.post('http://202.112.194.62:6881/api/ReverseDict',
                              data=paramData)
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
                r = requests.post('http://127.0.0.1:6889/api/ExampleSearch',
                                  data=exampleParamData)
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
                r = requests.post('http://202.112.194.62:10120/getdeffqn',
                                  data=json.dumps(paramData),
                                  headers=headers)
                result = json.loads(r.text)

                for ret in result:
                    ret = clean_space(ret)

                curCiDict.setdefault("explain", segCi)
                curCiDict.setdefault("explain2", ret)
                expStr = segCi + " " + ret
                if ipStr is None or ipStr == " ":
                    print("ip是空的")
                else:
                    print("ip是", ipStr)
                    ipStr = ipStr.split(',')[0]
                    self.homeService.insert_redict_userIp(
                        ipStr, param['inputExample'], expStr,
                        param['textType'])
                allData.append(curCiDict)

            lastData = allData

        else:  # 3 是英文

            paramData = {}
            paramData.setdefault("user_input", param['inputExample'])
            paramData.setdefault("lang", "en")
            r = requests.post('http://202.112.194.62:6881/api/ReverseDict',
                              data=paramData)
            result = json.loads(r.content)
            if len(result) > 10:
                result = result[:10]

            allData = []
            for segCi in result:

                curCiDict = {}
                exampleParamData = {}
                exampleParamData.setdefault("word", segCi)
                exampleParamData.setdefault("lang", "en")
                r = requests.post('http://127.0.0.1:6889/api/ExampleSearch',
                                  data=exampleParamData)
                exampleResult = json.loads(r.content)

                print("英文例句是##################")

                if len(exampleResult) == 0:
                    exampleResult.append({
                        "contentQian":
                        "There is no example for the time being."
                    })
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
                r = requests.post('http://202.112.194.62:10120/getdeffqn',
                                  data=json.dumps(paramData),
                                  headers=headers)
                result = json.loads(r.text)

                curCiDict.setdefault("explain", segCi)
                curCiDict.setdefault("explain2", result[0])
                expStr = segCi + " " + result[0]
                if ipStr == None or ipStr == " ":
                    print("ip是空的")
                else:
                    print("ip是", ipStr)
                    ipStr = ipStr.split(',')[0]
                    self.homeService.insert_redict_userIp(
                        ipStr, param['inputExample'], expStr,
                        param['textType'])

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


# 对反向词典 解释 提出反馈修改意见
class InsertReExplianFeedbackByUserIPHandler(BaseHandler):
    homeService = HomeService()

    def post(self):
        # 获取参数
        param = json.loads(self.request.body.decode('utf-8'))
        print(param)

        # 参数为空 useripStr,explain,praiseStr,steponStr,modifyStr
        if param['sententStr'].strip() == '' or param['explainStr'].strip(
        ) == '' or param['feedbackStr'].strip() == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            self.write(json.dumps(result, ensure_ascii=False))
            return

        # 获取用户ip
        ipStr = self.request.headers.get('X-Forwarded-For')
        # ipStr = "127.0.0.1"

        if ipStr == None or ipStr == " ":
            print("ip是空的")
        else:
            print("ip是", ipStr)
            ipStr = ipStr.split(',')[0]
            data = self.homeService.insert_re_explain_feedback_by_userIp(
                ipStr, param['sententStr'], param['explainStr'],
                param['feedbackStr'])
        # 组装结果
        result = ResponseBean.set_data(data)
        self.write(json.dumps(result, ensure_ascii=False))
        return

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')
