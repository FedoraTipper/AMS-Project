<template>
  <div>
    <div id="loading_action">
      <b-spinner
        v-if="spin"
        style="width: 3.5rem; height: 3.5rem;"
        variant="primary"
        label="Spinning"
      />
    </div>
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

    <b-modal size="xl" v-model="modal_label_relation_change" ok-only>
      <b-tabs card>
        <b-tab title="Add">
          <b-form @submit="modal_function">
            <div class="d-block text-center">
              <h4>{{modal_add_field}}</h4>
            </div>
            <b-form-group>
              <b-form-input v-model="selected.new_label_relationship"/>
            </b-form-group>
            <b-button type="submit" variant="primary">Add</b-button>
          </b-form>
        </b-tab>
        <b-tab title="Delete">
          <b-form @submit="modal_function_2">
            <div class="d-block text-center">
              <h4>{{modal_delete_field}}</h4>
            </div>
            <b-form-group>
              <b-form-select
                v-model="selected.label_relationship"
                :options="form.label_relationship"
                :value-field="form.field"
              />
            </b-form-group>
            <b-button type="submit" variant="danger">Delete</b-button>
          </b-form>
        </b-tab>
      </b-tabs>
    </b-modal>

    <b-modal size="xl" v-model="modal_type_show" ok-only>
      <div class="d-block text-center">
        <h4>Add a new type</h4>
      </div>
      <b-form @submit="add_type">
        <b-input-group prepend="New Type">
          <b-form-input v-model="selected.new_type"/>
        </b-input-group>
        <div id="draggablesspacing">
          <b-button type="submit" variant="primary">Add</b-button>
        </div>
      </b-form>
    </b-modal>

    <b-modal size="xl" v-model="modal_metadata_show" ok-only>
      <b-tabs card>
        <b-tab title="Display" active>
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
                <template slot="delete_button" slot-scope="row">
                  <b-button size="sm" @click="delete_metadata(row.item.meta_id)" variant="danger">x</b-button>
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
        </b-tab>
        <b-tab title="Add">
          <b-form @submit="add_metadata">
            <div class="d-block text-center">
              <h4>Add a metadata category</h4>
            </div>
            <div>
              <b-input-group prepend="Category">
                <b-form-input v-model="selected.category" required/>
              </b-input-group>
            </div>
            <div id="draggablesspacing">
              <b-input-group prepend="Data">
                <b-form-input v-model="selected.data" required/>
              </b-input-group>
            </div>
            <div id="draggablesspacing">
              <b-button type="submit" variant="primary">Add</b-button>
            </div>
          </b-form>
        </b-tab>
      </b-tabs>
    </b-modal>

    <b-modal size="xl" v-model="modal_search_show" ok-only>
      <div class="d-block text-center">
        <h3>Search for a node</h3>
      </div>
      <!-- User Interface controls -->
      <div id="container">
        <b-container fluid>
          <b-card-group class="text-center" id="log_table">
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
              :items="search_list"
              :fields="search_table_fields"
              :current-page="currentPage"
              :per-page="perPage"
              :filter="filter"
              :striped="true"
              :bordered="true"
              :hover="true"
              :outlines="true"
              :dark="true"
              selectable
              :select-mode="select_mode"
              selectedVariant="default"
              @row-selected="focusNode"
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
                  :total-rows="totalSearchRows"
                  :per-page="perPage"
                  v-model="currentPage"
                  class="my-0"
                />
              </b-col>
            </b-row>
          </b-card-group>
        </b-container>
      </div>
    </b-modal>
    <!-- Change collection -->
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
    <!-- Change layout button -->
    <b-dropdown
      id="overlay-button2"
      offset
      dropleft
      :text="current_layout"
      variant="primary"
      class="m-md-2"
      size="lg"
    >
      <div v-for="layout in layout_array" :key="layout">
        <b-dropdown-item @click="change_layout(layout)">{{layout}}</b-dropdown-item>
      </div>
    </b-dropdown>
    <div id="draggabledashboard">
      <div id="draggablelist">
        <vue-scroll>
          <div
            id="draggablesspacing"
            v-for="type in type_array"
            :key="type.type_id"
            v-bind="type_array"
          >
            <drag
              class="drag"
              @dragstart="start_drag"
              @dragend="end_drag"
              :transfer-data="{type}"
              :effect-allowed="['copy']"
              drop-effect="copy"
            >{{type.type}}</drag>
          </div>
        </vue-scroll>
      </div>
    </div>

    <drop
      class="drop"
      :class="{cytodrop}"
      @dragover="cytodrop = true"
      @dragleave="cytodrop = false"
      @drop="delete_type"
    >
      <div id="type_button">
        <b-button
          block
          size="lg"
          @click="modal_type_show=true"
          :variant="type_button_variant"
        >{{type_action}}</b-button>
      </div>
    </drop>
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
import dagre from "cytoscape-dagre";
import klay from "cytoscape-klay";
import { Drag, Drop } from "vue-drag-drop";
//Load cytoscapes theme config instance
let cytoscapeconfig = require("../style/cytoscapeconfig.js");
//Load external API functions
let APIUtil = (window.APIUtil = require("../js/api_functions.js"));
let FunctionUtil = (window.FunctionUtil = require("../js/utility_functions.js"));

