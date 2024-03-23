<template>
    <div class="checkout">
        <h1 class="text-superblue">Confirm your tickets...</h1>
        <table class="table table-striped">
            <thead>
                <tr>
                    <!-- <th>Match Name</th> -->
                    <th>Match ID</th>
                    <th>Category</th>
                    <th>Quantity</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="items in selectedTickets">
                    <td>{{ match_id }}</td>
                    <td>{{ items }}</td>
                    <td>{{ items }}</td>
                </tr>
            </tbody>
        </table>
        <div class="position-absolute bottom-0 end-0 mb-3 me-3">
            <button class="btn btn-primary" @click="redirectToCheckout">Proceed to Checkout</button>
        </div>
    </div>
</template>


<script>
import axios from 'axios';
export default {
    name: 'checkout',
    data() {
        return {
            user_id: this.$auth0.user.value.sub.split('|')[1],
            match_id: null,
            selectedTickets: null,
        };
    },
    mounted() {
        // Retrieve match ID and selected tickets from route parameters
        this.match_id = this.$route.params.id;
        this.selectedTickets = this.$route.params.selectedTickets;
        console.log(this.selectedTickets);
    },
    methods: {
        redirectToCheckout() {
            try {
                // hardcoded data to send. change this JSON dynamically according to the tickets selected
                const data = {
                    "match_id": this.match_id,
                    "tickets": this.selectedTickets,
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