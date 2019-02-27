import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import cytoautomove from 'cytoscape-automove'
import BootstrapVue from 'bootstrap-vue'
import VueCytoscape from 'vue-cytoscape'
import router from './router'

Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)
Vue.use(VueCytoscape)


import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-cytoscape/dist/vue-cytoscape.css'

Vue.config.productionTip = false


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
