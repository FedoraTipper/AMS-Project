<template>
  <div>
    <b-dropdown
      id="overlay-button"
      right
      offset="49"
      dropup
      text="+"
      variant="primary"
      class="m-2"
      size="lg"
    >
      <b-dropdown-item @click="modal_node_show=true">Node</b-dropdown-item>
      <b-dropdown-item @click="modal_link_show=true">Link</b-dropdown-item>
      <b-dropdown-item @click="modal_metadata_show=true">Metadata</b-dropdown-item>
    </b-dropdown>
    <b-button @click="modal_search_show=true" variant="primary" id="overlay-button-2" size="lg">🔍</b-button>
    <b-modal size="xl" v-model="modal_search_show" title="Search" ok-only>
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
              <b-col md="10" class="my-1">
                <b-form-group label-cols-sm="3" label="Per page" class="mb-0">
                  <b-form-select :options="pageOptions" v-model="perPage"/>
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
                  :total-rows="totalRows"
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
    <b-modal size="xl" v-model="modal_node_show">
      <b-tabs card>
        <b-tab title="Add" active>
          <b-form @submit="addNode">
            <b-input-group prepend="Type" required class="mt-3">
              <b-form-input v-model="form.node_type" required/>
            </b-input-group>
            <b-input-group prepend="Icon" class="mt-3">
              <b-form-input v-model="form.icon"/>
            </b-input-group>
            <b-form-group id="Label_id_group" label="Collection label:" label-for="label_dropdown">
              <b-form-select
                id="label_dropdown"
                :options="options.label"
                v-model="selected.node_label"
              />
            </b-form-group>
            <b-button type="submit" variant="primary">Add Node</b-button>
          </b-form>
        </b-tab>
        <b-tab title="Change">
          <b-form @submit="changeNode">
            <b-form-group
              id="Node_Type_group"
              label="Select node:"
              required
              label-for="node_dropdown"
            >
              <b-form-select
                id="old_node_dropdown"
                :options="nodes_form"
                required
                v-model="form.node_type"
              />
            </b-form-group>
            <b-input-group prepend="New Type" class="mt-3">
              <b-form-input v-model="form.new_node_type"/>
            </b-input-group>
            <b-input-group prepend="Icon" class="mt-3">
              <b-form-input v-model="form.icon"/>
            </b-input-group>
            <b-form-group id="Label_id_group" label="Collection label:" label-for="label_dropdown">
              <b-form-select
                id="label_dropdown"
                :options="options.label"
                v-model="selected.node_label"
              />
            </b-form-group>
            <b-button type="submit" variant="primary">Change Node</b-button>
          </b-form>
        </b-tab>
        <b-tab title="Delete">
          <b-form @submit="deleteNode">
            <b-form-group label="Select node to delete:" required>
              <b-form-select
                id="delete_node"
                :options="nodes_form"
                required
                v-model="form.node_type"
              />
            </b-form-group>
            <b-button type="submit" variant="danger">Delete Node</b-button>
          </b-form>
        </b-tab>
      </b-tabs>
    </b-modal>
    <b-modal size="xl" v-model="modal_link_show">
      <b-tabs card>
        <b-tab title="Add" active>
          <b-form @submit="addLink">
            <b-form-group label="Source:">
              <b-form-select
                id="label_dropdown"
                required
                :options="nodes_form"
                v-model="form.node_type_1"
              />
            </b-form-group>
            <b-form-group id="Label_id_group" label="Target:" label-for="node_id_2">
              <b-form-select
                id="label_dropdown"
                required
                :options="nodes_form"
                v-model="form.node_type_2"
              />
            </b-form-group>
            <b-form-group id="Label_id_group" label="Collection label:" label-for="label_dropdown">
              <b-form-select
                id="label_dropdown"
                :options="options.label"
                v-model="form.link_label"
              />
            </b-form-group>
            <b-form-group label="Relationship:" label-for="label_dropdown">
              <b-form-select :options="relationship_form" v-model="form.relationship"/>
            </b-form-group>
            <b-button type="submit" variant="primary">Add Link</b-button>
          </b-form>
        </b-tab>
        <b-tab title="Change">
          <b-form @submit="changeLink">
            <b-form-group label="Select link to change:" required label-for="label_dropdown">
              <b-form-select required :options="links_form" v-model="selected.link"/>
            </b-form-group>
            <b-form-group label="Source:">
              <b-form-select id="label_dropdown" :options="nodes_form" v-model="form.node_type_1"/>
            </b-form-group>
            <b-form-group id="Label_id_group" label="Target:" label-for="node_id_2">
              <b-form-select id="label_dropdown" :options="nodes_form" v-model="form.node_type_2"/>
            </b-form-group>
            <b-form-group id="Label_id_group" label="Collection label:" label-for="label_dropdown">
              <b-form-select
                id="label_dropdown"
                :options="options.label"
                v-model="form.link_label"
              />
            </b-form-group>
            <b-form-group label="Relationship:" label-for="label_dropdown">
              <b-form-select :options="relationship_form" v-model="form.relationship"/>
            </b-form-group>
            <b-button type="submit" variant="primary">Change Link</b-button>
          </b-form>
        </b-tab>
        <b-tab title="Delete">
          <b-form @submit="deleteLink">
            <b-form-group label="Select link to delete:" required>
              <b-form-select :options="links_form" required v-model="form.links_name"/>
            </b-form-group>
            <b-button type="submit" variant="danger">Delete Link</b-button>
          </b-form>
        </b-tab>
      </b-tabs>
    </b-modal>
    <b-modal size="xl" v-model="modal_metadata_show">
      <b-tabs card>
        <b-tab title="Get" active>
          <b-form @submit="getMetadata">
            <b-form-group label="Node:" label-for="node_id_2">
              <b-form-select required :options="nodes_form" v-model="selected.node"/>
              <div id="button_padding">
                <b-button type="submit" variant="primary">Get metadata</b-button>
              </div>
            </b-form-group>
            <div id="metadata_table">
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
          </b-form>
        </b-tab>
        <b-tab title="Add">
          <b-form @submit="addMetadata">
            <b-form-group label="Select Node:" label-for="node_id_2">
              <b-form-select required :options="nodes_form" v-model="selected.node"/>
            </b-form-group>
            <b-input-group prepend="Category" required class="mt-3">
              <b-form-input v-model="form.metadata.category"/>
            </b-input-group>
            <b-input-group prepend="Metadata" required class="mt-3">
              <b-form-input v-model="form.metadata.data"/>
            </b-input-group>
            <div id="button_padding">
              <b-button type="submit" variant="primary">Add Metadata</b-button>
            </div>
          </b-form>
        </b-tab>
        <b-tab title="Change">
          <b-form @submit="changeMetadata">
            <b-form-group label="Select Metadata ID:">
              <b-form-select required :options="metadata_form" v-model="selected.metadata"/>
            </b-form-group>
            <b-form-group label="Select Node:" label-for="node_id_2">
              <b-form-select :options="nodes_form" v-model="selected.node"/>
            </b-form-group>
            <b-input-group prepend="Category" required class="mt-3">
              <b-form-input v-model="form.metadata.category"/>
            </b-input-group>
            <b-input-group prepend="Metadata" required class="mt-3">
              <b-form-input v-model="form.metadata.data"/>
            </b-input-group>
            <b-button type="submit" variant="primary">Change Metadata</b-button>
          </b-form>
        </b-tab>
        <b-tab title="Delete">
          <b-form @submit="deleteMetadata">
            <b-form-group label="Select Metadata ID:">
              <b-form-select required :options="metadata_form" v-model="selected.metadata"/>
            </b-form-group>
            <b-button type="submit" variant="danger">Delete Metadata</b-button>
          </b-form>
        </b-tab>
      </b-tabs>
    </b-modal>
    <div id="holder">
      <cytoscape :config="config" :preConfig="preConfig"></cytoscape>
    </div>
    <div id="nodeData">
      <b-card title="Node data" tag="article" style="max-width: 20rem;" class="mb-2">
        <b-card-text>
          <b-input-group prepend="Node Type" class="mb-2 mr-sm-2 mb-sm-0">
            <b-input v-model="form.NDataType" disabled placeholder="Click a node"/>
          </b-input-group>
          <b-input-group prepend="Collection Label" class="mb-2 mr-sm-2 mb-sm-0">
            <b-input v-model="form.NDataCollection" disabled placeholder="None"/>
          </b-input-group>
        </b-card-text>
      </b-card>
    </div>
  </div>
