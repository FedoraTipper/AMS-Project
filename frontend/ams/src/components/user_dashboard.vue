<template>
  <div>
    <b-container fluid>
      <b-card-group>
        <b-card id="user_form" title="Change password">
          <b-form @submit="change_password">
            <b-input-group prepend="Username" required class="mt-3">
              <b-form-input v-model="form.username" disabled/>
            </b-input-group>
            <b-input-group prepend="Current Password" required class="mt-3">
              <b-form-input v-model="form.old_password" type="password" required/>
            </b-input-group>
            <b-input-group prepend="New Password" required class="mt-3">
              <b-form-input v-model="form.password" type="password" required/>
            </b-input-group>
            <b-input-group prepend="Confirm New Password" required class="mt-3">
              <b-form-input v-model="form.confirm_password" type="password" required/>
            </b-input-group>
            <b-button type="submit" variant="primary">Change Password</b-button>
          </b-form>
        </b-card>
      </b-card-group>
    </b-container>
  </div>
</template>

<script>
import crypto from "crypto";
export default {
  data() {
    return {
      auth_header: {
        Authorization: localStorage.getItem("Authorization")
      },
      logs_form: [],
      form: {
        username: localStorage.getItem("User"),
        old_password: "",
        password: "",
        confirm_password: "",
        privilege: 0
      }
    };
  },
  methods: {
    change_password() {
      let user_details = {};
      if (this.form.password == this.form.old_password) {
        alert("New and old password is the same");
        return false;
      }
      if (this.form.password == this.form.confirm_password) {
        const hash = crypto.createHash("sha256");

        user_details["old_password"] = hash
          .update(this.form.old_password, "utf-8")
          .digest()
          .toString("hex");
        const new_hash = crypto.createHash("sha256");
        user_details["new_password"] = new_hash
          .update(this.form.password, "utf-8")
          .digest()
          .toString("hex");

        this.axios({
          url: "http://127.0.0.1:5000/api/password/",
          headers: this.auth_header,
          method: "put",
          data: user_details
        }).then(response => {
          if (response.data["message"].includes("Success")) {
            alert("Password changed");
          } else {
            alert("Failed to change password");
          }
        });
      } else {
        alert("Passwords do not match");
      }
    }
  }
};
</script>

<style>
#user_form {
  width: 65%;
  right: 19%;
  margin-top: 4%;
  position: absolute;
}
</style>
