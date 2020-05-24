<template>
  <simple-fetch-card
    icon="mdi-speedometer"
    subtitle="Historical Speed Average"
    :dynamic="false"
    :endpoint="endpoint"
    :title="valid ? `${average.toFixed(2)} Km/h` : '-'"
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
    valid: false,
  }),
  methods: {
    successHandler(response) {
      this.average = parseFloat(response.data.average);
      this.valid = typeof this.average === 'number';
    },
    errorHandler(error) {
      console.log(error);
    },
  },
};
</script>
