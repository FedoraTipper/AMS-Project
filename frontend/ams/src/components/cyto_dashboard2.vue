<template>
  <div>
    <b-modal size="xl" v-model="modal_element_change" ok-only>
      <b-form @submit="modal_function">
        <b-form-group v-if="modal_node" label="Type:">
          <b-form-select
            v-model="selected.type"
            :options="type_dict"
            :value-field="type_array.type"
          />
        </b-form-group>
        <b-form-group label="Label:">
          <b-form-select
            v-model="selected.label_relationship"
            :options="form.label_relationship"
            :value-field="form.field"
          />
        </b-form-group>
        <b-input-group prepend="Icon" v-if="modal_node" class="mt-3">
          <b-form-input v-model="selected.icon"/>
        </b-input-group>
        <b-button type="submit" variant="primary">Change</b-button>
      </b-form>
    </b-modal>

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
      type_dict: {},
      view_array: [],
      view_dict: {},
      label_array: [],
      label_dict: {},
      relationship_array: [],
      relationship_dict: {},
      auth_header: {
        Authorization: localStorage.getItem("Authorization")
      },
      current_view: {
        name: "",
        id: ""
      },
      modal_metadata_show: false,
      modal_element_change: false,
      modal_node: false,
      form: {
        label_relationship: {},
        field: ""
      },
      selected: {
        label_relationship: "",
        type: "",
        icon: ""
      },
      modal_function: "",
      global_element: "",
      element_payload: {},
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
          this.view_array,
          this.current_view,
          this.label_array,
          this.relationship_array,
          this.auth_header,
          cy
        ).then(response => {
          this.type_dict = response["dicts"][0];
          //this.type_array = response["arrays"][0];
          this.label_dict = response["dicts"][1];
          //this.label_array = response["arrays"][1];
          this.relationship_dict = response["dicts"][2];
          // this.relationship_array = response["arrays"][2];
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
              content: "Change Details",
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
        let core_menu = (window.core_menu = cy.cxtmenu({
          selector: "core",
          commands: [
            {
              content: "Search",
              select: this.search()
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
        let condition_1 =
          "[source = '" + sourceNode["_private"]["data"]["id"] + "']";
        let condition_2 =
          "[target = '" + targetNode["_private"]["data"]["id"] + "']";
        let condition_3 =
          "[source = '" + targetNode["_private"]["data"]["id"] + "']";
        let condition_4 =
          "[target = '" + sourceNode["_private"]["data"]["id"] + "']";
        let edge_condition_1 = cy.edges(condition_1 + condition_2);
        let edge_condition_2 = cy.edges(condition_3 + condition_4);
        if (sourceNode == targetNode) {
          alert("Can't add link to same node");
          cy.remove(link);
        } else if (edge_condition_1.length + edge_condition_2.length != 1) {
          alert("Link already exists");
          cy.remove(link);
        } else {
          window.APIUtil.add_link(link_details, link, this.auth_header, cy);
        }
      });
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
      if (this.current_view.id != view.view_id) {
        this.current_view.name = view.name;
        this.current_view.id = view.view_id;
        this.$cytoscape.instance.then(cy => {
          window.APIUtil.load_view(
            view.view_id,
            this.type_dict,
            this.label_dict,
            this.relationship_dict,
            this.auth_header,
            cy
          ).then(() => {
            this.update_view();
          });
        });
      }
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
        this.form.label_relationship = this.relationship_dict;
        this.form.field = this.relationship_dict.message;
        this.selected.label_relationship =
          element["_private"]["data"]["payload"]["relationship_id"];
        this.element_payload = element["_private"]["data"]["payload"];
        this.element_payload["element_id"] = element["_private"]["data"]["id"];
        this.modal_node = false;
        this.modal_function = this.change_link;
        this.modal_element_change = true;
      } else {
        this.form.label_relationship = this.label_dict;
        this.form.field = this.label_dict.label_text;
        //Load node already set fields
        this.selected.label_relationship =
          element["_private"]["data"]["payload"]["label_id"];
        this.selected.type = element["_private"]["data"]["payload"]["type_id"];
        this.selected.icon = element["_private"]["data"]["payload"]["icon"];
        this.element_payload = element["_private"]["data"]["payload"];
        this.element_payload["element_id"] = element["_private"]["data"]["id"];
        this.modal_node = true;
        this.modal_function = this.change_node;
        this.modal_element_change = true;
      }
    },
    change_node() {
      let node_details = {
        node_id: this.element_payload["element_id"]
      };
      let change = false;
      if (
        this.selected.label_relationship &&
        this.selected.label_relationship != this.element_payload["label_id"]
      ) {
        node_details["label_id"] = this.selected.label_relationship;
        change = true;
      }
      if (this.selected.type != this.element_payload["type_id"]) {
        node_details["type_id"] = this.selected.type;
        change = true;
      }
      if (
        this.selected.icon &&
        this.selected.icon != this.element_payload["icon"]
      ) {
        node_details["icon"] = this.selected.icon;
        change = true;
      }
      if (change) {
        this.$cytoscape.instance.then(cy => {
          window.APIUtil.change_node(
            node_details,
            this.label_dict[this.selected.label_relationship],
            this.type_dict[this.selected.type],
            this.auth_header,
            cy
          ).then(() => {
            this.update_view();
            this.modal_element_change = false;
          });
        });
      } else {
        alert("Nothing to change");
        this.modal_element_change = false;
      }
    },
    change_link() {
      let link_details = {
        link_id: this.element_payload["link_id"]
      };
      if (
        this.selected.label_relationship &&
        this.selected.label_relationship !=
          this.element_payload["relationship_id"]
      ) {
        link_details["relationship_id"] = this.selected.label_relationship;
        this.$cytoscape.instance.then(cy => {
          window.APIUtil.change_link(
            link_details,
            this.relationship_dict[this.selected.label_relationship],
            this.auth_header,
            cy
          );
        });
        this.modal_element_change = false;
      } else {
        alert("Nothing to change");
        this.modal_element_change = false;
      }
    },
    getMetadata(element) {
      let uri = "?";
      if (element["_private"]["group"] == "edges") {
        uri += "link_id=" + element["_private"]["data"]["payload"]["link_id"];
        console.log(uri);
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
        link_id: link["_private"]["data"]["payload"]["link_id"]
      };
      this.$cytoscape.instance.then(cy => {
        window.APIUtil.delete_link(link_details, link, this.auth_header, cy);
      });
      this.update_view();
    },
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
    search() {}
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

