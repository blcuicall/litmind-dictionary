import Vue from 'vue'
import Router from 'vue-router'
import DictMain from '@/components/DictMain'
import ReDictMain from '@/components/ReDictMain'
import AdminUserIp from '@/components/AdminUserIp'
import ReAdminUserIp from '@/components/ReAdminUserIp'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'dictMain',
      component: DictMain
    }
  ]
})
