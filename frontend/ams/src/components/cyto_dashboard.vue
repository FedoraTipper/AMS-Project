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
            style: {
              "line-color": "#f92411",
              label: "data(name)"
            }
          }
        ]
      }
    };
  },
  methods: {
    cyUpdate() {
      this.$cytoscape.instance.then(cy => {
        let nodes = [];
        let links = [];
        let relationships = {};
        let relationship_dict = {};
        const auth_header = {
          Authorization: localStorage.getItem("Authorization")
        };
        const requests = [
          this.axios({
            url: "http://127.0.0.1:5000/api/node/",
            headers: auth_header,
            method: "get"
          }),
          this.axios({
            url: "http://127.0.0.1:5000/api/link/",
            headers: auth_header,
            method: "get"
          }),
          this.axios({
            url: "http://127.0.0.1:5000/api/relationship/",
            headers: auth_header,
            method: "get"
          })
        ];
        Promise.all(requests).then(values => {
          nodes = values[0].data["data"];
          links = values[1].data["data"];
          let relation_response = values[2].data["data"];
          for (var i = 0; i < relation_response; i++) {
            relationships[relation_response[i]["relationship_id"]] =
              relation_response[i]["message"];
          }

          for (var i = 0; i < nodes.length; i++) {
            console.log("b");
            var py = i * 2 + 10;
            var px = i * 2 + 10;
            cy.add({
              group: "nodes",
              data: {
                id: nodes[i]["node_id"],
                name: nodes[i]["type"],
                locked: false
              }
            });
          }
          for (var i = 0; i < links.length; i++) {
            console.log("c");
            cy.add({
              group: "edges",
              data: {
                id: "l" + links[i]["link_id"],
                source: links[i]["node_id_1"],
                target: links[i]["node_id_2"],
                label: relationships[links[i]["relationship_id"]]
              }
            });
          }
        });
        // console.log("a");
        // console.log(nodes.length);
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
    document.querySelectorAll("canvas").forEach(canvas => {
      canvas.style.left = "0";
    });
    this.$nextTick(this.cyUpdate);
  }
};
</script>

<style>
#holder {
  width: 100%;
  height: 100%;
  position: absolute;
}
</style>
