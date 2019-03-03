<template></template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    signout() {
      localStorage.clear();
      this.$router.push("/");
    }
  },
  mounted: function() {
    this.signout();
  }
};
</script>