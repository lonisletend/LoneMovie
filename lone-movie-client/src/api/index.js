import axios from "axios";

axios.defaults.withCredentials = true;

const ROOM_URL = "http://localhost:5000/room";
const URLS = {
  room: ROOM_URL,
};

export function createRoom(roomInfo) {
  return axios.post(`${ROOM_URL}/create`, roomInfo);
}

export function getRoom(query) {
  return axios.post(`${ROOM_URL}/get`, query);
}
export { URLS };
