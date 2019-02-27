<template>
  <div>
    <b-form @submit="onSubmit" class>
      <b-form-group id="Username_output" label="Username:">
        <b-form-input
          id="username_fld"
          type="text"
          v-model="form.username"
          required
          placeholder="Enter username"
        />
      </b-form-group>

      <b-form-group id="Password Group" label="Password:" label-for="exampleInput2">
        <b-form-input
          id="exampleInput2"
          type="password"
          v-model="form.password"
          required
          placeholder="Enter password"
        />
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      var details = JSON.stringify(this.form);
      this.axios
        .post("http://127.0.0.1:5000/api/auth/", details)
        .then(response => {
          var auth_token = response.headers["authorization"];
          localStorage.setItem("Authorization", auth_token);
          this.$router.push("/cyto");
        })
        .catch(error => console.log(error));
    }
  }
};
</script>