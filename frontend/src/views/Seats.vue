<!-- <template>
    <div class="seat-selection">
        <h1 class="text-superblue">Select Your Seats</h1>
        <p class="lead text-dark">Click on available seats to select them.</p>
        <div class="seat-map">
            <div v-for="(row, rowIndex) in seatMap" :key="rowIndex" class="seat-row">
                <div v-for="(seat, seatIndex) in row" :key="seatIndex" @click="toggleSeat(rowIndex, seatIndex)" class="seat" :class="{ 'selected': seat.selected, 'unavailable': !seat.available }">{{ seat.label }}</div>
            </div>
        </div>
        <div class="position-absolute bottom-0 end-0 mb-3 me-3">
            <button class="btn btn-primary" @click="proceedToCheckout">Proceed</button>
        </div>
    </div>
</template> -->

<template>
    <div class="seat-selection">
        <h1 class="text-superblue">Select Your Seats</h1>
        <p class="lead text-dark">Click on available seats to select them.</p>
        <div class="seat-map">
            <div v-for="(row, rowIndex) in seatMap" :key="rowIndex" class="seat-row">
                <div v-for="(seat, seatIndex) in row" :key="seatIndex" @click="toggleSeat(rowIndex, seatIndex)" class="seat" :class="{ 'selected': seat.selected, 'unavailable': !seat.available }">{{ seat.label }}</div>
            </div>
        </div>
        <div class="dropdown mb-3">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="seatDropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Seat Options
            </button>
            <div class="dropdown-menu" aria-labelledby="seatDropdown">
                <button class="dropdown-item" @click="selectSeatOption('Choose Seats')">Choose Seats</button>
                <button class="dropdown-item" @click="selectSeatOption('Quantity')">Select Quantity</button>
            </div>
        </div>
        <div v-if="selectedOption === 'Choose Seats'" class="position-absolute bottom-0 end-0 mb-3 me-3">
            <button class="btn btn-primary" @click="proceedToCheckout">Proceed</button>
        </div>
    </div>
</template>


<style scoped>
.text-superblue{
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
</style>

<!-- <script>
export default {
    data() {
        return {
            seatMap: [
                [{ label: 'A1', selected: false, available: true }, { label: 'A2', selected: false, available: false }, { label: 'A3', selected: false, available: true }],
                [{ label: 'B1', selected: false, available: true }, { label: 'B2', selected: false, available: true }, { label: 'B3', selected: false, available: true }],
                [{ label: 'C1', selected: false, available: false }, { label: 'C2', selected: false, available: true }, { label: 'C3', selected: false, available: true }],
            ]
        };
    },
    methods: {
        toggleSeat(rowIndex, seatIndex) {
            if (this.seatMap[rowIndex][seatIndex].available) {
                this.seatMap[rowIndex][seatIndex].selected = !this.seatMap[rowIndex][seatIndex].selected;
            }
        },
        proceedToCheckout() {
            // Add logic to handle proceeding to checkout with selected seats
            console.log('Selected seats:', this.getSelectedSeats());
            // Example: this.$router.push('/views/checkout');
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
</script> -->

<script>
export default {
    data() {
        return {
            seatMap: [
                [{ label: 'A1', selected: false, available: true }, { label: 'A2', selected: false, available: false }, { label: 'A3', selected: false, available: true }],
                [{ label: 'B1', selected: false, available: true }, { label: 'B2', selected: false, available: true }, { label: 'B3', selected: false, available: true }],
                [{ label: 'C1', selected: false, available: false }, { label: 'C2', selected: false, available: true }, { label: 'C3', selected: false, available: true }],
            ],
            selectedOption: 'Choose Seats' // Default option
        };
    },
    methods: {
        toggleSeat(rowIndex, seatIndex) {
            if (this.seatMap[rowIndex][seatIndex].available && this.selectedOption === 'Choose Seats') {
                this.seatMap[rowIndex][seatIndex].selected = !this.seatMap[rowIndex][seatIndex].selected;
            }
        },
        proceedToCheckout() {
            // Add logic to handle proceeding to checkout with selected seats
            console.log('Selected seats:', this.getSelectedSeats());
            // Example: this.$router.push('/views/checkout');
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
        },
        selectSeatOption(option) {
            this.selectedOption = option;
        }
    }
};
</script>

