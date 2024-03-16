<template>
    <div class="checkout">
        <h1>Confirm your tickets...</h1>
        <p class="lead text-dark text-center">Payment by ...</p>
        <div class="position-absolute bottom-0 end-0 mb-3 me-3"> <!-- Container for the button -->
            <button class="btn btn-primary" @click="redirectToCheckout">Proceed to Checkout</button>
        </div>
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
</style>
  
<script>
import axios from 'axios';

export default {
    methods: {
        redirectToCheckout() {
            try {
                // hardcoded data to send. change this JSON dynamically according to the tickets selected
                const data = {
                    "match_id": "1234",
                    "match_name": "Arsenal vs Chelsea",
                    "tickets": [
                        {"category": "A", "quantity": 2},
                        {"category": "B", "quantity": 3},
                        {"category": "C", "quantity": 4},
                        {"category": "Online", "quantity": 1}
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
                .then((result) => result.json())
                .then((data) => {
                    console.log(data);
                    // redirect to url
                    window.location.href = data.checkout_session.url;
                })
                .then((res) => {
                    console.log(res);
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