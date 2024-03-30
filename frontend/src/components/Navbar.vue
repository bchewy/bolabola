<style scoped>
.bg-green {
    background-color: #3a5a40;
}

.bg-lightblue {
    /* background-color: #387ADF; */
    background-color: #5356FF;
}

.bg-lightblue2 {
    background-color: #378CE7;
}

.bg-green2 {
    background-color: #a3b18a;
}

.text-evenlight {
    color: #a3b18a;
}

.text-evenlighter {
    color: white;
}

.text-supergreen {
    color: #a7c957;
}

.text-superblue {
    color: #DFF5FF;
}

.router-link-active {
    /* color: #50C4ED; */
    color: #67C6E3;
}

.nav-item .dropdown-menu {
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    /* Add shadow to dropdown */
}

.nav-item .dropdown-menu .dropdown-item:hover {
    background-color: #67C6E3;
}

.nav-item {
    margin: 0;
    /* Reset margin for nav item */
    padding: 0;
    /* Reset padding for nav item */
}


.navbar-nav .nav-link {
    display: block;
    /* Make sure the link takes up the full width and height of its container */
    line-height: 1.5;
    /* Adjust line height if necessary */
    padding: 0.5rem 1rem;
    /* Adjust padding as per your design */
    margin: 0;
    /* Reset margin for nav link */
    transition: background-color 0.3s, color 0.3s;
    /* Smooth hover transition */
}

.navbar-nav .nav-link:hover {
    /* background-color: #a3b18a; */
    /* color: #159dce; */
    color: #378CE7;
}

.dropdown-toggle::after {
    color: #a3b18a;
    /* Change dropdown arrow color */
}
</style>
<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-lightblue">
        <div class="container">
            <a class="navbar-brand text-superblue" href="#" style="display: flex; align-items: center;">
                <img src="https://s3.ap-southeast-1.amazonaws.com/esd-assets.bchwy.com/ticketboost.png"
                    class="img-fluid" style="max-height: 40px;">
                <router-link class="nav-link text-evenlighter" to="/"
                    style="margin-left: 5px;">Bola Bola</router-link>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <router-link class="nav-link text-evenlighter" to="/">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link text-evenlighter" to="/events">Matches</router-link>
                    </li>
                    <!-- <li class="nav-item">
                        <router-link class="nav-link text-evenlighter" to="/streaming">
                            Live Stream
                        </router-link>
                    </li> -->
                </ul>

                <ul class="navbar-nav">
                    <!-- {{ isAuthenticated }} -->
                    <!-- {{ user }} -->
                    <li v-if="!isAuthenticated" class="nav-item">
                        <a class="nav-link text-evenlighter" @click.prevent="login">Login</a>
                    </li>
                    <li v-else class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle text-evenlighter d-flex align-items-center" href="#"
                            id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <img :src="user.picture" alt="" class="rounded-circle me-2"
                                style="width: 30px; height: 30px" />
                            <span class="text-evenlighter">Welcome, {{ user.name }}!</span>
                        </a>
                        <ul class="dropdown-menu bg-lightblue2 text-evenlighter" aria-labelledby="navbarDropdown">
                            <li>
                                <router-link class="dropdown-item text-light" to="/profile">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                        style="fill: rgba(255, 255, 255, 1);transform: ;msFilter:;">
                                        <path
                                            d="M12 2C6.579 2 2 6.579 2 12s4.579 10 10 10 10-4.579 10-10S17.421 2 12 2zm0 5c1.727 0 3 1.272 3 3s-1.273 3-3 3c-1.726 0-3-1.272-3-3s1.274-3 3-3zm-5.106 9.772c.897-1.32 2.393-2.2 4.106-2.2h2c1.714 0 3.209.88 4.106 2.2C15.828 18.14 14.015 19 12 19s-3.828-.86-5.106-2.228z">
                                        </path>
                                    </svg> Profile</router-link>
                            </li>
                            <!-- <li>
                                <router-link class="dropdown-item text-light" to="/verify">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                        style="fill: rgba(255, 255, 255, 1);transform: ;msFilter:;">
                                        <circle cx="13" cy="4" r="2"></circle>
                                        <path
                                            d="M13.978 12.27c.245.368.611.647 1.031.787l2.675.892.633-1.896-2.675-.892-1.663-2.495a2.016 2.016 0 0 0-.769-.679l-1.434-.717a1.989 1.989 0 0 0-1.378-.149l-3.193.797a2.002 2.002 0 0 0-1.306 1.046l-1.794 3.589 1.789.895 1.794-3.589 2.223-.556-1.804 8.346-3.674 2.527 1.133 1.648 3.675-2.528c.421-.29.713-.725.82-1.225l.517-2.388 2.517 1.888.925 4.625 1.961-.393-.925-4.627a2 2 0 0 0-.762-1.206l-2.171-1.628.647-3.885 1.208 1.813z">
                                        </path>
                                    </svg> Verify</router-link>
                            </li> -->
                            <li
                                v-if="user.email == 'brian@bchewy.com' || user.email == 'melody.wong.2022@smu.edu.sg' || user.email == 'ryanlee99324@gmail.com' || user.email == 'planituser27@gmail.com'">
                                <router-link class=" dropdown-item text-light" to="/admin">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                        style="fill: rgb(255, 255, 255);transform:">
                                        <path
                                            d="m2.344 15.271 2 3.46a1 1 0 0 0 1.366.365l1.396-.806c.58.457 1.221.832 1.895 1.112V21a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1v-1.598a8.094 8.094 0 0 0 1.895-1.112l1.396.806c.477.275 1.091.11 1.366-.365l2-3.46a1.004 1.004 0 0 0-.365-1.366l-1.372-.793a7.683 7.683 0 0 0-.002-2.224l1.372-.793c.476-.275.641-.89.365-1.366l-2-3.46a1 1 0 0 0-1.366-.365l-1.396.806A8.034 8.034 0 0 0 15 4.598V3a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v1.598A8.094 8.094 0 0 0 7.105 5.71L5.71 4.904a.999.999 0 0 0-1.366.365l-2 3.46a1.004 1.004 0 0 0 .365 1.366l1.372.793a7.683 7.683 0 0 0 0 2.224l-1.372.793c-.476.275-.641.89-.365 1.366zM12 8c2.206 0 4 1.794 4 4s-1.794 4-4 4-4-1.794-4-4 1.794-4 4-4z">
                                        </path>
                                    </svg>
                                    Admin</router-link>
                            </li>
                            <li>
                            </li>
                            <li>
                                <hr class="dropdown-divider" />

                            </li>
                            <li>
                                <a class="dropdown-item text-light" @click="logout">Logout
                                    <font-awesome-icon icon="fa-solid fa-arrow-right-from-bracket" />
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
        <div class="overlay bg-white" style="height: 20px;"></div>
    </nav>
