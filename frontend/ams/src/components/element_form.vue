<template>
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
</template>
