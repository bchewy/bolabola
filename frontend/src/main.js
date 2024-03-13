// import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createAuth0 } from '@auth0/auth0-vue';


const app = createApp(App)


app.use(
    createAuth0({
        domain: "bchewy.auth0.com",
        clientId: `${import.meta.env.VITE_AUTH0_CLIENTID}`,
        authorizationParams: {
            redirect_uri: window.location.origin
        }
    })
);

// Check if your clientID is valid in your .env file in `/frontend/.env`
console.log("clientid")
console.log(import.meta.env.VITE_AUTH0_CLIENTID)

app.use(router)
app.mount('#app')