</template>


<script>
import { authGuard, useAuth0 } from '@auth0/auth0-vue';
import { watch, computed, defineComponent, ref, watchEffect } from 'vue';
import axios from "axios";

export default {
    setup() {
        const { loginWithRedirect, user, isAuthenticated, logout } = useAuth0();

        const checkUser = async () => {
            if (isAuthenticated.value) {
                console.log('User is authenticated');
                let user_id = user.value.sub;
                let user_id_after_split = user_id.split('|')[1];
                try {
                    // send a post request to the backend to add a new user
                    fetch(`http://localhost:8000/api/v1/user/check-create`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            user_id: user_id_after_split,
                            email: user.value.email,
                            name: user.value.name,
                        }),
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Successfully checked:', data);
                        })
                        .catch((error) => {
                            console.error('Error in check gg:', error);
                        });
                }
                catch (error) {
                    console.error('Error in check:', error);
                }
            }
            else {
                console.log('User is not authenticated');
            }
        }

        // check if the user is authenticated
        watchEffect(() => {
            if (isAuthenticated.value) {
                console.log('User is authenticated');
                console.log('User:', user.value);
                checkUser();
            } else {
                console.log('User is not authenticated');
            }
        });

        return {
            login: async () => {
                try {
                    await loginWithRedirect({
                        appState: { targetUrl: window.location.pathname }
                    });
                } catch (e) {
                    console.error('Failed to login:', e);
                }
            },
            logout: () => {
                logout({ logoutParams: { returnTo: window.location.origin } });
            },
            user,
            isAuthenticated,
            checkUser,
        };
    }
};
</script>

<!-- google-oauth2|106225716514519006902 -->