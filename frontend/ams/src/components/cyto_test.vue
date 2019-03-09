<template>
  <div id="holder">
    <div id="cy"></div>
  </div>
</template>

<script>
import cytoscape from "cytoscape";
// let cyto = require("./cytocomponent.js");
let cy = (window.cy = cytoscape({ container: document.getElementById("cy") }));
export default {
  methods: {
    cyUpdate() {
      const requests = [
        this.axios({
          url: "http://127.0.0.1:5000/api/node/",
          headers: this.auth_header,
          method: "get"
        }),
        this.axios({
          url: "http://127.0.0.1:5000/api/link/",
          headers: this.auth_header,
          method: "get"
        }),
        this.axios({
          url: "http://127.0.0.1:5000/api/relationship/",
          headers: this.auth_header,
          method: "get"
        }),
        this.axios({
          url: "http://127.0.0.1:5000/api/label/",
          headers: this.auth_header,
          method: "get"
        })
      ];
      Promise.all(requests).then(values => {});
    }
  }
};
</script>


<style>
#holder {
  width: 100%;
  height: 95.8%;
  position: absolute;
  background-color: #cfd8dc;
}
</style>
