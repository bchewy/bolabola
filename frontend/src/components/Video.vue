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
    @timeupdate="handleEvent(player?.currentTime())"
  />
</template>

<script lang="ts">
  import { defineComponent, shallowRef } from "vue";
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
    setup(props) {
      const player = shallowRef<VideoJsPlayer>();
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

      return { player, handleMounted, handleEvent };
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
