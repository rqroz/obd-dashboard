<template>
  <v-dialog v-model="dialog" max-width="600px">
    <template v-slot:activator="{ on }">
      <v-list-item link v-on="on">
        <v-list-item-action>
          <v-icon>mdi-account-edit</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>Update Personal Info</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </template>

    <v-card>
      <v-card-title>
        <span class="headline">Update Personal Info</span>
      </v-card-title>
      <v-card-text>
        <form-base
          btn-text="Update"
          btn-icon="mdi-account-edit"
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
        </form-base>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { DEFINE_USER } from '@/store/modules/user/actions';

import FormBase from '@/components/forms/Base';

import FORM_RULES from '@/resources/forms/rules';


export default {
  components: {
    FormBase,
  },
  data: vm => ({
    endpoint: '/profile/',
    dialog: false,
    model: vm.genModel('', '', ''),
    mounted: false,
    rules: {
      email: FORM_RULES.email,
      required: FORM_RULES.required,
      nameLength: value => value.length >= 3 || 'This field must have at least 3 characters',
    },
  }),
  computed: {
    loading() {
      return this.$refs.form.loading;
    },
  },
  methods: {
    genModel(first_name, last_name, email) {
      return { first_name, last_name, email };
    },
    successHandler(response) {
      this.$store.dispatch(DEFINE_USER, { user: response.data.user });
      this.dialog = false;
    },
    errorHandler(error) {
      console.log(error);
    },
  },
  mounted() {
    const user = this.$store.getters.user;
    if (user) {
      this.model = this.genModel(user.first_name, user.last_name, user.email);
    }

    this.mounted = true;
  },
};
</script>
