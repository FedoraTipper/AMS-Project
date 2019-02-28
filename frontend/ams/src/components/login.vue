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

      <b-alert
        :show="dismissCountDown"
        dismissible
        variant="danger"
        fade
        @dismissed="dismissCountDown=0"
        @dismiss-count-down="countDownChanged"
      >
        <p>Incorrect username/password</p>
      </b-alert>
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
      },
      dismissSecs: 5,
      dismissCountDown: 0,
      showDismissibleAlert: false
    };
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    showAlert() {
      this.dismissCountDown = this.dismissSecs;
    },
    onSubmit(evt) {
      evt.preventDefault();
      var details = JSON.stringify(this.form);
      this.axios
        .post("http://127.0.0.1:5000/api/auth/", details)
        .then(response => {
          if (response.data["message"].includes("Authenticated")) {
            var auth_token = response.headers["authorization"];
            localStorage.setItem("Authorization", auth_token);
            this.$router.push("/cyto");
          } else {
            this.dismissCountDown = this.dismissSecs;
          }
        })
        .catch(error => console.log(error));
    }
  }
};
</script>