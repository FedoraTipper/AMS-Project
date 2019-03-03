<template>
  <div>
    <b-container fluid>
      <!-- User Interface controls -->
      <b-card-group class="text-center" id="log_table">
        <b-row>
          <b-col md="8" class="my-1">
            <b-form-group label-cols-sm="3" label="Filter" class="mb-0">
              <b-input-group>
                <b-form-input v-model="filter" placeholder="Type to Search"/>
                <b-input-group-append>
                  <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                </b-input-group-append>
              </b-input-group>
            </b-form-group>
          </b-col>

          <b-col md="8" class="my-1">
            <b-form-group label-cols-sm="3" label="Per page" class="mb-0">
              <b-form-select :options="pageOptions" v-model="perPage"/>
            </b-form-group>
          </b-col>
        </b-row>

        <!-- Main table element -->
        <b-table
          show-empty
          stacked="md"
          :items="logs_form"
          :fields="fields"
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
              :total-rows="totalRows"
              :per-page="perPage"
              v-model="currentPage"
              class="my-0"
            />
          </b-col>
        </b-row>
      </b-card-group>
      <b-card-group>
        <b-card id="user_form" title="Add user">
          <b-form @submit="addUser">
            <b-input-group prepend="Username" required class="mt-3">
              <b-form-input v-model="form.username" required/>
            </b-input-group>
            <b-input-group prepend="Password" required class="mt-3">
              <b-form-input v-model="form.username" required/>
            </b-input-group>
            <b-form-group id="privilege" label="Privilege" label-for="privilege">
              <b-form-select id="privilege_dropdown" :options="[0,1]" v-model="form.node_label"/>
            </b-form-group>
            <b-button type="submit" variant="primary">Add Node</b-button>
          </b-form>
        </b-card>
      </b-card-group>
    </b-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      auth_header: {
        Authorization: localStorage.getItem("Authorization")
      },
      logs_form: [],
      form: {
        username: "",
        password: "",
        privilege: 0
      },
      fields: {
        message: {
          label: "Logs"
        }
      },
      totalRows: "10000",
      currentPage: 1,
      filter: null,
      pageOptions: [5, 10, 15],
      perPage: 5
    };
  },
  methods: {
    load_logs() {
      const requests = [
        this.axios({
          url: "http://127.0.0.1:5000/api/logs/",
          headers: this.auth_header,
          method: "get"
        })
      ];
      Promise.all(requests).then(values => {
        let logs = values[0].data["data"];
        this.totalRows = logs.length;
        for (let i = logs.length - 1; i > 0; i--) {
          this.logs_form.push({ message: logs[i]["message"] });
        }
      });
    },
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
    addUser() {}
  },
  mounted: function() {
    this.load_logs();
  }
};
</script>

<style>
#log_table {
  top: 6%;
  width: 65%;
  right: 19%;
  position: absolute;
}
#user_form {
  top: 65%;
  width: 65%;
  right: 19%;
  position: absolute;
}
</style>
