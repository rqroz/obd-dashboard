<template>
  <simple-fetch-card
    icon="mdi-gauge"
    subtitle="Average RPM"
    :endpoint="endpoint"
    :title="average ? average.toFixed(0) : '-'"
    @success="successHandler"
    @error="errorHandler"
  />
</template>

<script>
import SimpleFetchCard from '@/components/utils/cards/SimpleFetch';

export default {
  name: 'EngineRpmAverageCard',
  components: {
    SimpleFetchCard,
  },
  data: () => ({
    endpoint: '/engine/rpm/average/',
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
