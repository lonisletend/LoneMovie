import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import Buefy from "buefy";
import VueVideoPlayer from "vue-video-player";
import Clipboard from "v-clipboard";
import VueSocketIOExt from "vue-socket.io-extended";
import { io } from "socket.io-client";

import "buefy/dist/buefy.css";
import "video.js/dist/video-js.css";

Vue.config.productionTip = false;
Vue.use(Buefy);
Vue.use(VueVideoPlayer);
Vue.use(Clipboard);
const socket = io("http://192.168.50.103:5000");
Vue.use(VueSocketIOExt, socket);

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
