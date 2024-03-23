<template>
    <div class="seat-selection">
        <h1 class="text-superblue">Select Your Seats</h1>
        <p class="lead text-dark">Click on available seats to select them.</p>
        <p>
            User ID: {{ this.$auth0.user.value.sub.split('|')[1] }} <br>
            Match ID: {{ $route.params.id }}
        </p>
        <!-- Always display the seat map -->
        <div class="seat-map">
            <div v-for="(row, rowIndex) in seatMap" :key="rowIndex" class="seat-row">
                <div v-for="(seat, seatIndex) in row" :key="seatIndex" @click="selectSeat(seat)" class="seat"
                    :class="{ 'selected': seat.selected, 'unavailable': !seat.available }">{{ seat.label }}</div>
            </div>
        </div>
        <!-- Display quantity selectors for each selected seat -->
        <div v-for="seat in selectedSeats" :key="seat.label" class="quantity-selector">
            <label>Select Quantity for {{ seat.label }}:</label>
            <select v-model="selectedQuantities[seat.label]">
                <option v-for="n in maxQuantity" :value="n">{{ n }}</option>
            </select>
        </div>
        <!-- Display the proceed button if conditions are met -->
        <div v-if="proceedEnabled" class="position-absolute bottom-0 end-0 mb-3 me-3">
            <button class="btn btn-primary" @click="proceedToCheckout">Proceed</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    // props: ['match_id', 'selectedTickets'],
    data() {
        return {
            seatMap: [
                [{ label: 'A', selected: false, available: true }, { label: 'B', selected: false, available: true }, { label: 'C', selected: false, available: true }],
                [{ label: 'D', selected: false, available: true }, { label: 'E', selected: false, available: true }, { label: 'F', selected: false, available: true }],
                [{ label: 'G', selected: false, available: true }, { label: 'H', selected: false, available: true }, { label: 'I', selected: false, available: true }],
                [{ label: 'Online', selected: false, available: true }]
            ],
            selectedQuantities: {
                'A': 0,
                'B': 0,
                'C': 0,
                'D': 0,
                'E': 0,
                'F': 0,
                'G': 0,
                'H': 0,
                'I': 0,
                'Online': 0
            },
            maxQuantity: 4, // Maximum selectable quantity
            selectedSeats: [] // Track the currently selected seats
        };
    },
    computed: {
        proceedEnabled() {
            return this.selectedSeats.length > 0;
        },
    },
    methods: {
        selectSeat(seat) {
            if (seat.available) {
                // Deselect all other seats
                this.selectedSeats.forEach(selectedSeat => {
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
            // const selectedTickets = [];
            // for (const seat of this.selectedSeats) {
            //     const category = seat.label;
            //     const quantity = this.selectedQuantities[category];
            //     selectedTickets.push({ category, quantity });
            // }
            // console.log("SELECTED SEATS IN SEAT.VUE", selectedTickets);
            // this.$router.push({ name: 'checkout', params: { id: this.match_id, selectedTickets: this.selectedTickets } });


            // Passing non parameter data to the checkout page
            const selectedTickets = this.selectedSeats.map(seat => ({
                category: seat.label,
                quantity: this.selectedQuantities[seat.label]
            }));

            this.$store.dispatch('updateSelectedTickets', selectedTickets);


            this.$router.push({
                name: 'checkout',
                params: {
                    id: this.$route.params.id,
                    // selectedTickets: JSON.stringify(selectedTickets) // Convert to JSON string
                },
                props: {
                    selectedTickets: selectedTickets
                }
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
            return this.selectedSeats.map(seat => seat.label);
        }

    }

};
</script>


<style scoped>
.text-superblue {
    color: #5356FF;
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
    width: 30px;
    height: 30px;
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
</style>
