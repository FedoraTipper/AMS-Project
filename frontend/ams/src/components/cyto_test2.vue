<template>
  <div>
    <b-dropdown
      id="overlay-button"
      right
      offset="49"
      dropdown
      :text="current_view"
      variant="primary"
      class="m-2"
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
      current_view: "",
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
            }
          ]
        }));
      });
    },
    addLink(sourceNode, targetNode, Link) {},
    handleDrop(nodetype) {
      this.$cytoscape.instance.then(cy => {
        cy.add({
          group: "nodes",
          data: {
            id: this.i,
            name: nodetype["type"]["type"],
            payload: {
              type_id: nodetype["type"]["type_id"],
              type: nodetype["type"]["type"],
              node_id: "",
              //  Comeback to this and set the view
              view_id: ""
            },
            imglink: null
          }
        });
        this.cytodrop = false;
        this.i++;
      });

      this.update_view();
    },
    change_collection(view) {
      this.current_view = view.name;
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
    deleteNode(node) {
      this.$cytoscape.instance.then(cy => {
        cy.remove(node);
      });
    },
    deleteLink(link) {
      this.$cytoscape.instance.then(cy => {
        cy.remove(link);
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

