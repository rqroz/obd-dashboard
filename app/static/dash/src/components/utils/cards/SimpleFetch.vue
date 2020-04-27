<template>
  <v-skeleton-loader
    type="list-item-three-line"
    :loading="loading"
  >
    <v-card elevation="3">
      <v-card-title class="subtitle-1 font-weight-regular">
        {{ title || '-' }}
        <v-spacer />
        <v-icon v-if="icon">{{ icon }}</v-icon>
      </v-card-title>
      <v-card-subtitle v-if="subtitle">{{ subtitle }}</v-card-subtitle>
    </v-card>
  </v-skeleton-loader>
</template>

<script>
import fetchMixin from '@/mixins/fetchMixin';

export default {
  name: 'SimpleFetchCard',
  mixins: [fetchMixin],
  props: {
    endpoint: {
      type: String,
      required: true,
    },
    icon: String,
    subtitle: String,
    title: {
      type: String,
      required: true,
    },
  },
  methods: {
    successHandler(response) {
      this.$emit('success', response);
    },
    errorHandler(error) {
      this.$emit('error', error);
    },
  },
};
</script>
