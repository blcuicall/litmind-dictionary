

class CodeConst(object):
    # 成功
    CODE_OK = "200"

    # 错误
    CODE_ERROR = "500"

    # 传入参数错误
    CODE_ERROR_PARAMETER = "501"
    CODE_ERROR_PARAMETER_EMPTY = "502"

    # 失败
    CODE_FAIL = "400"
    CODE_FAIL_LOGIN_NEEDED = "401"
    CODE_WRONG_PAPER_NO = "402"
    CODE_FAIL_LOGIN_OUTTIME = "407"
    CODE_FAIL_LOGIN = "3101"
    CODE_FAIL_LOGIN_ID_PWD = "3102"
    CODE_FAIL_DATA_EMPTY = "3103"
    CODE_FAIL_USER_EXIST = "2333"

    # 模型
    CODE_NO_USER_OR_CUSTOMER = "4001"

    CODE_TOKEN_ERROR = "4002"
    CODE_TOKEN_EXPIRES = "4003"
    CODE_NO_AUTH = "4004"

    # 未知

    CODE_UNKNOWN = "9999"
    CODE_INFO_UNCON = "5555"


    msg_map = {
        CODE_ERROR: "处理失败",
        CODE_ERROR_PARAMETER: "传入参数错误",
        CODE_ERROR_PARAMETER_EMPTY: "上送参数不能为空",
        CODE_FAIL: "服务执行失败",
        CODE_FAIL_LOGIN: "登陆失败",
        CODE_FAIL_LOGIN_ID_PWD: "登陆失败[用户名或密码错误]",
        CODE_INFO_UNCON: "数据正在更新，暂不提供访问数据权限",
        CODE_NO_USER_OR_CUSTOMER: "没有这个用户或客户",
        CODE_TOKEN_ERROR: "您没有上送正确的token",
        CODE_TOKEN_EXPIRES: "您上送的token已超时，请重新获取",
        CODE_OK: "成功",
        CODE_FAIL_LOGIN_NEEDED: "你需要先登录！",
        CODE_WRONG_PAPER_NO: "身份证号码错误！",
        CODE_FAIL_LOGIN_OUTTIME: "登录超时，请您重新登录",
        CODE_FAIL_USER_EXIST: "用户名已存在，请更换用户名",
        CODE_NO_AUTH: "您没有权限添加审校意见"
    }


    @staticmethod
    def get_code_message(code):
        return CodeConst.msg_map[code]
