<template>
  <div id="holder">
    <cytoscape :config="config" :preConfig="preConfig"></cytoscape>
  </div>
</template>


<script>
import automove from "cytoscape-automove";
import cola from "cytoscape-cola";
export default {
  data() {
    return {
      config: {
        autounselectify: true,
        panningEnabled: true,
        boxSelectionEnabled: false,
        layout: {
          name: "cola"
        },
        style: [
          {
            selector: "node",
            style: {
              shape: "hexagon",
              "background-color": "red",
              label: "data(name)"
            }
          },
          {
            selector: "edge",
            css: {
              "line-color": "#f92411"
            }
          }
        ]
      }
    };
  },
  methods: {
    cyUpdate() {
      var nodes = [];
      var links = [];
      var labels = [];
      this.$cytoscape.instance.then(cy => {
        this.axios
          .get("http://127.0.0.1:5000/api/node/")
          .then(
            response => {
              nodes = response.data["data"];
              //   console.log(response.data["data"][i]["node_id"]);
              for (var i = 0; i < response.data["data"].length; i++) {
                var py = i * 2 + 10;
                var px = i * 2 + 10;
                cy.add({
                  group: "nodes",
                  data: {
                    id: response.data["data"][i]["node_id"],
                    name: response.data["data"][i]["type"],
                    locked: false
                  }
                });
              }
            },
            this.axios.get("http://127.0.0.1:5000/api/link/").then(response => {
              for (var i = 0; i < response.data["data"].length; i++) {
                links = response.data["data"];
                cy.add({
                  group: "edges",
                  data: {
                    id: "l" + response.data["data"][i]["link_id"],
                    source: response.data["data"][i]["node_id_1"],
                    target: response.data["data"][i]["node_id_2"]
                  }
                });
              }
            })
          )
          .catch(error => console.log(error));
      });
    },
    preConfig(cytoscape) {
      console.log("calling pre-config");
      // cytoscape: this is the cytoscape constructor
      cytoscape.use(cola);
      cytoscape.use(automove);
    }
  },
  mounted: function() {
    this.$nextTick(this.cyUpdate);
  }
};
</script>

<style>
#holder {
  width: 100%;
  height: 100%;
  position: absolute;
  right: 25%;
}
</style>
