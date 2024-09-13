<template>
    <div class="checkout">
        <h1>Thank you for purchasing!</h1>
        <!-- back home -->
        <router-link to="/" class="btn btn-primary gradient-button1">Back to Home</router-link>
    </div>
</template>


<style scoped>
.checkout {
    text-align: center;
    margin-top: 50px;
}

.card-container {
    display: flex;
    justify-content: center;
}

.card {
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 20px;
    margin: 10px;
    width: 300px;
    /* Adjust width as needed */
}

.card h2 {
    margin-top: 0;
}

.card p {
    margin-bottom: 0;
}

.gradient-button1 {
    background-image: linear-gradient(to right, #67C6E3, #5356FF); 
}
</style>

<script>
import axios from 'axios';

export default {
    methods: {
        async redirectToCheckout() {
            try {
                // hardcoded data to send. change this JSON dynamically according to the tickets selected
                const data = {
                    "match_id": "1234",
                    "match_name": "Arsenal vs Chelsea",
                    "tickets": [
                        { "category": "A", "quantity": 2 },
                        { "category": "B", "quantity": 3 },
                        { "category": "C", "quantity": 4 },
                        { "category": "Online", "quantity": 1 }
                    ],
                    "user_id": "123"
                };
                // make a POST request to the backend
                fetch('http://localhost:8000/api/v1/billing/checkout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                })
                    .then(response => response.json())
                    .then((data) => {
                        return this.stripe.redirectToCheckout({ sessionId: data.sessionId });
                    })
                    .then((result) => {
                        console.log(result);
                    })

                // Handle response if required
                console.log(response.data);
            } catch (error) {
                console.error(error);
            }
        },
    }
}

</script>