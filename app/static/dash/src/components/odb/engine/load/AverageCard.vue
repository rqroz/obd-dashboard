<template>
  <simple-fetch-card
    icon="mdi-engine"
    subtitle="Average Engine Load"
    :endpoint="endpoint"
    :title="average ? `${average.toFixed(2)} %` : '-'"
    @success="successHandler"
    @error="errorHandler"
  />
</template>

<script>
import SimpleFetchCard from '@/components/utils/cards/SimpleFetch';

export default {
  name: 'EngineLoadAverageCard',
  components: {
    SimpleFetchCard,
  },
  data: () => ({
    endpoint: '/engine/load/average/',
    average: null,
  }),
  methods: {
    successHandler(response) {
      this.average = parseFloat(response.data.average);
    },
    errorHandler(error) {
      console.log(error);
    },
  },
};
</script>
