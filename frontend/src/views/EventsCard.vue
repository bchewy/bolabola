<template>
    <div class="container-fluid mt-3">
    <div class="card h-100 position-relative" style="min-width: 18rem;">
        <div class="card-body">
            <h5 class="card-title">Manchester United vs Liverpool</h5>
            <!-- <p class="card-text" style="color: var(--primary-color)">
              <span v-for="tag in project.tags">#{{ tag }}&nbsp</span>
          </p> -->
            <div class="card-subtitle mb-2">Date: October 23, 2023, 8:00 PM</div>
            <p class="card-text description">
                Venue: Old Trafford Stadium, Manchester, England <br>
                Competition: English Premier League
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