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
    <b-button @click="search_show=true" variant="primary" id="overlay-button-2" size="lg">🔍</b-button>
    <b-modal size="xl" v-model="modal_node_show">
      <b-tabs card>
        <b-tab title="Add" active>
          <b-form @submit="addNode">
            <b-input-group prepend="Type" required class="mt-3">
              <b-form-input v-model="form.node_type" required/>
            </b-input-group>
            <b-form-group id="Label_id_group" label="Collection label:" label-for="label_dropdown">
              <b-form-select id="label_dropdown" :options="labels_form" v-model="form.node_label"/>
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
            <b-input-group prepend="New Type" required class="mt-3">
              <b-form-input v-model="form.new_node_type"/>
            </b-input-group>
            <b-form-group id="Label_id_group" label="Collection label:" label-for="label_dropdown">
              <b-form-select id="label_dropdown" :options="labels_form" v-model="form.node_label"/>
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
              <b-form-select id="label_dropdown" :options="labels_form" v-model="form.link_label"/>
            </b-form-group>
            <b-form-group label="Relationship:" label-for="label_dropdown">
              <b-form-select :options="relationship_form" v-model="form.relationship"/>
            </b-form-group>
            <b-button type="submit" variant="primary">Add Link</b-button>
          </b-form>
        </b-tab>
        <b-tab title="Change">
          <b-form @submit="changeLink">
            <b-form-group label="Select link:">
              <b-form-select :options="links_form" required v-model="form.link_type"/>
            </b-form-group>
            <b-input-group prepend="New Type" required class="mt-3">
              <b-form-input v-model="form.new_node_type"/>
            </b-input-group>
            <b-form-group id="Label_id_group" label="Collection label:" label-for="label_dropdown">
              <b-form-select id="label_dropdown" :options="labels_form" v-model="form.node_label"/>
            </b-form-group>
            <b-button type="submit" variant="primary">Change Node</b-button>
          </b-form>
        </b-tab>
        <b-tab title="Delete">
          <b-form @submit="deleteLink">
            <b-form-group label="Select link to delete:" required>
              <b-form-select :options="links_form" required v-model="form.links_name"/>
            </b-form-group>
            <b-button type="submit" variant="danger">Delete Node</b-button>
          </b-form>
        </b-tab>
      </b-tabs>
    </b-modal>
    <b-modal size="xl" v-model="modal_metadata_show">
      <b-tabs card>
        <b-tab title="Add" active>
          <b-form @submit="addNode">
            <b-input-group prepend="Type" required class="mt-3">
              <b-form-input v-model="form.node_type" required/>
            </b-input-group>
            <b-form-group id="Label_id_group" label="Collection label:" label-for="label_dropdown">
              <b-form-select id="label_dropdown" :options="labels_form" v-model="form.node_label"/>
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
            <b-input-group prepend="New Type" required class="mt-3">
              <b-form-input v-model="form.new_node_type"/>
            </b-input-group>
            <b-form-group id="Label_id_group" label="Collection label:" label-for="label_dropdown">
              <b-form-select id="label_dropdown" :options="labels_form" v-model="form.node_label"/>
            </b-form-group>
            <b-button type="submit" variant="primary">Change Node</b-button>
          </b-form>
        </b-tab>
      </b-tabs>
    </b-modal>
    <div id="holder">
      <cytoscape :config="config" :preConfig="preConfig"></cytoscape>
    </div>
  </div>
</template>


<script>
import jquery from "jquery";
import automove from "cytoscape-automove";
import cola from "cytoscape-cola";
import expandcollapse from "cytoscape-expand-collapse";
import cosebilkent from "cytoscape-cose-bilkent";

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
        relationship: ""
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
      relationship_dict: {},
      config: {
        panningEnabled: true,
        fit: true,
        animate: true,
        boxSelectionEnabled: true,
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
      }
    };
  },
  methods: {
    cyUpdate() {
      this.$cytoscape.instance.then(cy => {
        cy.elements().remove();
        this.nodes_form = [];
        this.nodes_dict = {};
        this.labels_form = [];
        this.labels_dict = {};
        this.links_dict = {};
        this.links_form = [];
        this.relationships_dict = {};
        this.relationship = [];
        this.relationships_form = [];
        let nodes = [];
        let links = [];
        let relationships = {};
        let colletion = cy.collection();
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

          for (var i = 0; i < nodes.length; i++) {
            this.nodes_form.push(nodes[i]["type"]);
            this.nodes_dict[nodes[i]["type"]] = nodes[i]["node_id"];
            cy.add({
              group: "nodes",
              data: {
                id: nodes[i]["node_id"],
                name: nodes[i]["type"]
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
          let labels = values[3].data["data"];
          for (var i = 0; i < labels.length; i++) {
            this.labels_form.push(labels[i]["label_text"]);
            this.labels_dict[labels[i]["label_text"]] = labels[i]["label_id"];
          }
          cy.center();
          var api = cy.expandCollapse("get");
          window.cy = cy;
          console.log(api);
          cy.layout({ name: "cose-bilkent" }).run();
        });
      });
    },
    preConfig(cytoscape) {
      cytoscape.use(cola);
      cytoscape.use(expandcollapse);
      cytoscape.use(cosebilkent);
    },
    addNode() {
      let node_details = {
        type: this.form.node_type
      };
      if (this.form.node_label) {
        node_details["label_id"] = this.labels_dict[this.form.node_label];
      }
      this.axios({
        url: "http://127.0.0.1:5000/api/node/",
        headers: this.auth_header,
        method: "post",
        data: node_details
      }).then(response => {
        if (response.data["message"].includes("Success")) {
          this.cyUpdate();
        } else {
          alert("Failed to create new node");
        }
      });
    },
    changeNode() {
      let node_details = {
        node_id: this.nodes_dict[this.form.node_type]
      };
      if (this.form.node_label) {
        node_details["label_id"] = this.labels_dict[this.form.node_label];
      }
      if (this.form.new_node_type) {
        node_details["type"] = this.form.new_node_type;
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
          alert("Failed to change node");
        }
      });
    },
    deleteNode() {
      let node_details = {
        node_id: this.nodes_dict[this.form.node_type]
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
        node_id_1: this.nodes_dict[this.form.node_type_1],
        node_id_2: this.nodes_dict[this.form.node_type_2]
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
          this.cyUpdate();
          alert("Created link");
        } else {
          alert("Failed to create new link");
        }
      });
    },
    changeLink() {},
    deleteLink() {
      console.log(this.form.links_name);
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
    addMetadata() {},
    changeMetadata() {},
    deleteMetadata() {}
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
#overlay-button {
  position: absolute;
  z-index: 101;
  left: calc(100vw - 150px);
  top: calc(100vh - 100px);
}
#overlay-button-2 {
  position: absolute;
  z-index: 101;
  left: calc(100vw - 215px);
  top: calc(100vh - 92px);
}
#holder {
  width: 100%;
  height: 95.8%;
  position: absolute;
  background-color: #cfd8dc;
}
</style>