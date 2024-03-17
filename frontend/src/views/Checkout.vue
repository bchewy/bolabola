<template>
    <div class="checkout">
        <h1 class="text-superblue">Confirm your tickets...</h1>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Match Name</th>
                    <th>Match ID</th>
                    <th>User ID</th>
                    <th>Selected Ticket Type</th>
                    <th>Category</th>
                    <th>Quantity</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Arsenal vs Chelsea</td>
                    <td>1234</td>
                    <td>123</td>
                    <td>{{selectedOption}}</td>
                    <td>{{selectedSeats}}</td>
                    <td>{{selectedQuantity}}</td>
                </tr>
            </tbody>
        </table>
        <div class="position-absolute bottom-0 end-0 mb-3 me-3">
            <button class="btn btn-primary" @click="redirectToCheckout">Proceed to Checkout</button>
        </div>
    </div>
</template>


<script>
import SeatSelection from './Seats.vue';
import axios from 'axios';
export default {
    components: {
        SeatSelection,
    },
    data() {
        return {
            selectedOption: String,
            selectedSeats: Array,
            selectedQuantity: Number
        };
    },
    methods: {
        redirectToCheckout() {
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

<style scoped>
.text-superblue {
    color: #5356FF;
}

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