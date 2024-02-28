// import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createAuth0 } from '@auth0/auth0-vue';


const app = createApp(App)

app.use(router)
app.use(
    createAuth0({
        domain: "bchewy.auth0.com",
        clientId: "C9lyittqlVtlVGtYEHImh1vwOYH0Rsaf",
        authorizationParams: {
            redirect_uri: window.location.origin
        }
    })
);

app.mount('#app')
