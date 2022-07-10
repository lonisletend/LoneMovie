<template>
  <div>
    <div v-show="type === 'Index'">
      <section>
        <b-tabs
          v-model="activeTab"
          type="is-toggle"
          position="is-centered"
          expanded
        >
          <b-tab-item label="创建房间">
            <div class="container is-fluid">
              <section>
                <b-field>
                  <b-input
                    placeholder="房间名称"
                    icon-right="close-circle"
                    icon-right-clickable
                    @icon-right-click="clear('createForm', 'name')"
                    v-model="createForm.name"
                  ></b-input>
                </b-field>
                <b-field>
                  <b-input
                    placeholder="房间密码"
                    type="password"
                    password-reveal
                    icon-right="close-circle"
                    icon-right-clickable
                    @icon-right-click="clear('createForm', 'password')"
                    v-model="createForm.password"
                  ></b-input>
                </b-field>
                <b-field>
                  <b-input
                    placeholder="用户名"
                    icon-right="close-circle"
                    icon-right-clickable
                    @icon-right-click="clear('createForm', 'username')"
                    v-model="createForm.username"
                  >
                  </b-input>
                </b-field>
                <b-button type="is-primary is-light" expanded @click="create">
                  创建
                </b-button>
              </section>
            </div>
          </b-tab-item>
          <b-tab-item label="加入房间">
            <div class="container is-fluid">
              <section>
                <b-field>
                  <b-input
                    placeholder="房间ID"
                    icon-right="close-circle"
                    icon-right-clickable
                    @icon-right-click="clear('joinForm', 'id')"
                    v-model="joinForm.id"
                  ></b-input>
                </b-field>
                <b-field>
                  <b-input
                    placeholder="房间密码"
                    type="password"
                    password-reveal
                    icon-right="close-circle"
                    icon-right-clickable
                    @icon-right-click="clear('joinForm', 'password')"
                    v-model="joinForm.password"
                  ></b-input>
                </b-field>
                <b-field>
                  <b-input
                    placeholder="用户名"
                    icon-right="close-circle"
                    icon-right-clickable
                    @icon-right-click="clear('joinForm', 'username')"
                    v-model="joinForm.username"
                  >
                  </b-input>
                </b-field>
                <b-button type="is-primary is-light" expanded @click="join">
                  加入
                </b-button>
              </section>
            </div>
          </b-tab-item>
          <b-tab-item label="关于">关于</b-tab-item>
        </b-tabs>
      </section>
    </div>
    <div v-show="type === 'Room'">
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
            @click="copyLink"
          >
            分享房间
          </b-button>
          <b-button
            type="is-success is-light"
            size="is-small"
            class="margin-left-10"
            @click="echo"
          >
            ECHO
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
  </div>
</template>

<script>
import "video.js/dist/video-js.css";
import "vue-video-player/src/custom-theme.css";
import { videoPlayer } from "vue-video-player";
import videojs from "video.js";
import "videojs-contrib-hls";
import { createRoom, getRoom } from "@/api";
import { store } from "@/store";

window.videojs = videojs;

export default {
  name: "IndexView",
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
      type: "Index",
      // Index
      activeTab: 0,
      createForm: {
        name: null,
        password: null,
        username: null,
      },
      joinForm: {
        id: null,
        password: null,
        username: null,
      },

      // Room
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
      joinParam: {
        id: null,
        password: null,
        key: null,
        username: null,
      },
    };
  },
  beforeMount() {
    console.log(this.$route);
    // let paramLength = Object.keys(this.$route.query).length;
    // if (paramLength === 0) {
    //   this.type = "Index";
    // } else if (paramLength > 0) {
    //   this.type = "Room";
    //   this.joinParam = this.$route.query;
    //   this.init_room();
    // } else {
    //   this.$router.push({ name: "index" });
    // }
  },
  mounted() {
    console.log(" ==> mounted");

    let paramLength = Object.keys(this.$route.query).length;
    if (paramLength === 0) {
      this.type = "Index";
    } else if (paramLength > 0) {
      this.type = "Room";
      this.joinParam = this.$route.query;
      this.joinParam.id = Number(this.joinParam.id);
      this.init_room();
    } else {
      this.$router.push({ name: "index" });
    }

    this.$socket.client.on("notice", (ret) => {
      console.log("[EVENT: (notice)] ==> ", ret);
      this.$buefy.notification.open({
        message: ret.msg,
        position: "is-top",
        type: ret.code === 0 ? "is-success" : "is-danger",
      });
    });
    this.$socket.client.on("echo", (ret) => {
      console.log("[EVENT: (echo)] ==> ", ret);
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
    clear(form, attr) {
      this[form][attr] = null;
    },
    getSharedLink(roomInfo) {
      return (
        location.protocol +
        "//" +
        location.host +
        "/#/" +
        "?id=" +
        roomInfo.id +
        "&key=" +
        roomInfo.key
      );
    },
    create() {
      console.log(this.createForm);
      createRoom(this.createForm).then((res) => {
        if (res.data.code === 0) {
          let roomInfo = res.data.data;
          this.joinParam = {
            id: roomInfo.id,
            key: roomInfo.key,
            username: this.createForm.username,
          };
          this.type = "Room";
          this.init_room();
        } else {
          this.$buefy.notification.open({
            message: res.data.code + ": " + res.data.msg,
            position: "is-top",
            type: "is-danger",
          });
        }
      });
    },
    join() {
      console.log(this.joinForm);
    },
    init_room() {
      if (!this.joinParam.id || !this.joinParam.key) {
        this.type = "Index";
        return;
      }
      if (this.joinParam.username) {
        this.getAndJoinRoom();
      } else {
        this.$buefy.dialog.prompt({
          message: `完善用户名:`,
          inputAttrs: {
            placeholder: "e.g. Kevin",
            maxlength: 10,
          },
          trapFocus: true,
          onConfirm: (value) => {
            this.joinParam.username = value;
            this.getAndJoinRoom();
          },
          onCancel: () => {
            console.log(this.joinParam);
            this.type = "Index";
          },
        });
      }
    },
    joinRoom() {
      // Join socket room
      this.$socket.client.emit("join", this.joinParam);
    },
    getAndJoinRoom() {
      getRoom(this.joinParam).then((res) => {
        if (res.data.code === 0) {
          console.log("res => ", res.data.data);
          let roomInfo = res.data.data;
          roomInfo.sharedLink = this.getSharedLink(roomInfo);
          store.setRoomInfo(roomInfo);
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
    onPlayerPlay(player) {
      console.log(player);
    },
    onPlayerPause(player) {
      console.log(player);
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
    echo() {
      this.$socket.client.emit("echo", this.joinParam);
    },
  },
};
</script>

<style scoped>
.margin-left-10 {
  margin-left: 10px;
}
</style>
