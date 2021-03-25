 <template>
  <div class="background">
    <div class="result-div">
      <div class="result-explain-div">
        <div class="top-result1">{{ resultDataDict.explain }}</div>
        <div class="top-result2" v-if="resultDataDict.explain2">
          {{ resultDataDict.explain2 }}
        </div>

        <div>
          <el-button class="xiugai-btn" @click="resetBtnClick">{{
            resetBtnLabel
          }}</el-button>
        </div>
      </div>

      <div class="result-list-div">
        <div class="infinite-list-div">
          <ul class="infinite-list" style="overflow: auto">
            <li class="infinite-list-li" v-for="value in dataArrList">
              {{ value.contentQian }}<span>{{ value.contentZhong }}</span
              >{{ value.contentHou }}

              <span v-if="value.source" class="sourceLabel2"
                >{{ sourceLabel }}{{ value.source }}</span
              >
            </li>
          </ul>
        </div>

        <div>
          <el-button
            class="more-btn"
            v-if="isShowMoreBtnView"
            @click="moreLabelClinck"
            >{{ moreBtnLabel }}</el-button
          >
        </div>
      </div>

      <div class="empty-div"></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      exchangeExplainInfoUrl: this.GLOBAL.BASE_URL + "/home/updataExplain",
      zanExplainUrl: this.GLOBAL.BASE_URL + "/home/upExplianZan",
      moreBtnLabel: " + 更多例句 ",
      resetBtnLabel: "修改",
      sourceLabel: "来源：",
      moreSeachWeight: "110px",
      isShowMoreBtnView: false,
      changeSign: 1,
      dataArrList: [],
      oneElementArr: [],
      oneArr: [],
      zanLabel: "赞",
      caiLabel: "踩",
    };
  },
  props: ["resultDataDict", "selectType"],
  mounted: function () {
    for (var i = 0; i < this.resultDataDict.examples.length; i++) {
      var tmpDict = this.resultDataDict.examples[i];
      if (tmpDict.source) {
        var sourceStr = tmpDict.source;
        sourceStr = sourceStr.replace("书名：", "");
        tmpDict.source = sourceStr;
      }
    }

    this.oneArr = [];
    if (this.resultDataDict.examples.length >= 5) {
      for (var i = 0; i < 5; i++) {
        var tmpDict = this.resultDataDict.examples[i];
        this.oneArr.push(tmpDict);
      }
      this.isShowMoreBtnView = true;
    } else {
      this.oneArr = this.resultDataDict.examples;
      this.isShowMoreBtnView = false;
    }

    this.dataArrList = this.oneArr;

    if (this.selectType == 1) {
      this.moreBtnLabel = "+ More examples";
      this.resetBtnLabel = "Feedback";
      this.sourceLabel = "From：";
      this.zanLabel = "Praise";
      this.caiLabel = "StepOn";
    } else {
      this.moreBtnLabel = "+ 更多例句";
      this.resetBtnLabel = "修改";
      this.sourceLabel = "来源：";
      this.zanLabel = "赞";
      this.caiLabel = "踩";
    }
  },
  methods: {
    moreLabelClinck() {
      if (this.changeSign == 1) {
        this.changeSign = 2;
        if (this.selectType == 1) {
          this.moreBtnLabel = "- Less examples";
        } else {
          this.moreBtnLabel = "- 收起例句";
        }
        this.dataArrList = this.resultDataDict.examples;
      } else {
        this.changeSign = 1;
        this.dataArrList = this.oneArr;

        if (this.selectType == 1) {
          this.moreBtnLabel = "+ More examples";
        } else {
          this.moreBtnLabel = "+ 更多例句";
        }
      }
    },
    zanBtnClick() {
      console.log("点赞了。。。");
      this.$http
        .post(
          this.zanExplainUrl,
          { explainStr: "性本善 形容具有慈爱、友善等正面特质的" },
          { emulateJSON: false, withCredentials: true }
        )
        .then(
          function (res) {
            if (res.body.statusCode == "200") {
              console.log(res.body.data);
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
    caiBtnClick() {
      console.log("点踩了。。。。");

      this.$http
        .post(
          this.zanExplainUrl,
          {
            explain: explainStr,
            praiseStr: praiseStr,
            steponStr: stepOnStr,
            modifyStr: modifyStr,
          },
          { emulateJSON: false, withCredentials: true }
        )
        .then(
          function (res) {
            if (res.body.statusCode == "200") {
              console.log(res.body.data);
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
    resetBtnClick() {
      this.$emit("done", this.resultDataDict);
    },
    exchangeExplainInfo(explainStr, praiseStr, stepOnStr, modifyStr) {
      this.$http
        .post(
          this.searchContentUrl,
          {
            explain: explainStr,
            praiseStr: praiseStr,
            steponStr: stepOnStr,
            modifyStr: modifyStr,
          },
          { emulateJSON: false, withCredentials: true }
        )
        .then(
          function (res) {
            if (res.body.statusCode == "200") {
              console.log(res.body.data);
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
  },
};
</script>

 <style scoped>
.result-div {
  background-color: white;
}

.result-div .result-explain-div {
  display: flex;
  margin: 10px 30px 0 10px;
}

.top-result {
  margin: 0 20px 0 0;
  color: #00a1b5;
  font-weight: bold;
  font-family: "Arial", "微软雅黑";
}

.top-result1 {
  margin: 0 0px 0 0px;
  font-size: 18px;
  font-weight: bold;
  font-family: "Arial", "微软雅黑";
  color: #555555;
}

.top-result2 {
  margin: 0 20px 0 20px;
  font-size: 18px;
  font-family: "Arial", "微软雅黑";
  color: #555555;
  text-align: left;
}

.xiugai-btn {
  margin: 0 20px 5px 20px;
  background-color: #00a1b5;
  height: 25px;
  line-height: 0;
  text-align: center;
  font-size: 16px;
  bottom: 10px;
  font-weight: bold;
  color: white;
  border-radius: 5px;
  font-family: "Arial", "微软雅黑";
}

.result-div .result-list-div {
  text-align: left;
  background-color: #f3fafb;
  margin: 0px 0px 0px 30px;
}

.infinite-list-div {
  display: flex;
  margin: 10px 0px 0px 0px;
}

.infinite-list {
  width: 100%;
  margin: 10px 10px 0px 0px;
  list-style-type: decimal;
}

.tool-btn {
  margin: 0px 20px 0px;
  font-size: 14px;
}

.empty-div {
  margin: 2px 0 2px 0;
  height: 2px;
}

.infinite-list-li {
  font-size: 16px;
  font-family: "微软雅黑";
  color: #555555;
}

span {
  font-weight: bold;
  color: #00a1b5;
  font-family: "微软雅黑";
  margin: 0px 0 0 0;
}

.sourceLabel2 {
  width: 300px;
  float: right;
  font-size: 14px;
  font-family: "楷体";
  text-align: left;
}

.more-btn {
  margin: 0px 0 0px 30px;
  height: 25px;
  line-height: 0;
  border: 1px solid #9facad;
  border-radius: 17.5px;
  color: #aaaaaa;
  font-size: 14px;
  font-family: "微软雅黑";
}

.zhanwei-div {
  width: 10px;
}
</style>

 <style >
.more-btn:hover {
  background-color: unset;
}
</style>