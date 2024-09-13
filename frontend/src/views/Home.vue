<template>
  <header>
    <!-- nav -->
  </header>
  <div class="container-fluid p-0 scroll-container bg-image pb-5">
    <section>
      <NavBar />
      <div class="text-light text-center d-flex align-items-center justify-content-center"
        style="background-image: url('/src/assets/background2.png'); background-size: cover; background-position: center; height: 100vh; opacity: 0.85">
        <div class="container">
          <div class="d-sm-flex align-items-center justify-content-center"> <!-- Center vertically and horizontally -->
            <div class="text-center">
              <h1><span class="text-superblue element">TicketBoost</span></h1>
              <p class="lead text-dark">
                Discover and book tickets for your favorite football events with TicketBoost. <br>Get access to
                exclusive deals
                and enjoy a seamless ticketing experience.
              </p>
              <button class="btn btn-primary gradient-button1" @click="$router.push('/events')">Get
                Started</button>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
  <!-- <Footer /> -->
</template>

<script>
import NavBar from '../components/Navbar.vue';
import { useAuth0 } from '@auth0/auth0-vue';
// import LearnMore from '../components/LearnMore.vue';
import { ref } from 'vue';
import Typed from 'typed.js';
// import Footer from '../components/Footer.vue'

export default {
  name: 'Home',
  data() {
    return {
      isTypedInitialized: false

    };
  },
  components: {
    NavBar,
    // LearnMore,
    // Footer,
  },
  mounted() {
    const element = document.querySelector('.element');
    const cursors = document.querySelectorAll('.typed-cursor');
    cursors.forEach(cursor => cursor.remove());  // Remove existing cursors

    if (!this.isTypedInitialized) {
      new Typed(element, {
        strings: ["Where Every Seat Tells a Story: Get Your Ticket Now!", "Your Ticket to the Ultimate Football Experience!", "Feel the Pulse of the Game: Secure Your Ticket Today!", "Score Your Seats, Secure Your Spot!"],
        typeSpeed: 50,
        backSpeed: 50,
        loop: true
      });
      this.isTypedInitialized = true;
    }
  },
  setup() {

    const { loginWithRedirect, user, isAuthenticated } = useAuth0();
    const cards = [
      {
        icon: "fa-solid fa-leaf",
        title: "Eco-friendly Navigation",
        description: "Navigate with a conscience! Discover a greener way to plan your journeys.",
        details: "Experience eco-friendly navigation that goes beyond the usual routes. Our app empowers you to make sustainable choices, reduce your carbon footprint, and explore eco-conscious alternatives. Discover routes that prioritize public transport, carpooling, biking, and walking while offering insights into your environmental impact. With us, every journey is a step towards a cleaner, greener future.",
        variant: "success",
      },
      {
        icon: "fa-solid fa-shoe-prints",
        title: "Traffic Optimization",
        description: "Efficient routes, cleaner air. Optimize traffic for a greener planet.",
        details: "Traffic Optimization is about more than just getting from A to B. It's about creating a sustainable future. Our app intelligently manages traffic to minimize congestion and emissions. By prioritizing eco-friendly modes of transport and offering real-time traffic insights, we help you reduce your carbon footprint and contribute to cleaner, healthier communities. Discover the details behind our innovative traffic solutions and take a step towards a more sustainable world.",
        variant: "success",
      },
      {
        icon: "fa-solid fa-bus",
        title: "Incentivising Public Transport",
        description: "Unlock rewards while saving the environment. Embrace public transport with badges.",
        details: "Our 'Incentivising Public Transport' feature revolutionizes the way you commute. We believe that public transport should not only be convenient but also rewarding. Our badge system encourages you to choose eco-friendly options like buses, subways, and trams. Each journey you make brings you closer to earning valuable rewards, while collectively we make our cities cleaner and greener. Learn more about how we're making public transport an attractive choice for you and a better choice for the planet.",
        variant: "success",
      },
    ];

    const currentCardIndex = ref(-1); // Track the currently selected card

    const openModal = (index) => {
      currentCardIndex.value = index;
    };

    const closeModal = () => {
      currentCardIndex.value = -1;
    };

    return {
      login: async () => {
        try {
          await loginWithRedirect();
        } catch (e) {
          alert('Failed to login');
          console.error('Failed to login:', e);
        }
      },
      cards,
      currentCardIndex,
      openModal,
      closeModal,
      isAuthenticated,
      user,
    }
  },
};
</script>


<style scoped>
/* Other component-specific styles */
.bg-image {
  background-image: url('https://s3.ap-southeast-1.amazonaws.com/esd-assets.bchwy.com/Stage.png');
  /* background-image: url('https://bchewy-images.s3.ap-southeast-1.amazonaws.com/plan-it/planit.png'); */
  background-size: cover;
  background-repeat: no-repeat;
}

.news-input {
  width: 50%;
  /* Set the width to 50% */
}

.bg-supergreen {
  background-color: #739072;
}

.bg-superblue {
  background-color: #749db6;
}

.beige-colour {
  /* background-color: ; */
  background-color: #ECE3CE;
}

.text-supergreen {
  color: #a7c957;
}

.text-superblue {
  /* color: lightblue; */
  color: #5356FF;
}

.light-green {
  background-color: #d1f4d1
}

.gradient-button1 {
  background-image: linear-gradient(to right, #67C6E3, #5356FF);
}
</style>