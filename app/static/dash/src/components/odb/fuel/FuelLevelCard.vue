<template>
  <simple-fetch-card
    icon="mdi-gas-station"
    subtitle="Fuel Level"
    :endpoint="endpoint"
    :message="message"
    :icon-color="iconColor"
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
    message: null,
    iconColor: null,
  }),
  methods: {
    successHandler(response) {
      this.level = parseFloat(response.data.value);
      if (this.level) {
        if (this.level < 25) {
          this.message = 'You are starting to run out of gas...';
          this.iconColor = 'warning';
        } else if (this.level < 10) {
          this.message = 'Time to refuel!';
          this.iconColor = 'error';
        } else {
          this.message = 'You don\'t need to worry about gas for now.';
          this.iconColor = 'primary';
        }
      }
    },
    errorHandler(error) {
      console.log(error);
    },
  },
};
</script>
