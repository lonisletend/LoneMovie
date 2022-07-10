<template>
  <div>
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
</template>

<script>
import { createRoom } from "@/api";
import { store } from "@/store";

export default {
  name: "IndexView",
  data() {
    return {
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
    };
  },
  beforeMount() {
    console.log(this.$route);
    let query = this.$route.query;
    if (!query) {
      this.joinForm = query;
    }
  },
  methods: {
    clear(form, attr) {
      this[form][attr] = null;
    },
    create() {
      console.log(this.createForm);
      createRoom(this.createForm).then((res) => {
        if (res.data.code === 0) {
          let roomInfo = res.data.data;
          roomInfo.id = Number(roomInfo.id);
          store.setRoomInfo(roomInfo);
          let query = {
            id: roomInfo.id,
            key: roomInfo.key,
            username: this.createForm.username,
          };
          this.$router.push({ name: "room", query: query });
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
  },
};
</script>

<style scoped></style>
