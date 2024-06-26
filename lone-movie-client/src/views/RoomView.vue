<template>
  <div>
    <section>
      <b-field grouped group-multiline>
        <b-button type="is-primary is-light" size="is-small">
          房间名: {{ state.roomInfo ? state.roomInfo.name : "" }}
        </b-button>
        <b-button
          type="is-success is-light"
          size="is-small"
          class="margin-left-10"
          @click="testVideo"
        >
          测试视频
        </b-button>
        <b-button
          type="is-success is-light"
          size="is-small"
          class="margin-left-10"
          @click="syncSource"
        >
          同步播放源
        </b-button>
        <b-button
          type="is-success is-light"
          size="is-small"
          class="margin-left-10"
          @click="copyLink"
        >
          分享房间
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
  sockets: {
    connect: function () {
      console.log(" ==> socket connected");
    },
    customEmit: function (data) {
      console.log(
        data +
          "this method was fired by the socket server. eg: io.emit('customEmit', data)"
      );
    },
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
      synced: false,
      currTime: 0,
    };
  },
  computed: {},
  beforeMount() {
    console.log(this.$route.query);
    // console.log(this.roomInfo);
    this.joinForm = this.$route.query;
    this.joinForm.id = Number(this.joinForm.id);
    this.init_room();
  },
  mounted() {
    console.log(" ==> mounted");
    this.$socket.client.on("notice", (ret) => {
      console.log("[EVENT: (notice)] ==> ", ret);
      this.$buefy.notification.open({
        message: ret.msg,
        position: "is-top",
        type: ret.code === 0 ? "is-success" : "is-danger",
      });
    });
    this.$socket.client.on("syncSource", (ret) => {
      console.log("[EVENT: (syncSource)] ==> ", ret);
      this.source = ret.data;
      this.$buefy.notification.open({
        message: "播放源已同步!",
        position: "is-top",
        type: ret.code === 0 ? "is-success" : "is-danger",
      });
    });
    this.$socket.client.on("syncPlay", (ret) => {
      console.log("syncPlay ==> ", ret);
      this.synced = !this.synced;
      this.currTime = ret.data;
      console.log("videoPlayer ==> ", this.$refs);
      this.$refs.videoPlayer.player.play();
    });
    this.$socket.client.on("syncPause", (ret) => {
      console.log("syncPause ==> ", ret);
      this.synced = !this.synced;
      this.currTime = ret.data;
      this.$refs.videoPlayer.player.pause();
    });
  },
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
      // Join socket room
      this.$socket.client.emit("join", this.joinForm);
    },
    getAndJoinRoom() {
      getRoom(this.joinForm).then((res) => {
        if (res.data.code === 0) {
          console.log("res => ", res.data.data);
          let roomInfo = res.data.data;
          roomInfo.id = Number(roomInfo.id);
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
          this.source = roomInfo.source;
          // Join Room.
          this.joinRoom();
        } else {
          this.$buefy.notification.open({
            message: res.data.code + ": " + res.data.msg,
            position: "is-top",
            type: "is-danger",
          });
        }
      });
    },
    syncSource() {
      let sourceParam = {
        id: this.state.roomInfo.id,
        key: this.state.roomInfo.key,
        source: this.source,
      };
      this.$socket.client.emit("syncSource", sourceParam);
    },
    // listen event
    onPlayerPlay(player) {
      console.log("synced ===> ", this.synced);
      if (this.synced) {
        console.log(" ==> sync play! currTime ==> ", this.currTime);
        player.currentTime(this.currTime);
        this.synced = false;
      } else {
        console.log("player play! currTime ==> ", player.currentTime());
        this.synced = true;
        let syncParam = {
          id: this.state.roomInfo.id,
          key: this.state.roomInfo.key,
          currTime: player.currentTime(),
        };
        this.$socket.client.emit("syncPlay", syncParam);
      }
    },
    onPlayerPause(player) {
      console.log("synced ===> ", this.synced);
      if (this.synced) {
        console.log(" ==> sync pause! currTime ==> ", this.currTime);
        player.currentTime(this.currTime);
        this.synced = false;
      } else {
        console.log("player pause! currTime ==> ", player.currentTime());
        this.synced = true;
        let syncParam = {
          id: this.state.roomInfo.id,
          key: this.state.roomInfo.key,
          currTime: player.currentTime(),
        };
        this.$socket.client.emit("syncPause", syncParam);
      }
    },
    copyLink() {
      console.log(this.state.roomInfo.sharedLink);
      this.$clipboard(this.state.roomInfo.sharedLink);
      this.$buefy.notification.open({
        message: "分享链接复制成功, 快去分享给小伙伴吧!",
        position: "is-top",
        type: "is-success",
      });
    },
    testVideo() {
      this.source = "http://vjs.zencdn.net/v/oceans.mp4";
    },
  },
};
</script>

<style scoped>
.margin-left-10 {
  margin-left: 10px;
}
</style>
