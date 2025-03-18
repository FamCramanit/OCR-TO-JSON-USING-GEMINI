import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import axios from 'axios'
import 'bootstrap-icons/font/bootstrap-icons.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'

createApp(App).use(axios).use(store).use(router).use(bootstrap).mount('#app')
