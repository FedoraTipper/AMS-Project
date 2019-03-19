<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-brand href="#/cyto">ASM System</b-navbar-brand>

      <b-navbar-toggle target="nav_collapse"/>

      <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav>
          <b-nav-item v-if="privilege" href="#/admin">Admin Dashboard</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav v-if="user_show" class="ml-auto">
          <b-nav-item-dropdown right>
            <!-- Using button-content slot -->
            <template slot="button-content">
              <em>{{username}}</em>
            </template>
            <b-dropdown-item href="#/userprofile">Profile</b-dropdown-item>
            <b-dropdown-item href="#/signout">Signout</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>


<script>
import store from "../store/store";
export default {
  computed: {
    privilege: () => store.state.privilege,
    username: () => store.state.username,
    user_show: () => store.state.user_show
  },
  methods: {
    load_variables() {
      let privilege = localStorage.getItem("Privilege");
      let user = localStorage.getItem("User");
      if (privilege && privilege == "true") {
        store.commit("set_privilege", true);
      }
      if (user) {
        store.commit("set_username", user);
      }
    }
  },
  mounted: function() {
    this.load_variables();
  }
};
</script>
