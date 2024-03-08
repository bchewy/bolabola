<template>
    <div class="confirmation">
        <h1>Confirmed bookings</h1>
        <div class="position-absolute bottom-0 end-0 mb-3 me-3"> <!-- Container for the button -->
            <!-- <button class="btn btn-primary" @click="$router.push('/views/confirmation')">Proceed</button> -->
        </div>
    </div>
</template>
  
  
<style scoped>
.confirmation {
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