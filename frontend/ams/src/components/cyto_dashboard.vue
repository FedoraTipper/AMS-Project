<template>
  <div>
    <b-button @click="modal_show=true" variant="primary" id="overlay-button" size="lg">+</b-button>
    <b-button @click="search_show=true" variant="primary" id="overlay-button-2" size="lg">🔍</b-button>
    <b-modal size="xl" v-model="modal_show">
      <b-card no-body>
        <b-tabs card>
          <b-tab title="Nodes" active>
            <b-card no-body>
              <b-tabs card>
                <b-tab title="Add" active>
                  <b-form @submit="addNode">
                    <b-input-group prepend="Type" required class="mt-3">
                      <b-form-input v-model="form.node_type" required/>
                    </b-input-group>
                    <b-form-group
                      id="Label_id_group"
                      label="Collection label:"
                      label-for="label_dropdown"
                    >
                      <b-form-select
                        id="label_dropdown"
                        :options="labels_form"
                        v-model="form.node_label"
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
                    <b-input-group prepend="New Type" required class="mt-3">
                      <b-form-input v-model="form.new_node_type"/>
                    </b-input-group>
                    <b-form-group
                      id="Label_id_group"
                      label="Collection label:"
                      label-for="label_dropdown"
                    >
                      <b-form-select
                        id="label_dropdown"
                        :options="labels_form"
                        v-model="form.node_label"
                      />
                    </b-form-group>
                    <b-button type="submit" variant="primary">Change Node</b-button>
                  </b-form>
                </b-tab>
              </b-tabs>
            </b-card>
          </b-tab>
          <b-tab title="Links">
            <b-card no-body>
              <b-tabs card>
                <b-tab title="Add" active>
                  <b-form @submit="addNode">
                    <b-input-group prepend="Type" required class="mt-3">
                      <b-form-input v-model="form.node_type" required/>
                    </b-input-group>
                    <b-form-group
                      id="Label_id_group"
                      label="Collection label:"
                      label-for="label_dropdown"
                    >
                      <b-form-select
                        id="label_dropdown"
                        :options="labels_form"
                        v-model="form.node_label"
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
                    <b-input-group prepend="New Type" required class="mt-3">
                      <b-form-input v-model="form.new_node_type"/>
                    </b-input-group>
                    <b-form-group
                      id="Label_id_group"
                      label="Collection label:"
                      label-for="label_dropdown"
                    >
                      <b-form-select
                        id="label_dropdown"
                        :options="labels_form"
                        v-model="form.node_label"
                      />
                    </b-form-group>
                    <b-button type="submit" variant="primary">Change Node</b-button>
                  </b-form>
                </b-tab>
              </b-tabs>
            </b-card>
          </b-tab>
          <b-tab title="Label"></b-tab>
        </b-tabs>
      </b-card>
    </b-modal>
    <div id="holder">
      <cytoscape :config="config" :preConfig="preConfig"></cytoscape>
    </div>
  </div>
</template>


<script>
import automove from "cytoscape-automove";
import cola from "cytoscape-cola";
import expandcollpase from "cytoscape-expand-collapse";

export default {
  data() {
    return {
      modal_show: false,
      search_show: false,
      form: {
        node_type: "",
        node_label: "",
        new_node_type: ""
      },
      auth_header: {
        Authorization: localStorage.getItem("Authorization")
      },
      labels_form: [],
      nodes_form: [],
      labels_dict: {},
      nodes_dict: {},
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
            selector: "edge[name]",
            style: {
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
        cy.elements().remove();
        this.nodes_form = [];
        this.nodes_dict = {};
        this.labels_form = [];
        this.labels_dict = {};
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
            cy.add({
              group: "edges",
              data: {
                id: "l" + links[i]["link_id"],
                source: links[i]["node_id_1"],
                target: links[i]["node_id_2"],
                name: relationships[links[i]["relationship_id"]]
              }
            });
          }
          let labels = values[3].data["data"];
          for (var i = 0; i < labels.length; i++) {
            this.labels_form.push(labels[i]["label_text"]);
            this.labels_dict[labels[i]["label_text"]] = labels[i]["label_id"];
          }
          cy.center();
          cy.layout({ name: "circle" }).run();
        });
      });
    },
    preConfig(cytoscape) {
      cytoscape.use(cola);
      cytoscape.use(expandcollpase);
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
#overlay-button {
  position: absolute;
  z-index: 101;
  left: calc(100vw - 100px);
  top: calc(100vh - 100px);
}
#overlay-button-2 {
  position: absolute;
  z-index: 101;
  left: calc(100vw - 165px);
  top: calc(100vh - 100px);
}
#holder {
  width: 100%;
  height: 95.8%;
  position: absolute;
  background-color: #cfd8dc;
}
</style>