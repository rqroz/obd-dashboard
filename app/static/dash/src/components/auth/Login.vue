<template>
  <form-base
    btn-text="Login"
    btn-icon="mdi-login-variant"
    :endpoint="endpoint"
    :model="model"
    @success="successHandler"
    @error="errorHandler"
  >
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
  data: () => ({
    endpoint: '/login/',
    model: {
      email: '',
      password: '',
    },
    rules: FORM_RULES,
    secret: true,
  }),
  methods: {
    successHandler(response) {
      console.log(response);
      this.$store.dispatch(DEFINE_USER, { user: response.data.user });
    },
    errorHandler(error) {
      console.log(error);
    }
  },
}
</script>
