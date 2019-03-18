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
export default {
  data() {
    return {
      privilege: false,
      username: "User",
      user_show: false
    };
  },
  methods: {
    load_variables() {
      let priv = localStorage.getItem("Privilege");
      let user = localStorage.getItem("User");
      if (priv && priv == "true") {
        this.privilege = window.privilege = true;
      }
      if (user) {
        this.user_show = true;
        this.username = window.username = user;
      }
    }
  },
  mounted: function() {
    this.load_variables();
  }
};
</script>
