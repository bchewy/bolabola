<template>
    <div class="seat-selection">
        <h1>Select Your Seats</h1>
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
</template>

<style scoped>
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

<script>
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
</script>
