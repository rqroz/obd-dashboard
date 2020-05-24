<template>
  <simple-fetch-card
    icon="mdi-speedometer"
    subtitle="Historical Speed Average"
    :dynamic="false"
    :endpoint="endpoint"
    :title="average !== null  ? `${average.toFixed(2)} Km/h` : '-'"
    @success="successHandler"
    @error="errorHandler"
  />
</template>

<script>
import SimpleFetchCard from '@/components/utils/cards/SimpleFetch';

export default {
  name: 'SpeedAverageCard',
  components: {
    SimpleFetchCard,
  },
  data: () => ({
    endpoint: '/engine/speed/average/',
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
