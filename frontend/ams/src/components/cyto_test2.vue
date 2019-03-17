<template>
  <div>
    <b-modal size="xl" v-model="modal_metadata_show" ok-only>
      <div id="metadata_table">
        <b-card-group class="text-center">
          <b-row>
            <b-col md="10" class="my-1">
              <b-form-group label-cols-sm="3" label="Filter" class="mb-0">
                <b-input-group>
                  <b-form-input v-model="filter" placeholder="Type to Search"/>
                  <b-input-group-append>
                    <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                  </b-input-group-append>
                </b-input-group>
              </b-form-group>
            </b-col>
          </b-row>

          <!-- Main table element -->
          <b-table
            show-empty
            stacked="md"
            :items="metadata_list"
            :fields="metadata_table_fields"
            :current-page="currentPage"
            :per-page="perPage"
            :filter="filter"
            :striped="true"
            :bordered="true"
            :hover="true"
            :outlines="true"
            :dark="true"
            @filtered="onFiltered"
          >
            <template slot="name" slot-scope="row">{{ row.value.first }} {{ row.value.last }}</template>

            <template slot="row-details" slot-scope="row">
              <b-card>
                <ul>
                  <li v-for="(value, key) in row.item" :key="key">{{ key }}: {{ value }}</li>
                </ul>
              </b-card>
            </template>
          </b-table>

          <b-row>
            <b-col md="6" class="my-1">
              <b-pagination
                :total-rows="totalMetaRows"
                :per-page="perPage"
                v-model="currentPage"
                class="my-0"
              />
            </b-col>
          </b-row>
        </b-card-group>
      </div>
    </b-modal>

    <b-dropdown
      id="overlay-button"
      offset
      dropleft
      :text="current_view.name"
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
import cola from "cytoscape-cola";
import cxtmenu from "cytoscape-cxtmenu";
import { Drag, Drop } from "vue-drag-drop";
//Load cytoscapes theme config instance
let cytoscapeconfig = require("../style/cytoscapeconfig.js");
//Load external API functions
let APIUtil = (window.APIUtil = require("../js/api_functions.js"));

export default {
  // Create components to allow for drag and drop
  components: {
    Drag,
    Drop
  },
  data() {
    return {
      cytodrop: false,
      type_array: [],
      view_array: [],
      label_array: [],
      relationship_array: [],
      type_count: {},
      auth_header: {
        Authorization: localStorage.getItem("Authorization")
      },
      current_view: {
        name: "",
        id: ""
      },
      modal_metadata_show: false,
      metadata_list: [],
      currentPage: 1,
      perPage: 5,
      filter: null,
      totalMetaRows: 0,
      metadata_table_fields: {
        meta_id: {
          label: "Metadata ID"
        },
        category: {
          label: "Metadata Category"
        },
        metadata: {
          label: "Field Data"
        }
      },
      config: {
        panningEnabled: true,
        fit: false,
        animate: false,
        boxSelectionEnabled: false,
        style: cytoscapeconfig.config
      }
    };
  },
  methods: {
    preConfig(cytoscape) {
      edgehandle(cytoscape);
      cxtmenu(cytoscape);
      cytoscape.use(cola);
    },
    load_assets() {
      //Load all assets from database
      this.$cytoscape.instance.then(cy => {
        window.APIUtil.load_assets(
          this.type_array,
          this.type_count,
          this.view_array,
          this.current_view,
          this.label_array,
          this.relationship_array,
          this.auth_header,
          cy
        ).then(() => {
          this.update_view();
        });
      });
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
        view_id: this.current_view.id
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
    handleDrop(node_type) {
      if (this.current_view.id != "") {
        let node_details = {
          view_id: this.current_view.id,
          type_id: node_type["type"]["type_id"]
        };
        this.$cytoscape.instance.then(cy => {
          window.APIUtil.add_node(
            node_details,
            node_type["type"]["type"],
            this.current_view,
            this.auth_header,
            cy
          ).then(() => {
            this.update_view();
          });
        });
        this.cytodrop = false;
      } else {
        alert("Pick a view");
      }
    },
    change_collection(view) {
      this.current_view.name = view.name;
      this.current_view.id = view.view_id;
    },
    update_view() {
      this.$cytoscape.instance.then(cy => {
        for (let i = 0; i < 5; i++) {
          cy.center();
          cy.layout({ name: "circle", fit: true }).run();
        }
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
      let uri = "?";
      if (element["_private"]["group"] == "edges") {
        uri += "link_id=" + element["_private"]["data"]["payload"]["link_id"];
      } else {
        uri += "node_id=" + element["_private"]["data"]["id"];
      }
      this.metadata_list = [];
      window.APIUtil.get_metadata(
        uri,
        this.metadata_list,
        this.auth_header
      ).then(response => {
        this.totalMetaRows = this.metadata_list.length;
        if (this.totalMetaRows != 0) {
          this.modal_metadata_show = true;
        } else {
          alert("No metadata found for the asset");
        }
      });
    },
    deleteNode(node) {
      let node_details = {
        node_id: node["_private"]["data"]["id"]
      };
      this.$cytoscape.instance.then(cy => {
        window.APIUtil.delete_node(node_details, node, this.auth_header, cy);
      });
      this.update_view();
    },
    deleteLink(link) {
      let link_details = {
        link_id: link["_private"]["data"]["id"]
      };
      this.$cytoscape.instance.then(cy => {
        window.APIUtil.delete_link(link_details, link, this.auth_header, cy);
      });
      this.update_view();
    },
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    }
  },
  mounted: function() {
    document.querySelectorAll("canvas").forEach(canvas => {
      canvas.style.left = "0";
    });
    this.$nextTick(this.loadModules());
    this.$nextTick(this.load_assets());
    this.update_view();
  }
};
</script>

<style>
@import "../style/cyto.css";
</style>

