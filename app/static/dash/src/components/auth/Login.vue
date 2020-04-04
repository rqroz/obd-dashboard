<template>
  <v-form ref="form" v-model="valid">
    <v-row>
      <v-col>
        <v-text-field
          v-model="model.email"
          :rules="[rules.required, rules.email]"
          label="E-mail"
          required
        />

        <v-text-field
          v-model="model.password"
          :append-icon="secret ? 'mdi-eye-off' : 'mdi-eye'"
          :rules="[rules.required, rules.passwordLength]"
          :type="secret ? 'password' : 'text'"
          label="Password"
          counter
          @click:append="secret = !secret"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col class="d-flex justify-end">
        <v-btn color="primary" :disabled="!valid" @click="validate">
          <v-icon class="mr-1">mdi-login-variant</v-icon>
          Enter
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import FORM_RULES from '@/resources/forms/rules';

export default {
  data: () => ({
    secret: true,
    valid: false,
    model: {
      email: '',
      password: '',
    },
    rules: FORM_RULES,
  }),

  methods: {
    validate () {
      if (!this.$refs.form.validate()) { return; }

      // TODO: Use requests to apply registration
      console.log(this.$requests);
    },
  },
}
</script>