</template>


<script>
import jquery from "jquery";
import cola from "cytoscape-cola";
import expandCollapse from "cytoscape-expand-collapse";
import cosebilkent from "cytoscape-cose-bilkent";

export default {
  data() {
    return {
      modal_node_show: false,
      modal_link_show: false,
      modal_metadata_show: false,
      modal_search_show: false,
      totalRows: "1",
      totalMetaRows: "1",
      currentPage: 1,
      filter: null,
      pageOptions: [5, 10, 15],
      perPage: 5,
      select_mode: "single",
      search_table_fields: {
        node_id: {
          label: "Node ID"
        },
        node_type: {
          label: "Node Type"
        },
        label_id: {
          label: "Label ID"
        }
      },
      selected: {
        node_label: "",
        link: "",
        metadata: ""
      },
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
      form: {
        metadata: {
          category: "",
          data: ""
        },
        node_type: "",
        node_type_1: "",
        node_type_2: "",
        node_label: "",
        link_label: "",
        new_node_type: "",
        links_name: "",
        relationship: "",
        NDataType: "",
        NDataCollection: "",
        icon: ""
      },
      auth_header: {
        Authorization: localStorage.getItem("Authorization")
      },
      options: {
        label: [],
        node: []
      },
      selected: {
        node: null
      },
      nodes_form: [],
      links_form: [],
      relationship_form: [],
      metadata_list: [],
      search_list: [],
      labels_dict: {},
      nodes_dict: {},
      links_dict: {},
      relationship_dict: {},
      metadata_form: [],
      config: {
        panningEnabled: true,
        fit: false,
        animate: false,
        boxSelectionEnabled: false,
        style: [
          {
            selector: "node",
            style: {
              shape: "hexagon",
              "background-color": "#0d47a1",
              label: "data(name)",
              "background-image": "data(imglink)",
              "background-fit": "cover",
              height: 24,
              width: 24
            }
          },
          {
            selector: "edge",
            style: {
              "line-color": "#42a5f5",
              label: "data(name)",
              "curve-style": "straight",
              "target-arrow-color": "#0d47a1",
              "target-arrow-shape": "triangle"
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
      }
    };
  },
  methods: {
    cyUpdate() {
      this.$cytoscape.instance.then(cy => {
        window.cy = cy;
        cy.elements().remove();
        this.resetVariables();
        let nodes = [];
        let links = [];
        let relationships = {};

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
            this.options.label.push({
              value: {
                label_id: labels[i]["label_id"],
                label_text: labels[i]["label_text"]
              },
              text: labels[i]["label_text"]
            });
            this.labels_dict[labels[i]["label_text"]] = labels[i]["label_id"];
            labels_dict_2[labels[i]["label_id"]] = labels[i]["label_text"];

            cy.add({
              group: "nodes",
              data: {
                id: "label_" + labels[i]["label_id"],
                name: labels[i]["label_text"],
                parent: "label_" + labels[i]["parent"],
                label_collection: labels[i]["label_text"],
                imglink: "null"
              }
            });
          }

          this.totalRows = nodes.length;
          for (var i = 0; i < nodes.length; i++) {
            this.nodes_form.push(nodes[i]["type"]);
            if (labels_dict_2[nodes[i]["label_id"]]) {
              this.nodes_dict[nodes[i]["type"]] = {
                node_id: nodes[i]["node_id"],
                node_type: nodes[i]["type"],
                label_id: labels_dict_2[nodes[i]["label_id"]]
              };
              this.search_list.push({
                node_id: nodes[i]["node_id"],
                node_type: nodes[i]["type"],
                label_id: labels_dict_2[nodes[i]["label_id"]]
              });
            } else {
              this.nodes_dict[nodes[i]["type"]] = {
                node_id: nodes[i]["node_id"],
                node_type: nodes[i]["type"]
              };
              this.search_list.push({
                node_id: nodes[i]["node_id"],
                node_type: nodes[i]["type"],
                label_id: "Null"
              });
            }
            let icon_link = "";
            if (nodes[i]["icon"]) {
              icon_link =
                "https://cors-anywhere.herokuapp.com/" + nodes[i]["icon"];
            } else {
              icon_link = "null";
            }

            cy.add({
              group: "nodes",
              data: {
                id: nodes[i]["node_id"],
                name: nodes[i]["type"],
                parent: "label_" + nodes[i]["label_id"],
                label_collection: labels_dict_2[nodes[i]["label_id"]],
                imglink: icon_link
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

            cy.add({
              group: "edges",
              data: {
                id: "l" + links[i]["link_id"],
                source: links[i]["node_id_1"],
                target: links[i]["node_id_2"],
                name: link_name
              }
            });
          }

          this.init_metadata_list();

          cy.layout({
            name: "cose-bilkent",
            nodeRepulsion: 30000,
            fit: true,
            padding: 150,
            nestingFactor: 0.2,
            gravity: 0.1
          }).run();
        });
        //Bind clicking a node, to load collection value
        cy.on("click", "node", evt => {
          this.form.NDataType = evt.target.data()["name"];
          this.form.NDataCollection = evt.target.data()["label_collection"];
        });
      });
    },
    preConfig(cytoscape) {
      try {
        expandCollapse(cytoscape, jquery);
      } catch {}
      cytoscape.use(cosebilkent);
    },
    addNode() {
      let node_details = {
        type: this.form.node_type
      };
      if (this.selected.node_label) {
        node_details["label_id"] = this.selected.node_label["label_id"];
      }
      if (this.form.icon) {
        node_details["icon"] = this.form.icon;
      }
      this.axios({
        url: "http://127.0.0.1:5000/api/node/",
        headers: this.auth_header,
        method: "post",
        data: node_details
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          alert("Added a new node");
          this.cyUpdate();
        } else {
          console.log(response.data["message"]);
          alert("Failed to create new node");
        }
      });
    },
    changeNode() {
      let node_details = {
        node_id: this.nodes_dict[this.form.node_type]["node_id"]
      };
      if (this.selected.node_label) {
        node_details["label_id"] = this.selected.node_label["label_id"];
      }
      if (this.form.new_node_type) {
        node_details["type"] = this.form.new_node_type;
      }
      if (this.form.icon) {
        node_details["icon"] = this.form.icon;
      }

      this.axios({
        url: "http://127.0.0.1:5000/api/node/",
        headers: this.auth_header,
        method: "put",
        data: node_details
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          alert("Changed Node");
          this.cyUpdate();
        } else {
          console.log(response.data["message"]);
          alert("Failed to change node");
        }
      });
    },
    deleteNode() {
      let node_details = {
        node_id: this.nodes_dict[this.form.node_type]["node_id"]
      };
      this.axios({
        url: "http://127.0.0.1:5000/api/node/",
        headers: this.auth_header,
        method: "delete",
        data: node_details
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          alert("Deleted Node");
          this.cyUpdate();
        } else {
          alert("Failed to delete node");
        }
      });
    },
    addLink() {
      let link_details = {
        node_id_1: this.nodes_dict[this.form.node_type_1]["node_id"],
        node_id_2: this.nodes_dict[this.form.node_type_2]["node_id"]
      };
      if (this.form.link_label) {
        link_details["label_id"] = this.labels_dict[this.form.link_label];
      }
      if (this.form.relationship) {
        link_details["relationship_id"] = this.relationship_dict[
          this.form.relationship
        ];
      }
      this.axios({
        url: "http://127.0.0.1:5000/api/link/",
        headers: this.auth_header,
        method: "post",
        data: link_details
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          alert("Created link");
          this.cyUpdate();
        } else {
          alert("Failed to create new link");
        }
      });
    },
    changeLink() {
      let link_details = {
        link_id: this.links_dict[this.selected.link]
      };
      if (this.form.node_type_1) {
        link_details["node_id_1"] = this.nodes_dict[this.form.node_type_1][
          "node_id"
        ];
      }
      if (this.form.node_type_2) {
        link_details["node_id_2"] = this.nodes_dict[this.form.node_type_2][
          "node_id"
        ];
      }
      if (this.form.link_label) {
        link_details["label_id"] = this.links_dict[this.form.link_label];
      }
      if (this.form.relationship) {
        link_details["relationship_id"] = this.relationship_dict[
          this.form.relationship
        ];
      }
      this.axios({
        url: "http://127.0.0.1:5000/api/link/",
        headers: this.auth_header,
        method: "put",
        data: link_details
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          alert("Changed link");
          this.cyUpdate();
        } else {
          alert("Failed to change new link");
        }
      });
    },
    deleteLink() {
      let link_details = {
        link_id: this.links_dict[this.form.links_name]
      };
      this.axios({
        url: "http://127.0.0.1:5000/api/link/",
        headers: this.auth_header,
        method: "delete",
        data: link_details
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          alert("Deleted Link");
          this.cyUpdate();
        } else {
          alert("Failed to delete link");
        }
      });
    },
    getMetadata() {
      this.metadata_list = [];
      let node_id = this.nodes_dict[this.selected.node]["node_id"];
      this.axios({
        url: "http://127.0.0.1:5000/api/metadata/?node_id=" + node_id,
        headers: this.auth_header,
        method: "get"
      }).then(response => {
        let response_data = response["data"].data;
        if (response_data.length != 0) {
          this.totalMetaRows = response_data.length;
          for (let i = 0; i < response_data.length; i++) {
            this.metadata_list.push({
              meta_id: response_data[i]["meta_id"],
              category: response_data[i]["category"],
              metadata: response_data[i]["metadata"]
            });
          }
        } else {
          alert("No metadata for node");
        }
      });
    },
    addMetadata() {
      let body_data = {
        node_id: this.nodes_dict[this.selected.node]["node_id"],
        category: this.form.metadata.category,
        metadata: this.form.metadata.data
      };
      this.axios({
        url: "http://127.0.0.1:5000/api/metadata/",
        headers: this.auth_header,
        method: "post",
        data: body_data
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          alert("Added metadata to node");
          this.init_metadata_list();
        } else {
          alert("Failed to add metadata to node");
        }
      });
    },
    changeMetadata() {
      let body_data = {
        meta_id: this.selected.metadata
      };
      if (this.selected.node) {
        body_data["node_id"] = this.nodes_dict[this.selected.node]["node_id"];
      }
      if (this.form.metadata.category) {
        body_data["category"] = this.form.metadata.category;
      }
      if (this.form.metadata.data) {
        body_data["metadata"] = this.form.metadata.data;
      }
      this.axios({
        url: "http://127.0.0.1:5000/api/metadata/",
        headers: this.auth_header,
        method: "put",
        data: body_data
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          alert("Changed metadata");
        } else {
          alert("Failed to change metadata");
        }
      });
    },
    deleteMetadata() {
      let body_data = {
        meta_id: this.selected.metadata
      };
      this.axios({
        url: "http://127.0.0.1:5000/api/metadata/",
        headers: this.auth_header,
        method: "delete",
        data: body_data
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          alert("Deleted metadata");
          this.init_metadata_list();
        } else {
          alert("Failed to delete metadata");
        }
      });
    },
    loadExpandCollapse() {
      this.$cytoscape.instance.then(cy => {
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
      });
    },
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
    focusNode(node) {
      this.modal_search_show = false;
      //Deselect any selected nodes
      window.api.expandAll({ animate: false });
      window.cy.nodes().unselect();
      let child_id = String(node[0]["node_id"]);
      let expandList = [cy.$id(child_id)];
      let parent = window.cy.getElementById(child_id)["_private"]["data"][
        "parent"
      ];
      if (parent) {
        //Build list for nodes that need to expanded out
        while (parent) {
          expandList.push(cy.$id(parent));
          child_id = parent;
          parent = window.cy.$id(child_id)["_private"]["data"]["parent"];
        }
        //Collapse all nodes on the map
        window.api.collapseAll();
        window.api.expandRecursively(expandList);
        // Highlight the node that was selected. Dirty way since expand has no promise
        setTimeout(function() {
          window.cy.$id(String(node[0]["node_id"])).select();
        }, 1000);
      } else {
        window.api.collapseAll();
        window.cy.$id(String(node[0]["node_id"])).select();
      }
    },
    resetVariables() {
      this.nodes_form = [];
      this.nodes_dict = {};
      this.options.label = [];
      this.labels_dict = {};
      this.links_dict = {};
      this.links_form = [];
      this.relationships_dict = {};
      this.relationship = [];
      this.search_list = [];
      this.relationships_form = [];
      this.metadata_form = [];
    },
    init_metadata_list() {
      this.metadata_form = [];
      this.axios({
        url: "http://127.0.0.1:5000/api/metadata/",
        headers: this.auth_header,
        method: "get"
      }).then(response => {
        let metadata_response = response.data["data"];
        for (let i = 0; i < metadata_response.length; i++) {
          this.metadata_form.push(metadata_response[i]["meta_id"]);
        }
      });
    }
  },
  mounted: function() {
    document.querySelectorAll("canvas").forEach(canvas => {
      canvas.style.left = "0";
    });
    //Load all map data with get requests
    this.$nextTick(this.cyUpdate);
    //Load expand collapse module
    this.$nextTick(this.loadExpandCollapse);
  }
};
</script>

<style>
#overlay-button {
  position: absolute;
  z-index: 1000;
  left: calc(100vw - 150px);
  top: calc(100vh - 100px);
}
#overlay-button-2 {
  position: absolute;
  z-index: 1000;
  left: calc(100vw - 215px);
  top: calc(100vh - 92px);
}
#holder {
  width: 100%;
  height: 95.8%;
  position: absolute;
  background-color: #cfd8dc;
}
#nodeData {
  z-index: 999;
  position: absolute;
  left: calc(100vw - 350px);
  top: calc(100vh - 300px);
}
#container {
  position: relative;
  padding-top: 45%;
}
#metadata_table {
  position: relative;
  padding-top: 30%;
}
#button_padding {
  padding-top: 10px;
}
</style>