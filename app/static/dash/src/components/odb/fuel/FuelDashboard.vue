<template>
  <v-card elevation="3">
    <v-card-title>
      TITLE HERE
    </v-card-title>
    <v-card-text>
      <embed :src="endpoint" width="100%" height="800" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    endpoint: '/dash/',
  }),
};
</script>
