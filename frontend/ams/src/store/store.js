import Vuex from 'vuex';
import Vue from "vue"

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    username: "User",
    privilege: false,
    user_show: false
  },
  mutations: {
    set_privilege(state, bool) {
      state.privilege = bool
    },
    set_username(state, user) {
      state.username = user
      state.user_show = true
    },
    clear(state) {
      state.username = "User"
      state.privilege = false
      state.user_show = false
    }
  }
});