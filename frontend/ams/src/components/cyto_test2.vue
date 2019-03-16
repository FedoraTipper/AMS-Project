<template>
  <div>
    <b-dropdown
      id="overlay-button"
      offset
      dropleft
      :text="current_view"
      variant="primary"
      class="m-md-2"
      size="lg"
    >
      <div v-for="view in view_array" :key="view.view_id" v-bind="view_array">
        <b-dropdown-item @click="change_collection(view)">{{view.name}}</b-dropdown-item>
      </div>
    </b-dropdown>

    <div id="draggabledashboard">
      <div
        id="draggablesspacing"
        v-for="type in type_array"
        :key="type.type_id"
        v-bind="type_array"
      >
        <drag
          class="drag"
          :transfer-data="{type}"
          :effect-allowed="['copy']"
          drop-effect="copy"
        >{{type.type}}</drag>
      </div>
    </div>
    <!-- Create droppable object -->
    <drop
      class="drop"
      :class="{cytodrop}"
      @dragover="cytodrop = true"
      @dragleave="cytodrop = false"
      @drop="handleDrop"
    >
      <div id="holder">
        <cytoscape :config="config" :preConfig="preConfig"></cytoscape>
      </div>
    </drop>
  </div>
</template>

<script>
import cytoscape from "cytoscape";
import edgehandle from "cytoscape-edgehandles";
import cxtmenu from "cytoscape-cxtmenu";
import { Drag, Drop } from "vue-drag-drop";
//Load cytoscapes theme config instance
let cytoscapeconfig = require("../assets/cytoscapeconfig.js");

export default {
  // Create components to allow for drag and drop
  components: {
    Drag,
    Drop
  },
  data() {
    return {
      cytodrop: false,
      type_array: [
        { type_id: "1", type: "Hello1" },
        { type_id: "2", type: "Hello2" }
      ],
      view_array: [
        { view_id: "1", name: "Countercept" },
        { view_id: "2", name: "MWR" }
      ],
      auth_header: {
        Authorization: localStorage.getItem("Authorization")
      },
      current_view: "",
      current_view_number: "",
      config: {
        panningEnabled: true,
        fit: false,
        animate: false,
        boxSelectionEnabled: false,
        style: cytoscapeconfig.config
      },
      i: 0
    };
  },
  methods: {
    preConfig(cytoscape) {
      edgehandle(cytoscape);
      cxtmenu(cytoscape);
    },
    loadModules() {
      this.$cytoscape.instance.then(cy => {
        let eh = (window.eh = cy.edgehandles({
          // Increase delay or will spawn long lasting node object
          hoverDelay: 400,
          snap: true,
          //Send to addLink function, to add the link to the database
          complete: (sourceNode, targetNode, addedEles) => {
            this.addLink(sourceNode, targetNode, addedEles);
          }
        }));
        eh.enableDrawMode();
        let menu = (window.menu = cy.cxtmenu({
          selector: "node, edge",
          commands: [
            {
              content: "Delete",
              select: element => {
                this.deleteElement(element);
              }
            },
            {
              content: "Change Label",
              select: element => {
                this.changeElement(element);
              }
            },
            {
              content: "Metadata",
              select: element => {
                this.getMetadata(element);
              }
            }
          ]
        }));
      });
    },
    addLink(sourceNode, targetNode, link) {
      let link_details = {
        node_id_1: sourceNode["_private"]["data"]["id"],
        node_id_2: targetNode["_private"]["data"]["id"],
        view_id: this.current_view_number
      };
      this.$cytoscape.instance.then(cy => {
        console.log(cy);
      });
      console.log("AAA");
      console.log(link[0]);

      // try{
      //   this.axios({
      //   url: "http://127.0.0.1:5000/api/link/",
      //   headers: this.auth_header,
      //   method: "post",
      //   data: node_details
      // }).then(response => {
      //   if (response.data["message"].includes("Success")) {
      //     let returned_id = response.data["payload"];
      //     this.$cytoscape.instance.then(cy => {
      //                 cy.remove(link)
      //     });

      //   } else {
      //     alert("Failed to create new link. " + response.data["message"]);
      //     this.$cytoscape.instance.then(cy => {
      //                 cy.remove(link)
      //     });
      //   }
      // });
      // }catch{
      //   cy.remove(link)
      // }
    },
    handleDrop(nodetype) {
      let node_details = {
        view_id: this.current_view_number,
        type_id: nodetype["type"]["type_id"]
      };
      this.axios({
        url: "http://127.0.0.1:5000/api/node/",
        headers: this.auth_header,
        method: "post",
        data: node_details
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          let returned_id = response.data["payload"];
          this.$cytoscape.instance.then(cy => {
            cy.add({
              group: "nodes",
              data: {
                id: returned_id,
                name: nodetype["type"]["type"],
                payload: {
                  type_id: nodetype["type"]["type_id"],
                  type: nodetype["type"]["type"],
                  //  Comeback to this and set the view
                  view_id: this.current_view_number
                },
                imglink: null
              }
            });
            this.cytodrop = false;
            this.update_view();
          });
        } else {
          alert("Failed to create new node. " + response.data["message"]);
        }
      });
    },
    change_collection(view) {
      this.current_view = view.name;
      this.current_view_number = view.view_id;
    },
    update_view() {
      this.$cytoscape.instance.then(cy => {
        cy.layout({ name: "circle", fit: true }).run();
        cy.center();
      });
    },
    deleteElement(element) {
      if (element["_private"]["group"] == "edges") {
        this.deleteLink(element);
      } else {
        this.deleteNode(element);
      }
    },
    changeElement(element) {
      if (element["_private"]["group"] == "edges") {
        this.deleteLink(element);
      } else {
        this.deleteNode(element);
      }
    },
    getMetadata(element) {
      if (element["_private"]["group"] == "edges") {
        this.deleteLink(element);
      } else {
        this.deleteNode(element);
      }
    },
    deleteNode(node) {
      let node_details = {
        node_id: node["_private"]["data"]["id"]
      };
      this.axios({
        url: "http://127.0.0.1:5000/api/node/",
        headers: this.auth_header,
        method: "delete",
        data: node_details
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          this.$cytoscape.instance.then(cy => {
            cy.remove(node);
          });
        } else {
          alert("Failed to delete node. " + response.data["message"]);
        }
      });
      this.update_view();
    },
    deleteLink(link) {
      this.$cytoscape.instance.then(cy => {
        let link_details = {
          link_id: link["_private"]["data"]["id"]
        };
        this.axios({
          url: "http://127.0.0.1:5000/api/link/",
          headers: this.auth_header,
          method: "delete",
          data: link_details
        }).then(response => {
          if (response.data["message"].includes("Success")) {
            this.$cytoscape.instance.then(cy => {
              cy.remove(link);
            });
          } else {
            alert("Failed to delete node. " + response.data["message"]);
          }
        });
        this.update_view();
      });
    }
  },
  mounted: function() {
    document.querySelectorAll("canvas").forEach(canvas => {
      canvas.style.left = "0";
    });
    this.$nextTick(this.loadModules());
    this.update_view();
  }
};
</script>

<style>
@import "../assets/cyto.css";
</style>

