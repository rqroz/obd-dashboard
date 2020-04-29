<template>
  <v-card elevation="3">
    <v-card-title class="justify-center">
      Driver Profile
    </v-card-title>
    <v-card-subtitle class="d-flex justify-center">
      Select one or more sessions to see your unique blueprints.
    </v-card-subtitle>
    <v-card-text>
      <embed :src="endpoint" width="100%" height="540" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    endpoint: '/dash/profile/',
  }),
};
</script>
