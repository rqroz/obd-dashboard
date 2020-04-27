<template>
  <v-skeleton-loader
    type="list-item-three-line"
    :loading="loading"
  >
    <v-card elevation="3">
      <v-card-title class="subtitle-1 font-weight-regular">
        {{ level ? level.toFixed(2) : '-' }} %
        <v-spacer />
        <v-icon>mdi-gas-station</v-icon>
      </v-card-title>
      <v-card-subtitle>Fuel Level</v-card-subtitle>
    </v-card>
  </v-skeleton-loader>
</template>

<script>
import fetchMixin from '@/mixins/fetchMixin';

export default {
  mixins: [fetchMixin],
  data: () => ({
    endpoint: '/fuel/level/latest/',
    level: null,
  }),
  methods: {
    successHandler(response) {
      this.level = Number(response.data.level);
    },
    errorHandler(error) {
      console.log(error);
    },
  },
};
</script>
