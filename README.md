# wenxindict


## 前端

``` bash
# 下载项目之后，先初始化项目，下载安装依赖
npm install

# 运行项目，本地测试
npm run dev

# 项目打包，部署上线
npm run build

```

## 后端
``` bash
# 与模型相关接口
一.正向词典：
1.1 传给模型：1.词语  2.句子
1.汉语      输入汉语，返回汉语
2.英语      输入英语，返回英语
3.汉英      输入汉语，返回英语
例子：
输入：词语：立即前往京城     句子：通知一发，他立即前往京城。
结果：
[
    {
        "explain":"立即：表后述事件紧接着发生。",
        "examples":[
            {
                "conent":"听到老师布置的任务，他立即停下手中的重要的事向操场奔去。",
                "source":"来源：《XXXX》"
            },
                        {
                "conent":"遇到这样的麻烦，我们必须立即采取行动，刻不容缓。",
                "source":"来源：《XXXX》"
            },
            ...
        ]
    },
    {
        "explain":"前往：向特定处所去。",
        "examples":[
            {
                "conent":"听到老师布置的任务，他立即停下手中的重要的事向操场奔去。",
                "source":"来源：《XXXX》"
            },
                        {
                "conent":"遇到这样的麻烦，我们必须立即采取行动，刻不容缓。",
                "source":"来源：《XXXX》"
            },
            ...
        ]
    },
    ...

]
1.2 正向词典模型相关接口
    # 将参数封装成元组形式
        paramTuple = (param['inputWord'], param['inputExample'])
        paramList = [paramTuple]
        paramData = {"param": paramList}

        1.2.1 汉英模型
            paramData.setdefault("language", "zh")
            r = requests.post('http://202.112.194.62:10119/getdefkcl', data=json.dumps(paramData),headers=headers)
            result = json.loads(r.text)

        1.2.2 汉语模型
            paramData.setdefault("language", "zh")
            r = requests.post('http://202.112.194.62:10120/getdeffqn', data=json.dumps(paramData),headers=headers)
            result = json.loads(r.text)

        1.2.3 英英模型
            paramData.setdefault("language", "en")
            r = requests.post('http://202.112.194.62:10120/getdeffqn', data=json.dumps(paramData), headers=headers)
            result = json.loads(r.text)
1.3 正向词典 例句 模型相关接口

        1.3.1 中文例句模型
            data = json.dumps({"word":segCi, "page_size":5, "page_off_set":1})
            r = requests.post(url="http://39.98.52.179:8685/word/getWordSentenceExample", data=data)
            examplesResult = json.loads(r.content)

        1.3.2 英文例句 模型
            exampleParamData = {}
            exampleParamData.setdefault("word", param['inputWord'])
            exampleParamData.setdefault("lang", "en")
            r = requests.post('http://127.0.0.1:6882/api/ExampleSearch', data=exampleParamData)
            exampleResult = json.loads(r.content)

二.反向词典：
2.1传给模型：句子
    1.汉语      输入汉语，返回汉语
    2.英语      输入英语，返回英语


例子：
输入：向特定住所去
结果：
[
    {
        "explain":"前往：前去；去：起程～|陪同～。  来源：《XXXX》",
        "examples":[
            {
                "conent":"大家兴高采烈地登上前往香山公园的大巴车。",
                "source":"来源：《XXXX》"
            },
                        {
                "conent":"大家兴高采烈地登上前往香山公园的大巴车。",
                "source":"来源：《XXXX》"
            },
                        {
                "conent":"大家兴高采烈地登上前往香山公园的大巴车。",
                "source":"来源：《XXXX》"
            },
            ...
        ]
    },
    {
        "explain":"前往：前去；去：起程～|陪同～。  来源：《XXXX》",
        "examples":[
            {
                "conent":"大家兴高采烈地登上前往香山公园的大巴车。",
                "source":"来源：《XXXX》"
            },
                        {
                "conent":"大家兴高采烈地登上前往香山公园的大巴车。",
                "source":"来源：《XXXX》"
            },
                        {
                "conent":"大家兴高采烈地登上前往香山公园的大巴车。",
                "source":"来源：《XXXX》"
            },
            ...
        ]
    },
    ...

]


2.2 反词典模型相关接口

        2.2.1 汉语模型
            paramData = {}
            paramData.setdefault("user_input", param['inputExample'])
            paramData.setdefault("lang", "zh")
            r = requests.post('http://202.112.194.62:6881/api/ReverseDict', data=paramData)
            result = json.loads(r.content)

        2.2.2 英语模型
            paramData = {}
            paramData.setdefault("user_input", param['inputExample'])
            paramData.setdefault("lang", "en")
            r = requests.post('http://202.112.194.62:6881/api/ReverseDict', data=paramData)
            result = json.loads(r.content)


```