export default {
  // Create components to allow for drag and drop
  components: {
    Drag,
    Drop
  },
  data() {
    return {
      spin: true,
      events: 0,
      cytodrop: false,
      type_action: "Add",
      type_button_variant: "secondary",
      layout_array: ["circle", "dagre", "klay", "cola"],
      current_layout: "circle",
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
      modal_search_show: false,
      modal_type_show: false,
      modal_label_relation_change: false,
      modal_node: false,
      form: {
        label_relationship: {},
        field: ""
      },
      selected: {
        label_relationship: "",
        type: "",
        icon: "",
        new_type: "",
        new_label_relationship: "",
        category: "",
        data: "",
        metadata_node: "",
        metadata_link: ""
      },
      modal_add_field: "",
      modal_delete_field: "",
      modal_function: "",
      modal_function_2: "",
      global_element: "",
      element_payload: {},
      metadata_list: [],
      search_list: [],
      currentPage: 1,
      perPage: 5,
      filter: null,
      totalMetaRows: 0,
      totalSearchRows: 0,
      select_mode: "single",
      metadata_table_fields: {
        meta_id: {
          label: "Metadata ID"
        },
        category: {
          label: "Metadata Category"
        },
        metadata: {
          label: "Field Data"
        },
        delete_button: {
          label: "Delete metadata"
        }
      },
      search_table_fields: {
        node_id: {
          label: "Node ID"
        },
        node_name: {
          label: "Node Name"
        },
        node_type: {
          label: "Node Type"
        },
        label_text: {
          label: "Label"
        }
      },
      config: {
        panningEnabled: true,
        fit: true,
        animate: true,
        boxSelectionEnabled: true,
        style: cytoscapeconfig.config
      }
    };
  },
  methods: {
    preConfig(cytoscape) {
      if (!window.eh) {
        edgehandle(cytoscape);
        cxtmenu(cytoscape);
        cytoscape.use(cola);
        cytoscape.use(dagre);
        cytoscape.use(klay);
      }
    },
    determine_loading() {
      if (this.events == 0) {
        this.spin = false;
      } else {
        this.spin = true;
      }
    },
    load_assets() {
      //Load all assets from database
      this.$cytoscape.instance.then(cy => {
        window.cy = cy;
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
          this.label_dict = response["dicts"][1];
          this.relationship_dict = response["dicts"][2];
          this.update_view();
        });
      });
    },
    loadModules() {
      this.events++;
      this.$cytoscape.instance.then(cy => {
        let eh = (window.eh = cy.edgehandles({
          // Increase delay or will spawn long lasting node object
          preview: true,
          snap: true,
          //Send to addLink function, to add the link to the database
          complete: (sourceNode, targetNode, addedEles) => {
            this.addLink(sourceNode, targetNode, addedEles);
          }
        }));
        eh.enableDrawMode();
        let menu = (window.menu = cy.cxtmenu({
          selector: "node",
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
            },
            {
              content: "Collapse",
              select: element => {
                this.collapse(element);
              }
            },
            {
              content: "Expand",
              select: element => {
                this.expand(element);
              }
            }
          ]
        }));
        let link_menu = (window.link_menu = cy.cxtmenu({
          selector: "edge",
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
              select: () => {
                this.search();
              }
            },
            {
              content: "Relationships",
              select: () => {
                this.setup_relationship_modal();
              }
            },
            {
              content: "Labels",
              select: () => {
                this.setup_label_modal();
              }
            }
          ]
        }));
      });
      this.events--;
    },
    addLink(sourceNode, targetNode, link) {
      let link_details = {
        node_id_1: sourceNode.data("id"),
        node_id_2: targetNode.data("id"),
        view_id: this.current_view.id
      };
      this.$cytoscape.instance.then(cy => {
        let condition_1 = "[source = '" + sourceNode.data("id") + "']";
        let condition_2 = "[target = '" + targetNode.data("id") + "']";
        let condition_3 = "[source = '" + targetNode.data("id") + "']";
        let condition_4 = "[target = '" + sourceNode.data("id") + "']";
        let edge_condition_1 = cy.edges(condition_1 + condition_2);
        let edge_condition_2 = cy.edges(condition_3 + condition_4);
        if (sourceNode == targetNode) {
          alert("Can't add link to same node");
          cy.remove(link);
        } else if (edge_condition_1.length + edge_condition_2.length != 1) {
          alert("Link already exists");
          cy.remove(link);
        } else {
          this.events++;
          window.APIUtil.add_link(link_details, link, this.auth_header, cy);
          this.events--;
        }
      });
    },
    start_drag() {
      this.type_action = "Drag here\nto delete";
      this.type_button_variant = "danger";
    },
    end_drag() {
      this.type_action = "Add";
      this.type_button_variant = "secondary";
    },
    handleDrop(node_type) {
      if (this.current_view.id != "") {
        let node_details = {
          view_id: this.current_view.id,
          type_id: node_type["type"]["type_id"]
        };
        this.events++;
        this.$cytoscape.instance.then(cy => {
          window.APIUtil.add_node(
            node_details,
            node_type["type"]["type"],
            this.current_view,
            this.auth_header,
            cy
          ).then(() => {
            this.events--;
            this.update_view();
          });
        });
        this.cytodrop = false;
      } else {
        alert("Pick a view");
      }
    },
    add_type() {
      let type_details = { type: this.selected.new_type };
      this.events++;
      window.APIUtil.add_type(
        type_details,
        this.type_array,
        this.auth_header
      ).then(response => {
        this.type_array = response["type_array"];
        this.modal_type_show = false;
        this.events--;
      });
    },
    delete_type(node_type) {
      let type = node_type["type"]["type"];
      let confirmation = confirm(
        "Are you sure you want to delete " + type + "?"
      );
      if (confirmation) {
        let type_details = node_type["type"];
        this.events++;
        window.APIUtil.delete_type(
          type_details,
          this.type_array,
          this.auth_header,
          window.cy
        ).then(response => {
          this.type_array = response["type_array"];
          this.update_view();
          this.events--;
        });
      }
    },
    change_collection(view) {
      if (this.current_view.id != view.view_id) {
        this.current_view.name = view.name;
        this.current_view.id = view.view_id;
        this.events++;
        this.$cytoscape.instance.then(cy => {
          window.APIUtil.load_view(
            view.view_id,
            this.type_dict,
            this.label_dict,
            this.relationship_dict,
            this.auth_header,
            cy
          ).then(() => {
            this.events--;
            this.update_view();
          });
        });
      }
    },
    update_view() {
      this.$cytoscape.instance.then(cy => {
        for (let i = 0; i < 5; i++) {
          cy.center();
          cy.layout({
            name: this.current_layout,
            fit: true,
            animate: true
          }).run();
        }
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
        console.log(this.relationship_dict);
        this.form.label_relationship = this.relationship_dict;
        this.form.field = this.relationship_dict.message;
        this.selected.label_relationship = element.data("payload")[
          "relationship_id"
        ];
        this.element_payload = element.data("payload");
        this.element_payload["element_id"] = element.data("id");
        this.modal_node = false;
        this.modal_function = this.change_link;
        this.modal_element_change = true;
      } else {
        this.form.label_relationship = this.label_dict;
        this.form.field = this.label_dict.label_text;
        //Load node already set fields
        this.selected.label_relationship = element.data("payload")["label_id"];
        this.selected.type = element.data("payload")["type_id"];
        this.selected.icon = element.data("payload")["icon"];
        this.element_payload = element.data("payload");
        this.element_payload["element_id"] = element.data("id");
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
        this.events++;
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
            this.events--;
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
        this.events++;
        this.$cytoscape.instance.then(cy => {
          window.APIUtil.change_link(
            link_details,
            this.relationship_dict[this.selected.label_relationship],
            this.auth_header,
            cy
          );
        });
        this.events--;
        this.modal_element_change = false;
      } else {
        alert("Nothing to change");
        this.modal_element_change = false;
      }
    },
    getMetadata(element) {
      let uri = "?";
      this.selected.metadata_link = null;
      this.selected.metadata_node = null;
      if (element["_private"]["group"] == "edges") {
        uri += "link_id=" + element.data("payload")["link_id"];
        this.selected.metadata_link = element.data("payload")["link_id"];
      } else {
        uri += "node_id=" + element.data("id");
        this.selected.metadata_node = element.data("id");
      }
      this.metadata_list = [];
      this.events++;
      window.APIUtil.get_metadata(
        uri,
        this.metadata_list,
        this.auth_header
      ).then(response => {
        this.totalMetaRows = this.metadata_list.length;
        this.modal_metadata_show = true;
        this.events--;
      });
    },
    add_metadata() {
      let metadata_details = {
        category: this.selected.category,
        data: this.selected.data
      };
      if (this.selected.metadata_node) {
        metadata_details["node_id"] = this.selected.metadata_node;
      } else {
        metadata_details["link_id"] = this.selected.metadata_link;
      }
      this.events++;
      window.APIUtil.add_metadata(
        metadata_details,
        this.metadata_list,
        this.auth_header
      ).then(response => {
        this.events--;
      });
    },
    delete_metadata(metadata_id) {
      let confirmation = confirm(
        "Are you sure you want to delete metadata " + metadata_id
      );
      if (confirmation) {
        let metadata_details = {
          meta_id: metadata_id
        };
        this.events++;
        window.APIUtil.delete_metadata(
          metadata_details,
          this.metadata_list,
          this.auth_header
        ).then(response => {
          this.metadata_list = response["metadata_list"];
          this.events--;
        });
      }
    },
    deleteNode(node) {
      let node_details = {
        node_id: node["_private"]["data"]["id"]
      };
      this.events++;
      this.$cytoscape.instance.then(cy => {
        window.APIUtil.delete_node(node_details, node, this.auth_header, cy);
      });
      this.update_view();
      this.events--;
    },
    deleteLink(link) {
      this.events++;
      let link_details = {
        link_id: link["_private"]["data"]["payload"]["link_id"]
      };
      this.$cytoscape.instance.then(cy => {
        window.APIUtil.delete_link(link_details, link, this.auth_header, cy);
      });
      this.update_view();
      this.events--;
    },
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
    search() {
      this.search_list = window.FunctionUtil.build_search_list(window.cy);
      this.totalSearchRows = this.search_list.length;
      this.modal_search_show = true;
    },
    focusNode(node) {
      this.modal_search_show = false;
      //Deselect any selected nodes
      if (node[0]) {
        this.$cytoscape.instance.then(cy => {
          node = cy.$id(String(node[0]["node_id"]));
          cy.nodes().unselect();
          node.data()["display"] = "element";
          node.select();
        });
      }
    },
    change_layout(layout) {
      this.current_layout = layout;
      this.update_view();
    },
    collapse(node) {
      window.FunctionUtil.collapse_node(node, window.cy);
    },
    expand(node) {
      window.FunctionUtil.expand_node(node, window.cy);
    },
    setup_relationship_modal() {
      this.selected.new_label_relationship = "";
      this.selected.label_relationship = null;
      this.modal_add_field = "Add a new relationship";
      this.modal_delete_field = "Delete a relationship";
      this.modal_function = this.add_relationship;
      this.modal_function_2 = this.delete_relationship;
      this.form.label_relationship = null;
      this.form.label_relationship = this.relationship_dict;
      this.form.field = this.relationship_dict.message;
      this.modal_label_relation_change = true;
    },
    setup_label_modal() {
      this.selected.new_label_relationship = "";
      this.selected.label_relationship = null;
      this.modal_add_field = "Add a new label";
      this.modal_delete_field = "Delete a label";
      this.modal_function = this.add_label;
      this.modal_function_2 = this.delete_label;
      this.form.label_relationship = null;
      this.form.label_relationship = this.label_dict;
      this.form.field = this.label_dict.label_text;
      this.modal_label_relation_change = true;
    },
    add_relationship() {
      if (
        window.FunctionUtil.relationship_exists(
          this.selected.new_label_relationship,
          this.relationship_dict
        ) == false
      ) {
        let relationship_details = {
          message: this.selected.new_label_relationship
        };
        this.events++;
        window.APIUtil.add_relationship(
          relationship_details,
          this.relationship_dict,
          this.relationship_array,
          this.auth_header
        ).then(response => {
          this.modal_label_relation_change = false;
          this.relationship_dict = response["relationship_dict"];
          this.relationship_array = response["relationship_array"];
          this.events--;
        });
      } else {
        alert("Relationship already exists");
      }
    },
    delete_relationship() {
      let relationship_details = {
        relationship_id: this.selected.label_relationship,
        message: this.relationship_dict[this.selected.label_relationship]
      };
      this.events++;
      window.APIUtil.delete_relationship(
        relationship_details,
        this.relationship_array,
        this.relationship_dict,
        this.auth_header,
        window.cy
      ).then(response => {
        this.modal_label_relation_change = false;
        this.relationship_dict = response["relationship_dict"];
        console.log(this.relationship_dict);
        this.relationship_array = response["relationship_array"];
        this.events--;
      });
    },
    add_label() {
      if (
        window.FunctionUtil.label_exists(
          this.selected.new_label_relationship,
          this.label_dict
        ) == false
      ) {
        let label_details = {
          label_text: this.selected.new_label_relationship
        };
        this.events++;
        window.APIUtil.add_label(
          label_details,
          this.label_array,
          this.label_dict,
          this.auth_header
        ).then(response => {
          this.modal_label_relation_change = false;
          this.label_dict = response["label_dict"];
          this.label_array = response["label_array"];
          this.events--;
        });
      } else {
        alert("The label already exists");
      }
    },
    delete_label() {
      let label_details = {
        label_id: this.selected.label_relationship,
        label_text: this.label_dict[this.selected.label_relationship]
      };
      this.events++;
      window.APIUtil.delete_label(
        label_details,
        this.label_array,
        this.label_dict,
        this.auth_header,
        window.cy
      ).then(response => {
        this.modal_label_relation_change = false;
        this.label_dict = response["label_dict"];
        this.label_array = response["label_array"];
        this.events--;
      });
    }
  },
  mounted: function() {
    document.querySelectorAll("canvas").forEach(canvas => {
      canvas.style.left = "0";
    });
    setInterval(() => {
      this.determine_loading();
    }, 250);
    this.$nextTick(this.loadModules());
    this.$nextTick(this.load_assets());
    this.update_view();
  }
};
</script>

<style>
@import "../style/cyto.css";
</style>

