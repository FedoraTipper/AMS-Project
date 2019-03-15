import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import BootstrapVue from 'bootstrap-vue'
import VueCytoscape from 'vue-cytoscape'
import router from './router'
import cytoscape from 'cytoscape'
import VueDragDrop from 'vue-drag-drop';

Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)
Vue.use(VueCytoscape)
Vue.use(cytoscape)
Vue.use(VueDragDrop);

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-cytoscape/dist/vue-cytoscape.css'

Vue.config.productionTip = false


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
