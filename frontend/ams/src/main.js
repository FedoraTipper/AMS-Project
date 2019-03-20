import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import BootstrapVue from 'bootstrap-vue'
import VueCytoscape from 'vue-cytoscape'
import router from './router'
import cytoscape from 'cytoscape'
import VueDragDrop from 'vue-drag-drop';
import vuescroll from 'vuescroll';
import store from "./store/store";

Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)
Vue.use(VueCytoscape)
Vue.use(cytoscape)
Vue.use(VueDragDrop);
Vue.use(vuescroll)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-cytoscape/dist/vue-cytoscape.css'
import 'vuescroll/dist/vuescroll.css';

Vue.config.productionTip = false


new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
