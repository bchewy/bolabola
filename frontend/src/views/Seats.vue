<template>
    <div class="queue">
        <h1>Choose your section...</h1>
        <p class="lead text-dark">You have 10 minutes to select your seats. <br> After that time, the selection process will be locked.</p>
        <div class="position-absolute bottom-0 end-0 mb-3 me-3"> <!-- Container for the button -->
            <button class="btn btn-primary" @click="$router.push('/views/checkout')">Proceed</button>
        </div>
    </div>
</template>
  
  
<style scoped>
.queue {
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