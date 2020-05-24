<template>
  <simple-fetch-card
    icon="mdi-car-battery"
    subtitle="Battery Status"
    :endpoint="endpoint"
    :message="message"
    :icon-color="iconColor"
    :title="read ? `${read.toFixed(2)} V` : '-'"
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
    read: null,
    message: null,
    iconColor: null,
  }),
  methods: {
    successHandler(response) {
      const isInDanger = response.data.value < response.data.min;
      this.message = isInDanger ?
        'Your battery\'s voltage is under the minimum threshold. Please change the battery ASAP.' :
        'Your car battery level is within the ideal range.';
      this.iconColor = isInDanger ? 'error' : 'primary';
      this.read = parseFloat(response.data.value);
    },
    errorHandler(error) {
      console.log(error);
    },
  },
};
</script>
