<template>
  <v-dialog v-model="dialog" persistent width="500">
      <template v-slot:activator="{ on }">
        <v-btn text v-on="on">
          <v-icon>mdi-logout</v-icon>
          Logout
        </v-btn>
      </template>

      <v-card>
        <v-card-title primary-title>
          Are you sure you want to log out?
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" :disabled="loading" text @click="dialog = false">
            Go Back
          </v-btn>
          <v-btn color="error" :loading="loading" text @click="logout">
            Yes, log me out
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import { CLEAR_USER } from '@/store/modules/user/actions';

export default {
  data: () => ({
    dialog: false,
    loading: false,
  }),
  methods: {
    logout() {
      this.loading = true;
      this.$requests.post('/logout/')
        .then(() => {
          this.$store.dispatch(CLEAR_USER);
          this.dialog = false;
          this.loading = false;
        })
        .catch((error) => {
          console.log(error.response);
          this.loading = false;
        });
    },
  },
};
</script>
