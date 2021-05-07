import Vue from 'vue'
import Vuex from "vuex"
import vuexlogin from 'modules/login'

Vue.use(Vuex)
export default new Vuex.store({
  modules:{
    vuexlogin
  }
})
