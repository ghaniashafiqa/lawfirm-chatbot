import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import './assets/tailwind.css'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
app.use(Toast, { timeout: 3000, position: 'top-right' })
