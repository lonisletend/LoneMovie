<template>
  <div>
    <section>
      <b-field grouped group-multiline>
        <b-button type="is-primary is-light" size="is-small">
          {{ state.roomInfo ? state.roomInfo.name : "" }}
        </b-button>
        <b-button
          type="is-success is-light"
          size="is-small"
          class="margin-left-10"
          @click="copyLink"
        >
          复制链接
        </b-button>
      </b-field>
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
import "videojs-contrib-hls";

import { store } from "@/store";
import { getRoom } from "@/api";

window.videojs = videojs;

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
      // room Info
      state: store.state,
      joinForm: {
        id: null,
        password: null,
        key: null,
        username: null,
      },
    };
  },
  computed: {},
  beforeMount() {
    console.log(this.$route.query);
    // console.log(this.roomInfo);
    this.joinForm = this.$route.query;
    this.init_room();
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
    init_room() {
      if (!this.joinForm.id || !this.joinForm.key) {
        this.$router.push({ path: "/", query: this.joinForm });
        return;
      }
      if (this.joinForm.username) {
        this.getAndJoinRoom();
      } else {
        this.$buefy.dialog.prompt({
          message: `完善用户名:`,
          inputAttrs: {
            placeholder: "e.g. Walter",
            maxlength: 10,
          },
          trapFocus: true,
          onConfirm: (value) => {
            this.joinForm.username = value;
            this.getAndJoinRoom();
          },
          onCancel: () => {
            console.log(this.joinForm);
            this.$router.push({ path: "/", query: this.joinForm });
          },
        });
      }
    },
    joinRoom() {
      // 校验form
      this.getAndJoinRoom();
    },
    getAndJoinRoom() {
      getRoom(this.joinForm).then((res) => {
        if (res.data.code === 0) {
          console.log("res => ", res.data.data);
          let roomInfo = res.data.data;
          roomInfo.sharedLink =
            location.protocol +
            "//" +
            location.host +
            "/#/room" +
            "?id=" +
            roomInfo.id +
            "&key=" +
            roomInfo.key;
          store.setRoomInfo(roomInfo);
          // Join Room.
        } else {
          this.$buefy.notification.open({
            message: res.data.code + ": " + res.data.msg,
            position: "is-top",
            type: "is-danger",
          });
        }
      });
    },
    onPlayerPlay(player) {
      console.log(player);
    },
    onPlayerPause(player) {
      console.log(player);
    },
    copyLink() {
      console.log(this.state.roomInfo.sharedLink);
      this.$buefy.notification.open({
        message: "复制成功, 快去分享给小伙伴吧!",
        position: "is-top",
        type: "is-success",
      });
    },
  },
};
</script>

<style scoped>
.margin-left-10 {
  margin-left: 10px;
}
</style>
