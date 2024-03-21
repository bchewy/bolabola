<template>
    <div class="checkout">
        <h1 class="text-superblue">Confirm your tickets...</h1>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Match Name</th>
                    <th>Match ID</th>
                    <th>Category</th>
                    <th>Quantity</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(ticket, index) in selectedTickets" :key="index">
                    <td>{{ match_name }}</td>
                    <td>{{ match_id }}</td>
                    <td>{{ ticket.category }}</td>
                    <td>{{ ticket.quantity }}</td>
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
            selectedQuantity: Number,
            match_id: "1234", // to be fetched from previous page
            match_name: "Arsenal vs Chelsea", // to be fetched from previous page
            user_id: this.$auth0.user.value.sub,
            // tickets: [
            //     { category: "A", quantity: 2 },
            //     { category: "B", quantity: 3 },
            //     { category: "Online", quantity: 4 },
            // ], 
            selectedTickets: [],
        };
    },
    methods: {
        redirectToCheckout() {
            try {
                // hardcoded data to send. change this JSON dynamically according to the tickets selected
                const data = {
                    "match_id": "1234",
                    "match_name": "Arsenal vs Chelsea",
                    "tickets": selectedTickets // [
                //         { "category": "A", "quantity": 2 },
                //         { "category": "B", "quantity": 3 },
                //         { "category": "C", "quantity": 4 },
                // ]
                    ,
                    "user_id": this.user_id,
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
        handleCheckout(selectedTickets) {
            this.selectedTickets = selectedTickets; // Update selectedTickets with emitted data
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