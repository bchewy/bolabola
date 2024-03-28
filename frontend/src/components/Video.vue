<template>
  <video-player
    class="video-player vjs-big-play-centered"
    :src="src"
    poster="/images/poster/oceans.png"
    crossorigin="anonymous"
    playsinline
    controls
    autoplay
    :volume="0.6"
    :height="320"
    @mounted="handleMounted"
    @ready="handleEvent($event)"
    @play="handleEvent($event)"
    @pause="handleEvent($event)"
    @ended="handleEvent($event)"
    @loadeddata="handleEvent($event)"
    @waiting="handleEvent($event)"
    @playing="handleEvent($event)"
    @canplay="handleEvent($event)"
    @canplaythrough="handleEvent($event)"
    @timeupdate="handleTimestamp(player?.currentTime())"
  />
</template>

<script lang="ts">
  import { defineComponent, shallowRef, onMounted, onBeforeUnmount, reactive } from "vue";
  import { VideoPlayer } from "@videojs-player/vue";
  import videojs from "video.js";
  import "video.js/dist/video-js.css";
  import EventItem from "@/views/EventItem.vue";
  import { isExecutionPatchIncrementalResult } from "@apollo/client/utilities";

  type VideoJsPlayer = ReturnType<typeof videojs>;

  export default defineComponent({
    name: "vue-basic-player",
    title: "Basic player (Vue)",
    url: "",
    components: {
      VideoPlayer,
    },
    props: ["src", "playNow"],
    data() {
      return {
        lastEmittedTime: 0,
      }
    },
    setup(props, { emit }) {
      const player = shallowRef<VideoJsPlayer>();
      const state = reactive({
        lastEmittedTime: 0,
      });

      const handleTimeUpdate = () => {
        if (player.value) {
          // emit('video-timestamp', player.value.currentTime());
        }
      };

      onMounted(() => {
        player.value.on('timeupdate', handleTimeUpdate);
      });

      onBeforeUnmount(() => {
        if (player.value) {
          player.value.off('timeupdate', handleTimeUpdate);
        }
      });

      const handleMounted = (payload: any) => {
        player.value = payload.player;
        if (props.playNow) {
          player.value.play();
        }
        console.log("Basic player mounted:", payload);
      };

      const handleEvent = (log: any) => {
        console.log("Basic player event", log);
      };

      const handleTimestamp = (time: number) => {
        const roundedTime = Math.round(time);
        if (roundedTime === state.lastEmittedTime) {
          return;
        }
        state.lastEmittedTime = roundedTime;
        emit("video-timestamp", roundedTime);
      };

      return { player, handleMounted, handleEvent, handleTimestamp };
    },
  });
</script>

<!-- <style lang="scss" scoped>
    @import '@/styles/variables.scss';
    @import '@/styles/mixins.scss'; -->
<!--   
    .video-player {
      background-color: $black;
      width: 100%;
    } -->
<!-- </style> -->
