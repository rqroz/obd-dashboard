<template>
  <simple-fetch-card
    icon="mdi-car-battery"
    subtitle="Battery Status"
    :endpoint="endpoint"
    :message="message"
    :title="average ? `${average.toFixed(2)} V` : '-'"
    @success="successHandler"
    @error="errorHandler"
  />
</template>

<script>
import SimpleFetchCard from '@/components/utils/cards/SimpleFetch';

export default {
  name: 'BatteryCard',
  components: {
    SimpleFetchCard,
  },
  data: () => ({
    endpoint: '/engine/battery/latest/',
    average: null,
    message: null,
  }),
  methods: {
    successHandler(response) {
      this.average = parseFloat(response.data.value);
      this.message = response.data.message;
    },
    errorHandler(error) {
      console.log(error);
    },
  },
};
</script>
