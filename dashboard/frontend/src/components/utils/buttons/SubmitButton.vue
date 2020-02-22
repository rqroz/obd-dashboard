<template>
  <v-btn
    :loading="loading"
    :disabled="loading"
    :color="color"
    @click="$emit('submit')"
  >
    {{ text }}
    <v-icon v-if="icon" right>{{ icon }}</v-icon>
  </v-btn>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true,
    },
    color: {
      type: String,
      default: 'info darken-1',
    },
    icon: String,
    loading: Boolean,
    disabled: Boolean,
  },
};
</script>
