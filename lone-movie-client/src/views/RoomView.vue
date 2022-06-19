<template>
  <div>
    <section>
      <b-field>
        <b-input
          placeholder="输入播放源(支持MP4, M3U8)"
          v-model="source"
        ></b-input>
      </b-field>
    </section>
    <video-player
      v-show="visible"
      class="vjs-custom-skin"
      ref="videoPlayer"
      :options="playerOptions"
      :playsinline="true"
      @play="onPlayerPlay($event)"
      @pause="onPlayerPause($event)"
    >
    </video-player>
  </div>
</template>

<script>
import "video.js/dist/video-js.css";
import "vue-video-player/src/custom-theme.css";

import { videoPlayer } from "vue-video-player";
import videojs from "video.js";

window.videojs = videojs;
// hls plugin for videojs6
import "videojs-contrib-hls";

export default {
  name: "RoomView",
  components: {
    videoPlayer,
  },
  data() {
    return {
      visible: false,
      playerOptions: {
        visible: false,
        height: "360",
        playbackRates: [0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
        sources: [
          {
            withCredentials: false,
            type: "video/mp4",
            src: "http://vjs.zencdn.net/v/oceans.mp4",
          },
        ],
        flash: { hls: { withCredentials: false } },
        html5: { hls: { withCredentials: false } },
        poster:
          "https://surmon-china.github.io/vue-quill-editor/static/images/surmon-5.jpg",
      },
      source: null,
    };
  },
  computed: {},
  beforeMount() {
    console.log(this.$route.query);
  },
  mounted() {},
  watch: {
    source(val) {
      console.log(val);
      if (!val) {
        this.$buefy.notification.open({
          message: "请维护播放源!",
          type: "is-danger",
        });
      }
      let srcArr = val.split(".");
      let type = srcArr[srcArr.length - 1];
      console.log("type ==> ", type);
      if (type === "mp4" || type === "MP4") {
        this.playerOptions.sources[0].type = "video/mp4";
        this.playerOptions.sources[0].src = val;
        this.visible = true;
      } else if (type === "m3u8" || type === "M3U8") {
        console.log("type ==> ", type);
        this.playerOptions.sources[0].type = "application/x-mpegURL";
        this.playerOptions.sources[0].src = val;
        this.visible = true;
      } else {
        this.$buefy.notification.open({
          message: "暂时只支持MP4, M3U8!",
          type: "is-danger",
        });
        this.visible = false;
      }
      console.log(JSON.stringify(this.playerOptions));
    },
  },
  methods: {
    onPlayerPlay(player) {
      console.log(player);
    },
    onPlayerPause(player) {
      console.log(player);
    },
  },
};
</script>

<style scoped></style>
