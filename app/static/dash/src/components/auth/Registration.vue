<template>
  <form-base
    btn-text="Register"
    btn-icon="mdi-login-variant"
    :endpoint="endpoint"
    :model="model"
    @success="successHandler"
    @error="errorHandler"
  >
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
      v-model="model.confirm_password"
      :append-icon="secret ? 'mdi-eye-off' : 'mdi-eye'"
      :rules="[rules.required, rules.passwordLength, rules.passwordsMatch]"
      :type="secret ? 'password' : 'text'"
      label="Confirm Password"
      counter
      @click:append="secret = !secret"
    />
  </form-base>
</template>

<script>
import { DEFINE_USER } from '@/store/modules/user/actions';

import FormBase from '@/components/forms/Base';
import FORM_RULES from '@/resources/forms/rules';


export default {
  components: {
    FormBase,
  },
  data() {
    return {
      endpoint: '/register/',
      model: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '',
      },
      secret: true,
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
    successHandler(response) {
      this.$store.dispatch(DEFINE_USER, { user: response.data.user });
    },
    errorHandler(error) {
      console.log(error);
    }
  },
}
</script>
