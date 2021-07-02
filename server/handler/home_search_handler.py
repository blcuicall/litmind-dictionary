import sys
import json
from common.response_bean import ResponseBean, CodeConst
from common.base_handler import BaseHandler
from server.home_server import HomeService
from dicts.ner import NERDict
import requests
from corenlp_client import CoreNLP

sys.path.append('../')


class HomeSearchHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(HomeSearchHandler, self).__init__(*args, **kwargs)
        self.homeService = HomeService()
        self.type2route = {'1': 'zh2zh', '2': 'zh2en', '3': 'en2en'}
        self.chengyu = self.read_chengyu()
        self.ner_dict = NERDict
        self.annotators = {
            "zh": CoreNLP(url="http://202.112.194.61:8085", lang="zh"),
            "en": CoreNLP(url="http://202.112.194.61:8085", lang="en")
        }

    def read_chengyu(self):
        with open('dicts/chengyu.txt') as fr:
            chengyu = set([line.strip() for line in fr.readlines()])
        return chengyu

    def preprocess_zh(self, input_word, input_example):
        return input_word, input_example

    def preprocess_en(self, input_word, input_example):
        input_word = input_word.lower()
        input_example = input_example.lower()
        return input_word, input_example

    def ner(self, input_word, input_example, input_lang):
        anno = self.annotators[input_lang].annotate(input_example)
        ner_list = anno.entities[0]
        ner_type = None
        if len(ner_list):
            for term in ner_list:
                if input_word == term["text"]:
                    ner_type = term["ner"]
        return ner_type

    def postprocess_zh(self, definition):
        return definition.replace(' ', '')

    def postprocess_en(self, definition):
        return definition

    def get_definition(self, input_word, input_example, route, input_lang):
        if input_lang == "zh":
            input_word, input_example = self.preprocess_zh(
                input_word, input_example)
        elif input_lang == "en":
            input_word, input_example = self.preprocess_en(
                input_word, input_example)
        if input_word not in input_example:
            definition = ""
        else:
            ner_type = self.ner(input_word, input_example, input_lang)
            if ner_type and ner_type in self.ner_dict:
                definition = self.ner_dict[ner_type][input_lang]
            else:
                res = requests.post(f"http://202.112.194.62:10086/{route}",
                                    json={
                                        "word": input_word,
                                        "example": input_example
                                    })
                definition = res.json()[0]
            out_lang = route.split('2')[1]
            if out_lang == 'zh':
                definition = self.postprocess_zh(definition)
            elif out_lang == 'en':
                definition = self.postprocess_en(definition)
        return definition

    def get_examples(self, input_word, input_lang):
        example_api = "http://127.0.0.1:6889/api/ExampleSearch"
        res = requests.post(example_api,
                            data={
                                "word": input_word,
                                "lang": input_lang
                            })
        retrieval = res.json()
        examples = []
        if not retrieval:
            examples.append({"contentQian": "暂无例句"})
        else:
            for item in retrieval:
                sent = item['content']
                source = item.get('source', '书名暂缺')
                word_idx = sent.index(input_word)
                before = sent[:word_idx]
                after = sent[word_idx + len(input_word):]
                sent = sent.replace(input_word, f"<span>{input_word}</span>")
                examples.append({
                    "content": sent,
                    "contentQian": before,
                    "contentZhong": input_word,
                    "ContentHou": after,
                    "source": source
                })
        return examples

    def get_result(self, input_word, input_example, route, input_lang):
        definition = self.get_definition(input_word, input_example, route,
                                         input_lang)
        examples = self.get_examples(input_word, input_lang)

        if not definition:
            explain_in_db = "暂无解释" if input_lang == "zh" else \
                "There is no explanation for the moment"
        else:
            explain_in_db = f"{input_word} {definition}"
        return definition, examples, explain_in_db

    # 运行入口
    def post(self):
        # 获取参数
        param = json.loads(self.request.body.decode('utf-8'))
        print(param)
        # 参数为空 textType  inputExample  inputWord
        if param['inputWord'].strip() == '' or param['inputExample'].strip(
        ) == '' or param['textType'].strip() == '':
            result = ResponseBean.set_status_code(
                CodeConst.CODE_ERROR_PARAMETER_EMPTY)
            self.write(json.dumps(result, ensure_ascii=False))
            return
        input_word = param['inputWord']
        input_example = param['inputExample']
        text_type = param['textType']
        route = self.type2route[text_type]
        input_lang = 'zh' if text_type == '1' or text_type == '2' else 'en'
        definition, examples, explain_in_db = self.get_result(
            input_word, input_example, route, input_lang)

        ip_str = self.request.headers.get('X-Forwarded-For')
        self.homeService.insert_userIp(ip_str, input_word, input_example,
                                       explain_in_db, text_type)

        result_data = [{
            "explain": input_word if definition else 'notin',
            "explain2": definition,
            "examples": examples
        }]
        result = ResponseBean.set_data(result_data)
        self.write(json.dumps(result, ensure_ascii=False))

    def options(self):
        self.write('{"errorCode":"00","errorMessage","success"}')
