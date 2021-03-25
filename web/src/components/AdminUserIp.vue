<template>
  <div class="user-ip" v-loading="loading">
    <div class="top-label">用户查询记录:{{ searchCount }}条</div>
    <el-table
      class="table-list"
      :data="
        tableData.slice(
          (currentPage - 1) * currentPageSize,
          currentPage * currentPageSize
        )
      "
      max-height="800px"
      style="width: 95%"
    >
      <el-table-column prop="user_ip" label="用户ip" width="180">
      </el-table-column>
      <el-table-column prop="create_time" label="查询时间" width="180">
      </el-table-column>
      <el-table-column prop="word" label="查询词语" width="180">
      </el-table-column>
      <el-table-column prop="sentence" label="查询例句"> </el-table-column>
      <el-table-column prop="explain" label="词语解析"> </el-table-column>
    </el-table>

    <div class="next-page">
      <el-pagination
        @size-change="handlePageSizeChange"
        @current-change="handlePageCurrentChange"
        :current-page="currentPage"
        :page-sizes="[15, 30, 50, 100, 200]"
        :page-size="currentPageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="currentTotalSize"
      >
      </el-pagination>
    </div>

    <div class="loading-view" v-if="isShowLoadingView">
      <div class="loading-label">
        <label class="loading-content">加载中...</label>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "AdminUserIp",
  data() {
    return {
      isShowLoadingView: false,
      searchCount: 0,
      searchHistoryUrl: this.GLOBAL.BASE_URL + "/home/searchGetUserIp",
      tableData: [],
      currentTotalSize: 0,
      currentPageSize: 15,
      currentPage: 1,
    };
  },
  mounted: function () {
    this.getUserIP();
  },
  methods: {
    handlePageSizeChange(val) {
      this.currentPageSize = val;
    },
    handlePageCurrentChange(val) {
      this.currentPage = val;
    },

    handleSizeChange(val) {
      this.$emit("sizeChange", val);
    },
    getUserIP() {
      this.isShowLoadingView = true;
      this.$http
        .get(this.searchHistoryUrl, {
          emulateJSON: false,
          withCredentials: true,
        })
        .then(
          function (res) {
            this.isShowLoadingView = false;
            if (res.body.statusCode == "200") {
              this.tableData = res.body.data;
              this.searchCount = this.tableData.length;
              this.currentTotalSize = this.tableData.length;
            } else {
              console.log(res.body.message);
            }
          },
          function (res) {
            this.isShowLoadingView = false;
            console.log(res.status);
          }
        );
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.user-ip {
  position: absolute;
  /* background-color: turquoise; */
  top: 30px;
  left: 30px;
  right: 30px;
  height: 900px;
}

.loading-view {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.1);
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
}
.loading-label {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  margin: auto;
  width: 200px;
  height: 80px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
}
.loading-content {
  position: absolute;
  left: 0;
  top: 0px;
  bottom: 0px;
  bottom: 0;
  right: 0;
  line-height: 80px;

  font-size: 18px;
  text-align: center;
}
.top-label {
  position: absolute;

  top: 30px;
  left: 30px;
  right: 30px;
  height: 40px;
  text-align: center;
  font-size: 22px;
}
.table-list {
  position: absolute;

  top: 100px;
  left: 30px;
  right: 30px;

  height: 800px;
}

.next-page {
  position: absolute;

  top: 940px;
  left: 30px;
  right: 30px;

  height: 44px;
}
</style>
