<template>
    <div class="seat-selection">
        <h1 class="text-superblue">Select Your Seats</h1>
        <p class="lead text-dark">Click on available seats to select them.</p>
        <!-- Always display the seat map -->
        <div class="seat-map">
            <div v-for="(row, rowIndex) in seatMap" :key="rowIndex" class="seat-row">
                <div v-for="(seat, seatIndex) in row" :key="seatIndex" @click="selectSeat(seat)"
                     class="seat" :class="{ 'selected': seat.selected, 'unavailable': !seat.available }">{{ seat.label }}</div>
            </div>
        </div>
        <!-- Display quantity selector when a seat is selected -->
        <div v-if="selectedSeat" class="quantity-selector">
            <label>Select Quantity for {{ selectedSeat.label }}:</label>
            <select v-model="selectedQuantities[selectedSeat.label]">
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
export default {
    data() {
        return {
            seatMap: [
                [{ label: 'A', selected: false, available: true }, { label: 'B', selected: false, available: false }, { label: 'C', selected: false, available: true }],
                [{ label: 'D', selected: false, available: true }, { label: 'E', selected: false, available: true }, { label: 'F', selected: false, available: true }],
                [{ label: 'G', selected: false, available: false }, { label: 'H', selected: false, available: true }, { label: 'I', selected: false, available: true }],
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
            selectedSeat: null // Track the currently selected seat
        };
    },
    computed: {
        proceedEnabled() {
            return this.selectedSeat !== null;
        }
    },
    methods: {
        selectSeat(seat) {
            if (seat.available) {
                // Deselect previous seat if any
                if (this.selectedSeat) {
                    this.selectedSeat.selected = false;
                }
                // Select new seat
                seat.selected = true;
                this.selectedSeat = seat;
            }
        },
        proceedToCheckout() {
            console.log('Selected seats:', this.getSelectedSeats());
            console.log('Selected quantities:', this.selectedQuantities);
            this.$router.push('/views/checkout');
        },
        getSelectedSeats() {
            const selectedSeats = [];
            for (let i = 0; i < this.seatMap.length; i++) {
                for (let j = 0; j < this.seatMap[i].length; j++) {
                    if (this.seatMap[i][j].selected) {
                        selectedSeats.push(this.seatMap[i][j].label);
                    }
                }
            }
            return selectedSeats;
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




