<template>
    <div class="seat-selection">
        <h1 class="text-superblue">Select Your Seats</h1>
        <p class="lead text-dark">Click on available category to select.</p>
        <p>
            <!-- User ID: {{ this.$auth0.user.value.sub.split('|')[1] }} <br> -->
            Match ID: {{ $route.params.id }}
        </p>
        <!-- Always display the seat map -->
        <div class="seat-map">
            <div v-for="(row, rowIndex) in seatMap" :key="rowIndex" class="seat-row">
                <div v-for="(seat, seatIndex) in row" :key="seatIndex" @click="selectSeat(seat)" class="seat"
                    :class="{ selected: seat.selected, unavailable: !seat.available }">
                    {{ seat.label }}: {{ seat.quantity }}
                    Reserved: {{ seat.reserved }}
                </div>
            </div>
        </div>
        <!-- Display quantity selectors for each selected seat -->
        <div v-for="seat in selectedSeats" :key="seat.label" class="quantity-selector">
            <label>Select Quantity for {{ seat.label }}:</label>
            <select v-model="selectedQuantities[seat.label]">
                <option v-for="n in seat.left" :value="n">{{ n }}</option>
            </select>
        </div>

        <!-- Display the proceed button if conditions are met -->
        <div v-if="proceedEnabled" class="d-flex justify-content-center mb-3 mt-2">
            <button class="btn btn-primary gradient-button1" @click="proceedToCheckout">
                Proceed
            </button>
        </div>
    </div>
    <!-- {{ seatMap }} -->
    <!-- {{ seatData }} -->
</template>

<script>
import axios from "axios";
export default {
    // props: ['match_id', 'selectedTickets'],
    data() {
        return {
            seatMap: [
                [
                    { label: "A", selected: false, available: true, quantity: 0, reserved: 0 },
                    { label: "B", selected: false, available: true, quantity: 0, reserved: 0 },
                    { label: "C", selected: false, available: true, quantity: 0, reserved: 0 },
                ],
                // [{ label: "Online", selected: false, available: true }],
            ],
            selectedQuantities: {
                A: 0,
                B: 0,
                C: 0,
                // Online: 0,
            },
            maxQuantity: 4,
            selectedSeats: [], // Track the currently selected seats
        };
    },
    computed: {
        proceedEnabled() {
            const seatSelected = this.selectedSeats.length > 0;
            const quantitySelected = this.selectedSeats.every(seat => this.selectedQuantities[seat.label] > 0);
            return seatSelected && quantitySelected;
        },
    },
    mounted() {
        // Inital to get seats
        axios.post("http://localhost:8000/api/v1/seat/tickets/count", {
            "match_id": this.$route.params.id, // note that there is a bug here, if we visit the seats page like this. 
        }).then((response) => {
            if (response) {
                console.log(response.data)
                let reserved_tickets = response.data.reserved_tickets
                let available_tickets = response.data.available_tickets
                for (let row of this.seatMap) {
                    for (let seat of row) {
                        if (seat.label == "A") {
                            seat.quantity = available_tickets.A
                            seat.reserved = reserved_tickets.A
                            seat.left = seat.quantity - seat.reserved
                            if (seat.reserved >= seat.quantity) {
                                seat.available = false
                            }
                        }
                        if (seat.label == "B") {
                            seat.quantity = available_tickets.B
                            seat.reserved = reserved_tickets.B
                            seat.left = seat.quantity - seat.reserved
                            if (seat.reserved >= seat.quantity) {
                                seat.available = false
                            }
                        }
                        if (seat.label == "C") {
                            seat.quantity = available_tickets.C
                            seat.reserved = reserved_tickets.C
                            seat.left = seat.quantity - seat.reserved
                            if (seat.reserved >= seat.quantity) {
                                seat.available = false
                            }
                        }
                    }
                }
            }
        })
    },
    methods: {
        selectSeat(seat) {
            if (seat.available) {
                // Deselect all other seats
                this.selectedSeats.forEach((selectedSeat) => {
                    if (selectedSeat.label !== seat.label) {
                        selectedSeat.selected = false;
                    }
                });
                // Toggle selected state of the clicked seat
                seat.selected = !seat.selected;
                // Update selectedSeats array
                this.selectedSeats = seat.selected ? [seat] : [];
            }
        },

        proceedToCheckout() {
            // Passing non parameter data to the checkout page
            const selectedTickets = this.selectedSeats.map((seat) => ({
                category: seat.label,
                quantity: this.selectedQuantities[seat.label],
            }));

            this.$store.dispatch("updateSelectedTickets", selectedTickets);

            this.$router.push({
                name: "checkout",
                params: {
                    id: this.$route.params.id,
                    // selectedTickets: JSON.stringify(selectedTickets) // Convert to JSON string
                },
                props: {
                    selectedTickets: selectedTickets,
                },
            });
            // emit over to checkout
            // this.$emit('checkout', selectedTickets);

            // // send a response to the backend to create a checkout session
            // fetch(`http://localhost:8000/api/v1/booking/init-match-booking/${match_id}?userid=${userid}&cat=${cat}&qty=${qty}`)
            //     .then((response) => response.json())
            //     .then((data) => {
            //         // if response successful, redirect to the checkout page
            //         if (data.code === 200) {
            //             this.$router.push('/views/checkout');
            //         }
            //     })
            //     .catch((error) => {
            //         console.error('Error:', error);
            //     });
        },
        getSelectedSeats() {
            return this.selectedSeats.map((seat) => seat.label);
        },
    },
};
</script>

<style scoped>
.text-superblue {
    color: #5356ff;
}

.seat-selection {
    text-align: center;
    margin-top: 50px;
}

.seat-map {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.seat-row {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

.seat {
    width: 90px;
    height: 75px;
    border: 1px solid #ccc;
    margin: 0 5px;
    cursor: pointer;
}

.selected {
    background-color: green;
}

.unavailable {
    background-color: #ccc;
}

.quantity-selector {
    margin-top: 10px;
}

.gradient-button1 {
    background-image: linear-gradient(to right, #67C6E3, #5356FF); 
}
</style>
