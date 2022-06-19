import Vue from "vue";
import VueRouter from "vue-router";
import IndexView from "@/views/IndexView";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "index",
    component: IndexView,
  },
  {
    path: "/room",
    name: "room",
    component: () => import("@/views/RoomView"),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
