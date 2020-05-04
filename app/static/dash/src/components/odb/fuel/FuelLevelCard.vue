<template>
  <simple-fetch-card
    icon="mdi-gas-station"
    subtitle="Fuel Level"
    :endpoint="endpoint"
    :title="level ? `${level.toFixed(2)} %` : '-'"
    @success="successHandler"
    @error="errorHandler"
  />
</template>

<script>
import SimpleFetchCard from '@/components/utils/cards/SimpleFetch';

export default {
  components: {
    SimpleFetchCard,
  },
  data: () => ({
    endpoint: '/fuel/level/latest/',
    level: null,
  }),
  methods: {
    successHandler(response) {
      this.level = parseFloat(response.data.level);
    },
    errorHandler(error) {
      console.log(error);
    },
  },
};
</script>
