<template>
  <v-skeleton-loader
    type="list-item-three-line"
    :loading="loading"
  >
    <v-card elevation="3">
      <v-card-title class="subtitle-1 font-weight-regular">
        {{ average ? average.toFixed(2) : '-' }} %
        <v-spacer />
        <v-icon>mdi-engine</v-icon>
      </v-card-title>
      <v-card-subtitle>Average Engine Load</v-card-subtitle>
    </v-card>
  </v-skeleton-loader>
</template>

<script>
import fetchMixin from '@/mixins/fetchMixin';

export default {
  mixins: [fetchMixin],
  data: () => ({
    endpoint: '/engine/load/average/',
    average: null,
  }),
  methods: {
    successHandler(response) {
      this.average = response.data.average;
    },
    errorHandler(error) {
      console.log(error);
    },
  },
};
</script>
