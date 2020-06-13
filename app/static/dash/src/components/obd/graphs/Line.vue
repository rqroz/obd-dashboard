<template>
  <v-card elevation="3">
    <v-card-title class="justify-center">
      Line Graphs
    </v-card-title>
    <v-card-subtitle class="d-flex justify-center">
      See line charts for your data, organized by session.
    </v-card-subtitle>
    <v-card-text>
      <embed :src="endpoint" width="100%" height="800" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    endpoint: '/dash/lines/',
  }),
};
</script>
