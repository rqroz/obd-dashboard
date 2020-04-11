<template>
  <v-card elevation="3">
    <v-card-title class="subtitle-1 font-weight-regular">
      {{ user.first_name }} {{ user.last_name }}
      <v-spacer />
      <v-icon>mdi-car-connected</v-icon>
    </v-card-title>
    <v-card-subtitle>{{ user.email }}</v-card-subtitle>
  </v-card>
</template>

<script>
export default {
  computed: {
    user() {
      return this.$store.getters.user;
    },
  },
};
</script>
