// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Bourgeon from 'bourgeon'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import App from './App.vue'

Vue.use(ElementUI)

Vue.use(Bourgeon, {
  locales: ['fr', 'en']
})

/* eslint-disable no-new */
new Vue({
  render: h => h(App)
}).$mount('#app')
