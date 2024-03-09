<template>
    <NavBar />
    <div class="container-fluid mt-3">
        <div class="row">
            <div class="col text-center"> 
                <h1>Match Description</h1>
            </div>
        </div>
    </div>

    <div class="container-fluid mt-3">
        <div class="row">
            <div class="col">
                <EventsCard />
            </div>
        </div>
    </div>
</template>

<script setup>
import EventsCard from '@/views/EventsCard.vue'
import NavBar from '../components/Navbar.vue';
</script>