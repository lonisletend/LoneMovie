const store = {
  debug: false,
  state: {
    auth: false,
    group: null,
    user: {},
    roomInfo: null,
  },
  setAuth(auth) {
    this.state.auth = auth;
  },
  setGroup(group) {
    this.state.group = group;
  },
  setUser(user) {
    this.state.user = user;
  },
  setRoomInfo(roomInfo) {
    this.state.roomInfo = roomInfo;
  },
};

export { store };
