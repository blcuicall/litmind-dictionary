<template>
  <div class="dictmain">
    <div class="content-view">
      <div class="top-div">
        <div>
          <div class="top-main-div">
            <img class="main-img" src="~@/assets/文心-02.png" />
            <h1 class="top-title">{{ mainTitleLabel }}</h1>
          </div>
        </div>

        <div class="top-tool-div">
          <el-tabs class="el-tabs__item" v-model="activeName" @tab-click="handleClick">
            <el-tab-pane :label="hanyuBtn" name="first"></el-tab-pane>
            <el-tab-pane :label="yingyuBtn" name="second"></el-tab-pane>
            <el-tab-pane :label="hanyingBtn" name="third"></el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <div class="top-redict-div">
        <div class="ci-div">
          <div class="input-label">{{ ciLabel }}</div>

          <el-input class="input-ci" v-model="inputCi" :placeholder="ciLabelHolder"
            @keyup.enter.native="searhBtnClinck"></el-input>
        </div>

        <div class="ju-div">
          <div class="input-label">{{ juLabel }}</div>
          <el-input class="input-ju" v-model="inputJu" :placeholder="juLabelHolder"
            @keyup.enter.native="searhBtnClinck"></el-input>
        </div>
        <div class="search-div" @click="searhBtnClinck">
          <i class="el-icon-search"></i>
          <div class="search-label">{{ searchLabel }}</div>
        </div>
      </div>
      <div class="alert-label" v-if="isShowErrorView">
        <div class="alert-warning-label">{{ noInvoSearchCi }}</div>
      </div>

      <div class="result-div">
        <ul class="result-list" style="overflow: auto">
          <div class="result-list-item" v-for="dict in searchDataArr">
            <div>
              <ResultToolView :resultDataDict="dict" :selectType="selectTpye" ref="allVestDialog"
                @done="callbackConfirmVest"></ResultToolView>
            </div>
          </div>
        </ul>
        <div class="explainWarn-div" v-if="isShawExplainWarnLabel">
          {{ explainWarnLabel }}
        </div>
      </div>

      <div class="empty-div"></div>
    </div>

    <div class="father-div">
      <label class="tool-btn reproblem-label" @click="returnProblermClick">{{
          returnProblermLabel
      }}</label>
    </div>

    <div class="father-div">
      <label class="tool-btn">Copyright ⓒ 2021 BLCU-ICALL,
        <a style="color: #00a1b5; text-decoration: none" href="http://nlp.csai.tsinghua.edu.cn">THUNLP
        </a>
      </label>
    </div>

    <div class="'father-div">
      <label class="tool-btn">
        国家语委科研项目本系统（ZDI135-105）
      </label>
    </div>

    <div class="commit-view" v-if="isShowCommitview">
      <div class="commit-div input-father">
        <i class="el-icon-close" @click="cancleBtnClinck"></i>
        <div class="commit-label">{{ currExplain }}</div>

        <div class="commit-input-dict">
          <el-input style="border: none; outline: none" type="textarea" :autosize="{ minRows: 3, maxRows: 3 }"
            :placeholder="resetYourCommit" v-model="textarea">
          </el-input>
        </div>

        <div class="commit-btn" @click="commitBtnClinck">
          {{ commitBtnLabel }}
        </div>
      </div>

      <div class="commit-div" v-if="isShowCommitSuccessView">
        <i class="el-icon-close" @click="cancleBtnClinck"></i>

        <div class="commit-success">{{ commitSuccessLabel }}</div>
      </div>
    </div>

    <div class="return-commit-view" v-if="isShowReturnCommitview">
      <div class="commit-div input-father">
        <i class="el-icon-close" @click="returnCancleBtnClinck"></i>
        <div class="commit-label">{{ returnCurrProblemLabel }}</div>

        <div class="commit-input-dict">
          <el-input style="border: none; outline: none" type="textarea" :autosize="{ minRows: 3, maxRows: 3 }"
            :placeholder="returnResetYourCommit" v-model="returnTextarea">
          </el-input>
        </div>

        <div class="commit-btn" @click="returnCommitBtnClinck">
          {{ commitBtnLabel }}
        </div>
      </div>

      <div class="commit-div" v-if="isShowCommitSuccessView">
        <i class="el-icon-close" @click="returnCancleBtnClinck"></i>

        <div class="commit-success">{{ commitSuccessLabel }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import ResultToolView from "../global/functView/ResultToolView.vue";
export default {
  name: "DictMain",
  data() {
    return {
      activeName: "first",
      inputCi: "",
      inputJu: "",
      selectCurrentTextType: "1",
      searchContentUrl: this.GLOBAL.BASE_URL + "/home/searchContent",
      insertFeedbackUrl: this.GLOBAL.BASE_URL + "/home/insertFeedback",
      insertExplainFeedbackUrl:
        this.GLOBAL.BASE_URL + "/home/insertExplianFeedback",
      searchDataArr: [],
      isShowErrorView: false,
      isShowCommitview: false,
      isShowCommitSuccessView: false,
      isShowReturnCommitview: false,

      textarea: "",
      currExplain: "",

      isShawExplainWarnLabel: false,

      selectTpye: 2,
      mainTitleLabel: "文心·词典",
      aboutSystem: "关于系统",
      aboutUs: "关于我们",
      redictBtnLabel: "反向词典",

      hanyuBtn: "汉语",
      yingyuBtn: "English",
      hanyingBtn: "汉英",

      ciLabel: "词语",
      ciLabelHolder: "请输入查询词",
      juLabel: "句子",
      juLabelHolder: "请输入包含查询词的句子",
      noInvoSearchCi: "句子中不包含查询词，请重新输入",
      searchLabel: "查  询",

      explainWarnLabel: "本页面释义由系统自动生成",
      returnProblermLabel: "反馈建议",

      resetYourCommit: "请输入您的修改",
      commitBtnLabel: "提交",
      commitSuccessLabel: "您的反馈已提交，感谢您的支持！",

      returnCurrProblemLabel: "您对我们的系统有何意见或建议？",
      returnTextarea: "",
      returnResetYourCommit: "请输入您的反馈",
    };
  },
  components: {
    ResultToolView: ResultToolView,
  },

  mounted: function () {
    this.selectCurrentTextType = "1";
  },
  methods: {
    callbackConfirmVest(curdict) {
      this.isShowCommitview = true;
      this.textarea = "";
      this.currExplain = curdict.explain;
    },

    changeLang(tpyeIndex) {
      this.selectTpye = tpyeIndex;
      this.searchDataArr = [];
      this.inputCi = "";
      this.inputJu = "";
      this.isShawExplainWarnLabel = false;
      if (tpyeIndex == 1) {
        (this.mainTitleLabel = "LitMind Dictionary"),
          (this.aboutSystem = "About LitMind"),
          (this.aboutUs = "About Us"),
          (this.redictBtnLabel = "Reverse Dictionary"),
          (this.ciLabel = "Word"),
          (this.ciLabelHolder = "Type the search Word."),
          (this.juLabel = "Sentence"),
          (this.juLabelHolder = "Please input a sentence containing the word."),
          (this.noInvoSearchCi =
            "There is no query word in the sentence, please re-enter.");
        (this.searchLabel = "Search"),
          (this.explainWarnLabel =
            "Definitions are automatically generated by our system."),
          (this.returnProblermLabel = "Make Suggestions");

        this.resetYourCommit = "Please input the definition of your feedback.";
        this.commitBtnLabel = "Submit";
        this.commitSuccessLabel = "Thanks for your feedback !";

        this.returnCurrProblemLabel = "Any suggestions about this website?";
        this.returnResetYourCommit = "Please input your feedback.";
      } else {
        this.mainTitleLabel = "文心·词典";
        this.aboutSystem = "关于系统";
        this.aboutUs = "关于我们";
        this.redictBtnLabel = "反向词典";
        (this.ciLabel = "词语"), (this.ciLabelHolder = "请输入查询词");
        (this.juLabel = "句子"),
          (this.juLabelHolder = "请输入包含查询词的句子");
        this.noInvoSearchCi = "句子中不包含查询词，请重新输入";
        (this.searchLabel = "查  询"),
          (this.explainWarnLabel = "本页面释义由系统自动生成");
        this.returnProblermLabel = "反馈建议";

        this.resetYourCommit = "请输入您的修改";
        this.commitBtnLabel = "提交";
        this.commitSuccessLabel = "您的反馈已提交，感谢您的支持！";

        this.returnCurrProblemLabel = "您对我们的系统有何意见或建议？";
        this.returnResetYourCommit = "请输入您的反馈";
      }
    },

    handleClick(tab, event) {
      if (this.activeName == "first") {
        this.selectCurrentTextType = "1";
        this.changeLang(2);
      } else if (this.activeName == "second") {
        this.selectCurrentTextType = "3";
        this.changeLang(1);
      } else if (this.activeName == "third") {
        this.selectCurrentTextType = "2";
        this.changeLang(2);
      } else if (this.activeName == "fourth") {
      }
    },
    goRedictPageClinck() {
      this.$router.push({
        path: "/redictmain",
        name: "redictmain",
        query: {},
      });
    },

    searhBtnClinck() {
      this.getSearchContentData();
    },
    getSearchContentData() {
      this.searchDataArr = [];
      this.isShowErrorView = false;

      if (this.inputCi == "" || this.inputJu == "") {
        alert("请选择词语和例句");
        return;
      }
      console.log("开始请求数据。。。。");
      this.$http
        .post(
          this.searchContentUrl,
          {
            inputWord: this.inputCi,
            inputExample: this.inputJu,
            textType: this.selectCurrentTextType,
          },
          { emulateJSON: false, withCredentials: true }
        )
        .then(
          function (res) {
            if (res.body.statusCode == "200") {
              console.log(res.body.data);
              if (res.body.data[0].explain == "notin") {
                console.log("词语不在例句中");
                this.isShowErrorView = true;
                this.searchDataArr = [];
              } else {
                this.searchDataArr = res.body.data;
                this.isShawExplainWarnLabel = true;
                this.isShowErrorView = false;
              }
            } else {
              console.log(res.body.message);
              this.isShowErrorView = false;
            }
          },
          function (res) {
            console.log(res.status);
            this.isShowErrorView = false;
          }
        );
    },

    cancleBtnClinck() {
      this.isShowCommitview = false;
      this.textarea = "";
      this.isShowCommitSuccessView = false;
    },

    commitBtnClinck() {
      if (this.textarea == "") {
        alert("请输入反馈内容66666");
        return;
      }
      console.log("开始请求数据。。。。");

      this.$http
        .post(
          this.insertExplainFeedbackUrl,
          {
            wordStr: this.inputCi,
            sententStr: this.inputJu,
            explainStr: this.currExplain,
            feedbackStr: this.textarea,
          },
          { emulateJSON: false, withCredentials: true }
        )
        .then(
          function (res) {
            if (res.body.statusCode == "200") {
              this.isShowCommitSuccessView = true;
              console.log(res.body.data);
            } else {
              console.log(res.body.message);
            }
          },
          function (res) {
            console.log(res.status);
          }
        );
    },
    returnProblermClick() {
      this.isShowReturnCommitview = true;
    },

    returnCancleBtnClinck() {
      this.isShowReturnCommitview = false;
      this.returnTextarea = "";
      this.isShowCommitSuccessView = false;
    },
    returnCommitBtnClinck() {
      if (this.returnTextarea == "") {
        alert("请输入反馈内容");
        return;
      }
      console.log("开始请求数据。。。。");

      this.$http
        .post(
          this.insertFeedbackUrl,
          { feedStr: this.returnTextarea },
          { emulateJSON: false, withCredentials: true }
        )
        .then(
          function (res) {
            if (res.body.statusCode == "200") {
              this.isShowCommitSuccessView = true;
              console.log(res.body.data);
            } else {
              console.log(res.body.message);
            }
          },
          function (res) {
            console.log(res.status);
          }
        );
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>
.dictmain {
  margin-top: 0px;
}

label {
  color: #00a1b5;
  font-size: 18px;
  font-weight: bold;
}

.top-div {
  background-color: #f8fcfc;
  height: 160px;
}

.top-main-div {
  width: 700px;
  height: 120px;
  display: flex;
  margin: auto;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.main-img {
  margin: 0px 10px 0 50px;
  width: 60px;
  height: 60px;
}

.top-title {
  margin: 0px 40px 0 0px;
  color: black;
  font-size: 48px;
  font-family: "Times New Roman", "华文中宋";
}

.top-tool-div {
  margin: 0 30px 0;
  display: flex;
}

.top-redict-div {
  margin: 60px 20px 0;
}

.father-div {
  height: 25px;
}

.tool-btn {
  margin: 0px 0px 0px;
  height: 40px;
  width: 70px;
  line-height: 40px;
  text-align: center;
  font-size: 14px;
  font-family: "Arial";
}

.top-result {
  margin: 20px 10px 0 0;
}

.redict-zi {
  position: absolute;
  right: 105px;
  font-size: 14px;
  width: 25px;
  height: 25px;
  text-align: center;
  line-height: 25px;
  border-radius: 17px;
  border: 2px solid #00a1b5;
  font-family: "微软雅黑";
}

.top-one {
  position: absolute;
  top: 70px;
  width: 120px;
  height: 30px;
  line-height: 30px;
  text-align: right;
  right: 150px;
  font-size: 14px;
  color: #333333;
  font-family: "微软雅黑";
}

.top-mid {
  position: absolute;
  background-color: #333333;
  top: 75px;
  width: 3px;
  height: 20px;
  line-height: 30px;
  right: 125px;
  font-size: 20px;
}

.top-two {
  position: absolute;
  top: 70px;
  height: 30px;
  line-height: 30px;
  right: 20px;
  text-align: right;
  font-size: 14px;
  color: #333333;
  font-family: "微软雅黑";
}

.redict-btn {
  position: absolute;
  height: 35px;
  line-height: 0;
  right: 20px;
  font-size: 16px;
  color: #00a0b4;
  border-radius: 10px;
  border: 2px solid #00a0b4;
  font-family: "微软雅黑";
}

.redict-btn:hover {
  background-color: #00a0b4;
  color: white;
}

.input-label {
  margin: 15px 0px 0px 10px;
  width: 120px;
  height: 30px;
  line-height: 30px;
  font-size: 18px;
  color: #333333;
  border-right: 2px solid #00a0b4;
  font-family: "微软雅黑";
}

.ci-div {
  display: flex;
  margin: 0 30px 0 30px;
  border-radius: 15px;
  border: 1px solid #00a1b5;
}

.ci-div>>>.el-input__inner {
  border: 0;
}

.input-ci {
  margin: 10px 10px 10px 10px;
  font-size: 18px;
}

.ju-div {
  display: flex;
  border-radius: 15px;
  border: 1px solid #00a1b5;
  margin: 30px 30px 30px 30px;
}

.ju-div>>>.el-input__inner {
  border: 0;
}

.input-ju {
  margin: 10px 10px 10px 10px;
  font-size: 18px;
}

.search-div {
  display: flex;
  width: 400px;
  background-color: #00a0b4;
  border-radius: 10px;
  margin: auto;
  cursor: pointer;
}

.el-icon-search {
  margin: 10px 10px 0 160px;
  font-size: 20px;
  color: white;
  font-weight: bold;
}

.search-label {
  margin: 7px 0px 10px 00px;
  font-size: 18px;
  color: white;
  font-weight: bold;
  font-family: "微软雅黑";
}

.search-btn {
  width: 190px;
}

.alert-label {
  margin: 10px 0 0;
}

.alert-warning-label {
  color: red;
}

.result-div {
  margin: 30px 20px 30px 20px;
  border-radius: 15px;
  background-color: white;
}

.result-list {
  margin: 0px;
}

.result-list .result-list-item {
  margin: 10px 30px 10px 0px;
}

.explainWarn-div {
  margin: 0px 50px 0 0px;
  text-align: right;
  font-size: 16px;
  color: #aaaaaa;
  font-family: "微软雅黑";
}

.empty-div {
  margin: 10px 0 10px 0;
  height: 20px;
}

.reproblem-label {
  cursor: pointer;
  font-family: "Arial", "华文中宋";
}
</style>

<style>
.el-tabs__item {
  font-size: 18px !important;
  line-height: 40px;
  display: inline-block;
  list-style: none;
  font-weight: 500;
  border-bottom: 2px solid #e4e7ed;
  font-family: "Times New Roman", "华文中宋";
}

.el-tabs__item:hover {
  color: #00a0b4 !important;
}

.el-tabs__item.is-active {
  color: black !important;
}

.el-tabs__nav-wrap::after {
  background-color: transparent;
}

.el-tabs__active-bar {
  background-color: #00a1b5;
}

.commit-view {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.6);
  right: 10px;
  bottom: 10px;
  left: 10px;
  top: 10px;
}

.return-commit-view {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.5);
  right: 10px;
  bottom: 10px;
  left: 10px;
  top: 10px;
}

.commit-div {
  position: absolute;
  background-color: white;
  width: 550px;
  height: 250px;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  margin: auto;
  border: 1px solid #00a1b5;
}

.el-icon-close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 38px;
  color: #00a1b5;
  font-weight: bold;
  font-family: "微软雅黑";
}

.commit-label {
  position: absolute;
  top: 50px;
  right: 40px;
  left: 40px;
  height: 35px;
  font-size: 18px;
  font-weight: bold;
  font-family: "微软雅黑";
  text-align: left;
}

.commit-btn {
  position: absolute;
  background-color: #00a1b5;
  right: 40px;
  width: 80px;
  height: 35px;
  line-height: 35px;
  font-size: 18px;
  bottom: 10px;
  font-weight: bold;
  color: white;
  border-radius: 10px;
  font-family: "微软雅黑";
}

.commit-input-dict {
  position: absolute;
  top: 100px;
  left: 40px;
  width: 470px;
  height: 95px;
  font-size: 18px;
  font-family: "微软雅黑";
}

.commit-input-dict>>>.el-textarea__inner {
  border: 0;
  resize: none;
}

.el-textarea {
  border: unset;
}

.commit-success {
  position: absolute;
  right: 40px;
  left: 40px;
  height: 40px;
  line-height: 40px;
  font-size: 18px;
  bottom: 105px;
  font-family: "微软雅黑";
}

.bottom-div {
  position: fixed;
  left: 0px;
  bottom: 30px;
  font-family: "微软雅黑";
  margin: auto;
  width: 100%;
}
</style>
