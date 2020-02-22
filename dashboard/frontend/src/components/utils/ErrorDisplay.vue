<template>
  <div>
    <v-alert
      v-for="(error, idx) in errors"
      v-bind:key="idx"
      class="text-small"
      type="error"
      dense
      dismissible
    >
      {{ error }}
    </v-alert>
  </div>
</template>

<script>
export default {
  props: {
    errors: {
      type: Array,
      default: () => [],
    },
  },
};
</script>
