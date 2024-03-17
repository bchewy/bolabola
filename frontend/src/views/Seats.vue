<template>
    <div class="seat-selection">
        <h1 class="text-superblue">Select Your Seats</h1>
        <p class="lead text-dark">Click on available seats to select them.</p>
        <div class="row justify-content-center">
            <div class="col-md-6">
                <select class="form-select mb-3" v-model="selectedOption" @change="selectSeatOption(selectedOption)"
                    style="width: 100%">
                    <option value="Stadium Ticket">Stadium Ticket</option>
                    <option value="Streaming Ticket">Streaming Ticket</option>
                </select>
            </div>
        </div>
        <!-- Display the seat map only if selectedOption is not 'Streaming Ticket' -->
        <div v-if="selectedOption !== 'Streaming Ticket'" class="seat-map">
            <div v-for="(row, rowIndex) in seatMap" :key="rowIndex" class="seat-row">
                <div v-for="(seat, seatIndex) in row" :key="seatIndex" @click="toggleSeat(rowIndex, seatIndex)"
                    class="seat" :class="{ 'selected': seat.selected, 'unavailable': !seat.available }">{{ seat.label }}
                </div>
            </div>
        </div>
        <!-- Display the quantity selector -->
        <div v-if="selectedOption === 'Streaming Ticket' || (selectedOption === 'Stadium Ticket' && selectedSeats.length > 0)"
            class="quantity-selector">
            <label for="quantity">Select Quantity:</label>
            <select id="quantity" v-model="selectedQuantity">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
            </select>
        </div>
        <!-- Display the proceed button if conditions are met -->
        <div v-if="(selectedOption === 'Streaming Ticket' && selectedQuantity > 0) || (selectedOption === 'Stadium Ticket' && selectedSeats.length > 0 && selectedQuantity > 0)"
            class="position-absolute bottom-0 end-0 mb-3 me-3">
            <button class="btn btn-primary" @click="proceedToCheckout">Proceed</button>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        selectedOption: String,
        selectedSeats: Array,
        selectedQuantity: Number
    },
    data() {
        return {
            seatMap: [
                [{ label: 'A1', selected: false, available: true }, { label: 'A2', selected: false, available: false }, { label: 'A3', selected: false, available: true }],
                [{ label: 'B1', selected: false, available: true }, { label: 'B2', selected: false, available: true }, { label: 'B3', selected: false, available: true }],
                [{ label: 'C1', selected: false, available: false }, { label: 'C2', selected: false, available: true }, { label: 'C3', selected: false, available: true }],
            ],
            selectedOption: 'Stadium Ticket', // Default option
            dropdownOpen: false, // Tracks the dropdown state
            selectedQuantity: 0, // Tracks the selected quantity
            selectedSeats: [] // Tracks the selected seats
        };
    },
    methods: {
        toggleSeat(rowIndex, seatIndex) {
            if (this.seatMap[rowIndex][seatIndex].available && this.selectedOption === 'Stadium Ticket') {
                this.seatMap[rowIndex][seatIndex].selected = !this.seatMap[rowIndex][seatIndex].selected;
                this.updateSelectedSeats(); // Update selected seats when toggling seats
            }
        },
        proceedToCheckout() {
            console.log('Selected seats:', this.selectedSeats);
            console.log('Selected quantity:', this.selectedQuantity);
            this.$router.push('/views/checkout');
        },
        updateSelectedSeats() {
            this.selectedSeats = [];
            for (let i = 0; i < this.seatMap.length; i++) {
                for (let j = 0; j < this.seatMap[i].length; j++) {
                    if (this.seatMap[i][j].selected) {
                        this.selectedSeats.push(this.seatMap[i][j].label);
                    }
                }
            }
        },
        selectSeatOption(option) {
            this.selectedOption = option;
            this.dropdownOpen = false; // Close the dropdown after selecting an option
            this.selectedQuantity = 0; // Reset selected quantity when changing option
            this.selectedSeats = []; // Reset selected seats when changing option
        },
        toggleDropdown() {
            this.dropdownOpen = !this.dropdownOpen; // Toggle the dropdown state
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
</style>
