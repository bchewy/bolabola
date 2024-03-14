<template>
    <div class="container-fluid mt-3">
      <div class="card h-100 position-relative" style="min-width: 18rem;" v-if="selectedMatch">
        <div class="card-body">
          <h5 class="card-title">{{ selectedMatch.title }}</h5>
          <div class="card-subtitle mb-2">Date: {{ selectedMatch.date }}</div>
          <p class="card-text description">
            Venue: {{ selectedMatch.venue }} <br>
            Competition: {{ selectedMatch.competition }}
          </p>
        </div>
        <div class="position-absolute bottom-0 end-0 mb-3 me-3"> <!-- Container for the button -->
          <button class="btn btn-primary" @click="$router.push('/views/queue')">Book Now</button>
        </div>
      </div>
    </div>
  </template>
  
  
<script setup>
import { toRefs } from "vue";
const props = defineProps(["project"]);
const { project } = toRefs(props);
</script>
  
<style scoped>
/* show shadow on hover of card */
.card:hover {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
    transition: all 0.3s cubic-bezier(0.3, 0, 0, 1.3);
}

/* button {
    background-color: var(--primary-color);
    color: var(--btn-color);
    width: 100%;
} */

.card-text {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    /* number of lines to display before truncating */
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
    overflow: hidden;
}
</style>