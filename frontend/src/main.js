// import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'

import { createApp, provide } from 'vue'
import App from './App.vue'
import router from './router'
import { createAuth0 } from '@auth0/auth0-vue';
import { createApolloProvider } from '@vue/apollo-option'
import { ApolloClient, ApolloLink, InMemoryCache, createHttpLink } from '@apollo/client/core'
import store from './store';


const app = createApp(App)
app.use(store)

// const cache = new InMemoryCache()

// const httpLink = createHttpLink({
//     uri: 'http://localhost:8000/api/v1/match/', // Replace with your GraphQL server URI
// });

// const authMiddleware = new ApolloLink((operation, forward) => {
//     // add the authorization to the headers
//     operation.setContext({
//       headers: {
//         'Access-Control-Allow-Origin': '*',
//       },
//     });

//     return forward(operation);
// });

// const apolloClient = new ApolloClient({
//     link: authMiddleware.concat(httpLink),
//     cache: new InMemoryCache(),
// });

// const apolloProvider = createApolloProvider({
//     defaultClient: apolloClient,

// })

app.use(
    createAuth0({
        domain: "bchewy.auth0.com",
        clientId: `Mq0NzZPGFcxVVcm7vRY08xo7mYBHGNWZ`,
        authorizationParams: {
            redirect_uri: window.location.origin
        }
    })
);

// Check if your clientID is valid in your .env file in `/frontend/.env`
console.log("clientid")
console.log(import.meta.env.VITE_AUTH0_CLIENTID)

app.use(router)
// app.use(apolloProvider)
app.mount('#app')
