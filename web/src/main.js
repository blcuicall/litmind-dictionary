// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import global_ from './global/global.js'
import axios from "axios"
import VueResource from "vue-resource";
import ResultToolView from './global/functView/ResultToolView.vue'
Vue.use(ElementUI)
Vue.use(VueResource);
Vue.use(ResultToolView)
Vue.config.productionTip = false
Vue.prototype.GLOBAL = global_
Vue.prototype.axios = axios
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
