<template>
  <v-form ref="form" v-model="valid">
    <v-row>
      <v-col>
        <v-text-field
          v-model="model.first_name"
          :rules="[rules.required, rules.nameLength]"
          label="First Name"
          counter
        />
        <v-text-field
          v-model="model.last_name"
          :rules="[rules.required, rules.nameLength]"
          label="Last Name"
          counter
        />
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
        <v-text-field
          v-model="model.confirmPassword"
          :append-icon="secret ? 'mdi-eye-off' : 'mdi-eye'"
          :rules="[rules.required, rules.passwordLength, rules.passwordsMatch]"
          :type="secret ? 'password' : 'text'"
          label="Confirm Password"
          counter
          @click:append="secret = !secret"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col class="d-flex justify-end">
        <v-btn color="primary" :disabled="!valid" @click="validate">
          <v-icon class="mr-1">mdi-login</v-icon>
          Register
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import FORM_RULES from '@/resources/forms/rules';

export default {
  data() {
    return {
      secret: true,
      valid: false,
      model: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirmPassword: '',
      },
      rules: {
        email: FORM_RULES.email,
        passwordLength: FORM_RULES.passwordLength,
        required: FORM_RULES.required,
        passwordsMatch: value => value === this.model.password || 'The passwords don\'t match',
        nameLength: value => value.length >= 5 || 'This field must have at least 5 characters',
      },
    };
  },

  methods: {
    validate () {
      if (!this.$refs.form.validate()) { return; }

      // TODO: Use requests to apply registration
    },
  },
}
</script>
