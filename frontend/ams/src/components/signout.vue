<template></template>

<script>
import store from "../store/store";
export default {
  methods: {
    signout() {
      localStorage.clear();
      store.commit("clear");
      this.$router.push("/");
    }
  },
  mounted: function() {
    this.signout();
  }
};
</script>