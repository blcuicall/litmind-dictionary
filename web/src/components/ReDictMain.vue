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
        <!-- <label class="top-one" >{{aboutSystem}}</label>
            <label class="top-mid" ></label> -->
        <!-- <div class="top-two" >{{aboutSystem}} | {{aboutUs}}</div> -->

        <div class="top-tool-div">
          <el-tabs
            class="el-tabs__item"
            v-model="activeName"
            @tab-click="handleClick"
          >
            <el-tab-pane :label="hanyuBtn" name="first"></el-tab-pane>
            <el-tab-pane :label="yingyuBtn" name="second"></el-tab-pane>
            <!-- <el-tab-pane :label=moreBtn name="fourth"></el-tab-pane> -->
          </el-tabs>

          <el-button class="redict-btn" @click="goRedictPageClinck">{{
            redictBtnLabel
          }}</el-button>
        </div>
      </div>

      <div class="top-redict-div">
        <div class="ju-div">
          <el-input
            class="input-ju"
            v-model="inputJu"
            :placeholder="juLabelHolder"
            @keyup.enter.native="searhBtnClinck"
          ></el-input>

          <div>
            <i class="el-icon-search" @click="searhBtnClinck"></i>
          </div>
        </div>
      </div>

      <div class="result-div">
        <ul class="result-list" style="overflow: auto">
          <div class="result-list-item" v-for="dict in searchDataArr">
            <div>
              <ResultToolView
                :resultDataDict="dict"
                :selectType="selectTpye"
                ref="allVestDialog"
                @done="callbackConfirmVest"
              ></ResultToolView>
            </div>
          </div>
        </ul>
        <!-- <div class="explainWarn-div" v-if="isShawExplainWarnLabel">
                            {{explainWarnLabel}}
                        </div> -->
      </div>

      <div class="empty-div"></div>
    </div>

    <!-- <div class="bottom-div">  -->

    <div class="father-div">
      <label class="tool-btn reproblem-label" @click="returnProblermClick">{{
        returnProblermLabel
      }}</label>
    </div>

    <div class="father-div">
      <label class="tool-btn">Copyright ⓒ BLCU-ICALL 2021</label>
    </div>
    <!-- </div> -->

    <div class="commit-view" v-if="isShowCommitview">
      <div class="commit-div">
        <i class="el-icon-close" @click="cancleBtnClinck"></i>
        <div class="commit-label">{{ currExplain }}</div>

        <div class="commit-input">
          <el-input
            style="border: none; outline: none"
            type="textarea"
            :autosize="{ minRows: 3, maxRows: 3 }"
            :placeholder="resetYourCommit"
            v-model="textarea"
          >
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
    <!-- 提交反馈意见 -->
    <div class="return-commit-view" v-if="isShowReturnCommitview">
      <div class="commit-div">
        <i class="el-icon-close" @click="returnCancleBtnClinck"></i>
        <div class="commit-label">{{ returnCurrProblemLabel }}</div>

        <div class="commit-input">
          <el-input
            style="border: none; outline: none"
            type="textarea"
            :autosize="{ minRows: 3, maxRows: 3 }"
            :placeholder="returnResetYourCommit"
            v-model="returnTextarea"
          >
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
      inputJu: "",
      selectCurrentTextType: "1",
      selectTpye: 2,
      searchContentUrl: this.GLOBAL.BASE_URL + "/home/redictSearchContent",
      insertFeedbackUrl: this.GLOBAL.BASE_URL + "/home/insertFeedback",
      insertReExplainFeedbackUrl:
        this.GLOBAL.BASE_URL + "/home/insertReExplianFeedback",
      searchDataArr: [],
      isShawExplainWarnLabel: false,

      isShowCommitview: false,
      isShowCommitSuccessView: false,
      isShowReturnCommitview: false,

      textarea: "",
      currExplain: "",

      resetYourCommit: "请输入您的修改",
      commitBtnLabel: "提交",
      commitSuccessLabel: "您的反馈已提交，感谢您的支持！",

      returnCurrProblemLabel: "您对我们的系统有何意见或建议？",
      returnTextarea: "",
      returnResetYourCommit: "请输入您的反馈",

      // 切换语言相关属性
      mainTitleLabel: "文心·词典",
      aboutSystem: "关于系统",
      aboutUs: "关于我们",
      redictBtnLabel: "词典",

      hanyuBtn: "汉语",
      yingyuBtn: "English",
      hanyingBtn: "汉英",

      ciLabel: "词语",
      ciLabelHolder: "请输入词语",
      juLabel: "句子",
      juLabelHolder: "请输入您的描述",

      explainWarnLabel: "本释义由系统生成",
      returnProblermLabel: "反馈建议",

      isShowCommitview: false,
      textarea: "",
      currExplain: "",
    };
  },
  components: {
    ResultToolView: ResultToolView, //将别名demo 变成 组件 Demo
  },

  mounted: function () {
    // this.$refs.childComp.$on('resetBtnClick', () => {
    // console.log('父组件监听')
    // })
    this.selectCurrentTextType = "1";
  },
  methods: {
    callbackConfirmVest(curdict) {
      //    console.log("调完子事件，在父事件响应")
      //    console.log(curdict)
      this.isShowCommitview = true;
      this.textarea = "";
      this.currExplain = curdict.explain;
    },

    changeLang(tpyeIndex) {
      this.selectTpye = tpyeIndex;
      this.searchDataArr = [];
      this.inputJu = "";
      this.isShawExplainWarnLabel = false;
      if (tpyeIndex == 1) {
        // 1是英文

        (this.mainTitleLabel = "LitMind Dictionary"),
          (this.aboutSystem = "About LitMind"),
          (this.aboutUs = "About Us"),
          (this.redictBtnLabel = "Dictionary"),
          // this.hanyuBtn = "Chinese",
          // this.yingyuBtn = "English",

          (this.ciLabel = "Word"),
          (this.ciLabelHolder = "Type the search Word."),
          (this.juLabel = "Sentence"),
          (this.juLabelHolder = "Please enter your description."),
          (this.explainWarnLabel = "Source of definitions: Oxford Dictionary."),
          (this.returnProblermLabel = "Make Suggestions");

        this.resetYourCommit = "Please input the definition of your feedback.";
        this.commitBtnLabel = "Submit";
        this.commitSuccessLabel = "Thanks for your feedback !";

        this.returnCurrProblemLabel = "Any suggestions about this website?";
        this.returnResetYourCommit = "Please input your feedback.";
      } else {
        (this.mainTitleLabel = "文心·词典"),
          (this.aboutSystem = "关于系统"),
          (this.aboutUs = "关于我们"),
          (this.redictBtnLabel = "词典"),
          // this.hanyuBtn = "汉语",
          // this.yingyuBtn = "英语",

          (this.ciLabel = "词语"),
          (this.ciLabelHolder = "请输入词语"),
          (this.juLabel = "句子"),
          (this.juLabelHolder = "请输入您的描述"),
          (this.explainWarnLabel = "本页释义来源为《中文词汇网络》"),
          (this.returnProblermLabel = "反馈建议");

        this.resetYourCommit = "请输入您的修改";
        this.commitBtnLabel = "提交";
        this.commitSuccessLabel = "您的反馈已提交，感谢您的支持！";

        this.returnCurrProblemLabel = "您对我们的系统有何意见或建议？";
        this.returnResetYourCommit = "请输入您的反馈";
      }
    },

    handleClick(tab, event) {
      // console.log(this.activeName);
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
      //   console.log("跳转到词典")
      this.$router.push({
        path: "/",
        name: "dictMain",
        query: {},
      });
    },

    // 点击搜索按钮
    searhBtnClinck() {
      // this.selectTypeValue 词语或解释   this.selectCurrentTextType 1：中-中   2：中--英  3： 英--英
      this.getSearchContentData();
    },
    getSearchContentData() {
      // this.selectCurrentTextType 1：中-中   2：中--英  3： 英--英
      this.searchDataArr = [];
      //发送 post 请求
      if (this.inputJu == "") {
        alert("请输入您的描述");
        return;
      }
      console.log("开始请求数据。。。。");
      // this.isShowLoadingView =  true
      this.$http
        .post(
          this.searchContentUrl,
          { inputExample: this.inputJu, textType: this.selectCurrentTextType },
          { emulateJSON: false, withCredentials: true }
        )
        .then(
          function (res) {
            // this.isShowLoadingView =  false
            if (res.body.statusCode == "200") {
              if (res.body.data[0] == "notin") {
                this.searchDataArr = [];
              } else {
                if (res.body.data.length > 10) {
                  for (var i = 0; i < 10; i++) {
                    var tmp = res.body.data[i];
                    this.searchDataArr.push(tmp);
                  }
                } else {
                  this.searchDataArr = res.body.data;
                }

                this.isShawExplainWarnLabel = true;
              }
              //   console.log(this.searchDataArr);
            } else {
              console.log(res.body.message);
            }
          },
          function (res) {
            // this.isShowLoadingView =  false
            console.log(res.status);
          }
        );
    },
    // 提交意见相关事件
    cancleBtnClinck() {
      this.isShowCommitview = false;
      this.textarea = "";
      this.isShowCommitSuccessView = false;
    },
    // 提交 解释的反馈意见
    commitBtnClinck() {
      //发送 post 请求
      if (this.textarea == "") {
        alert("请输入反馈内容66666");
        return;
      }
      console.log("开始请求数据。。。。");

      this.$http
        .post(
          this.insertReExplainFeedbackUrl,
          {
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

    // 提交反馈意见相关事件
    returnCancleBtnClinck() {
      this.isShowReturnCommitview = false;
      this.returnTextarea = "";
      this.isShowCommitSuccessView = false;
    },
    returnCommitBtnClinck() {
      //发送 post 请求
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
label {
  color: #00a1b5;
  font-size: 18px;
  font-weight: bold;
  font-family: "微软雅黑";
}

.content-view {
  margin: 0px 0 0;
}
.top-div {
  background-color: #f8fcfc;
  height: 160px;
}

.top-main-div {
  /* background-color: rebeccapurple; */
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
  font-family: "华文中宋";
}
.top-tool-div {
  /* background-color: fuchsia; */
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
  font-family: "微软雅黑";
  /* background-color: yellow; */
}
.top-result {
  margin: 20px 10px 0 0;
}
.redict-zi {
  position: absolute;
  /* background-color: khaki; */
  right: 105px;
  font-size: 14px;
  width: 25px;
  height: 25px;
  text-align: center;
  line-height: 25px;
  border-radius: 17px;
  border: 2px solid #00a1b5;
}

.top-one {
  position: absolute;
  top: 70px;
  width: 120px;
  height: 30px;
  line-height: 30px;
  right: 120px;
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
  /* color: #00A1B5;  */
}
.top-two {
  position: absolute;
  top: 70px;

  height: 30px;
  line-height: 30px;
  right: 20px;
  font-size: 14px;
  color: #333333;
  font-family: "微软雅黑";
}
.redict-btn {
  position: absolute;
  /* width: 85px; */
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
/* 添加鼠标悬浮事件 改变背景颜色 */
/* .tool-btn:hover {
	background-color: rgb(255, 255, 255);
    color: black;
} */

.input-label {
  background-color: #f3fafb;
  margin: 10 10 10 0px;
  width: 80px;
  line-height: 60px;
  font-size: 18px;

  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
}

.ju-div {
  display: flex;
  border-radius: 15px;
  border: 1px solid #00a1b5;
  margin: 0 0 0 10px;
}
/* 利用穿透，设置input边框隐藏 */
.ju-div >>> .el-input__inner {
  border: 0;
}
.input-ju {
  margin: 10px 10px 10px 10px;
  font-size: 18px;
}

.el-icon-search {
  margin: 10px 20px 0;
  font-size: 38px;
  color: #00a1b5;
  font-weight: bold;
  cursor: pointer;
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
  position: absolute;
  right: 100px;
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
  font-family: "华文中宋";
}
</style>

<style>
.el-tabs__item {
  font-size: 18px !important;
  line-height: 40px;
  display: inline-block;
  list-style: none;
  font-weight: 500;
  font-family: "Times New Roman", "华文中宋";
  /* color: #00A1B5 !important; */
}
.el-tabs__item:hover {
  /* background-color: #00A0B4; */
  color: #00a0b4 !important;
}
.el-tabs__item.is-active {
  color: black !important;
}

.el-tabs__active-bar {
  background-color: #00a1b5;
}

/* 提交意见相关view */
.commit-view {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.5);
  right: 10px;
  bottom: 10px;
  left: 10px;
  top: 10px;
}
/* 提交反馈意见view */
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
  border-radius: 15px;
  font-family: "微软雅黑";
}

.commit-input {
  position: absolute;
  /* background-color: #00A1B5;  */
  top: 100px;
  left: 40px;
  width: 470px;
  height: 95px;
  font-size: 18px;

  font-family: "微软雅黑";
  border: unset;
  outline: none;
}

/* 利用穿透，设置input边框隐藏 */
.commit-div >>> .el-input__inner {
  border: 0;
  border: unset;
  outline: none;
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