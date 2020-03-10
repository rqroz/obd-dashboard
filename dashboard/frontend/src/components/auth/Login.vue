<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col>
        <v-card
          class="mx-auto"
          max-width="400"
        >
          <v-card-text class="text--primary">
            <v-form
              ref="form"
              v-model="valid"
              lazy-validation
              @keyup.enter.native="submit"
            >
              <v-text-field
                v-model="model.email"
                :rules="rules.email"
                label="E-mail"
                required
              />
              <v-text-field
                v-model="model.password"
                :rules="rules.password"
                label="Senha"
                type="password"
                required
              />

              <v-btn
                :disabled="!valid"
                :loading="loading"
                color="success"
                class="mr-4"
                @click="submit"
              >
                Submit
              </v-btn>
            </v-form>
          </v-card-text >
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    data: () => ({
      valid: false,
      loading: false,
      model: {
        email: null,
        password: null,
      },
      rules: {
        email: [
          v => !!v || 'E-mail is required',
          v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
        ],
        password: [
          v => !!v || 'Password is required',
          v => (v && v.length >= 8) || 'Password must have at least 8 characters',
        ],
      },
    }),
    methods: {
      submit() {
        if (!this.$refs.form.validate()) { return; }
        this.loading = true;
        this.$requests.post('/api-auth/login/', this.model)
          .then((response) => {
            // eslint-disable-next-line
            console.log('success', response);
          })
          // eslint-disable-next-line
          .catch((err) => console.log('failure', err.response))
          .then(() => this.loading = false);
      },
    },
  }
</script>
