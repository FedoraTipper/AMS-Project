<template>
  <div id="holder">
    <div id="cy" ref="cy"></div>
  </div>
</template>
<script>
// import cytocomponent from "./cytocomponent";
import cytoscape from "cytoscape";
let expandCollapse = require("cytoscape-expand-collapse");
import cosebilkent from "cytoscape-cose-bilkent";
let jquery = require("jquery");
export default {
  data() {
    return {
      modal_node_show: false,
      modal_link_show: false,
      modal_metadata_show: false,
      search_show: false,
      form: {
        node_type: "",
        node_type_1: "",
        node_type_2: "",
        node_label: "",
        link_label: "",
        new_node_type: "",
        links_name: "",
        relationship: "",
        NDataType: "",
        NDataCollection: ""
      },
      auth_header: {
        Authorization: localStorage.getItem("Authorization")
      },
      labels_form: [],
      nodes_form: [],
      links_form: [],
      relationship_form: [],
      labels_dict: {},
      nodes_dict: {},
      links_dict: {},
      relationship_dict: {}
    };
  },
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

      Promise.all(requests).then(values => {
        let nodes = [];
        let links = [];
        let relationships = {};
        nodes = values[0].data["data"];
        links = values[1].data["data"];
        let relation_response = values[2].data["data"];
        for (var i = 0; i < relation_response.length; i++) {
          this.relationship_form.push(relation_response[i]["message"]);
          this.relationship_dict[relation_response[i]["message"]] =
            relation_response[i]["relationship_id"];
          relationships[relation_response[i]["relationship_id"]] =
            relation_response[i]["message"];
        }

        let labels = values[3].data["data"];
        let labels_dict_2 = {};
        for (var i = 0; i < labels.length; i++) {
          this.labels_form.push(labels[i]["label_text"]);
          labels_dict_2[labels[i]["label_id"]] = labels[i]["label_text"];
          this.labels_dict[labels[i]["label_text"]] = labels[i]["label_id"];
        }

        window.cy.add({
          group: "nodes",
          data: {
            id: "b",
            name: "collectiuon"
          }
        });

        for (var i = 0; i < nodes.length; i++) {
          this.nodes_form.push(nodes[i]["type"]);
          if (this.labels_dict[nodes[i]["label_id"]]) {
            this.nodes_dict[nodes[i]["type"]] = {
              nodes_id: nodes[i]["node_id"],
              label_id: this.labels_dict[nodes[i]["label_id"]]
            };
          } else {
            this.nodes_dict[nodes[i]["type"]] = {
              nodes_id: nodes[i]["node_id"]
            };
          }

          window.cy.add({
            group: "nodes",
            data: {
              id: nodes[i]["node_id"],
              name: nodes[i]["type"],
              parent: "b",
              label_collection: labels_dict_2[nodes[i]["label_id"]]
            }
          });
        }
        for (var i = 0; i < links.length; i++) {
          let link_name = "";
          if (relationships[links[i]["relationship_id"]]) {
            link_name =
              "(l" +
              links[i]["link_id"] +
              ") " +
              relationships[links[i]["relationship_id"]];
          } else {
            link_name = "(l" + links[i]["link_id"] + ") ";
          }
          this.links_form.push(link_name);
          this.links_dict[link_name] = links[i]["link_id"];

          window.cy.add({
            group: "edges",
            data: {
              id: "l" + links[i]["link_id"],
              source: links[i]["node_id_1"],
              target: links[i]["node_id_2"],
              name: link_name
            }
          });
          window.cy.layout({ name: "cose-bilkent" }).run();
        }
      });
    }
  },
  mounted: function() {
    //this.$nextTick(this.cyUpdate);
    expandCollapse(cytoscape, jquery);
    // cytoscape.use(expandCollapse);
    cytoscape.use(cosebilkent);

    let cy = (window.cy = cytoscape({
      container: document.getElementById("cy"),
      layout: {
        name: "cose-bilkent"
      },
      style: [
        {
          selector: "node",
          style: {
            shape: "hexagon",
            "background-color": "#0d47a1",
            label: "data(name)"
          }
        },
        {
          selector: "edge",
          style: {
            "line-color": "#42a5f5",
            label: "data(name)"
          }
        },
        {
          selector: "node.cy-expand-collapse-collapsed-node",
          style: {
            "background-color": "darkblue",
            shape: "rectangle"
          }
        },
        {
          selector: ":parent",
          style: {
            "background-opacity": 0.333
          }
        },
        {
          selector: "edge[name]",
          style: {
            label: "data(name)"
          }
        },
        {
          selector: ":selected",
          style: {
            "border-width": 3,
            "border-color": "#DAA520"
          }
        }
      ]
    }));
    let api = "";
    try {
      api = window.api = cy.expandCollapse({
        layoutBy: {
          name: "cose-bilkent",
          animate: "end",
          randomize: false,
          fit: true
        },
        fisheye: true,
        animate: true,
        undoable: false
      });
    } catch {
      api = window.api = cy.expandCollapse({
        layoutBy: {
          name: "cose-bilkent",
          animate: "end",
          randomize: false,
          fit: true
        },
        fisheye: true,
        animate: true,
        undoable: false
      });
    }

    document.querySelectorAll("canvas").forEach(canvas => {
      canvas.style.left = "0";
    });
    this.$nextTick(this.cyUpdate);
    cy.layout({ name: "cose-bilkent" }).run();
    api.collapseAll();
  }
};
</script>


<style>
#holder {
  width: 100%;
  height: 95.8%;
  position: absolute;
  background-color: #cfd8dc;
  float: left;
  left: 0px;
}
#cy {
  z-index: 999;
  width: 100%;
  height: 95.8%;
  float: left;
  left: 0px;
}
</style>
