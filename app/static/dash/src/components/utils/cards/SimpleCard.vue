<style scoped>
.cursor-help {
  cursor: help;
}
</style>

<template>
  <v-card elevation="3">
    <v-card-title class="subtitle-1 font-weight-regular">
      {{ title || '-' }}
      <v-spacer />
      <span v-if="icon">
        <v-tooltip v-if="message" bottom>
          <template v-slot:activator="{ on }">
            <v-icon v-on="on" class="cursor-help" :color="iconColor">
              {{ icon }}
            </v-icon>
          </template>
          <span>{{ message }}</span>
        </v-tooltip>
        <v-icon v-else>
          {{ icon }}
        </v-icon>
      </span>
    </v-card-title>
    <v-card-subtitle v-if="subtitle">{{ subtitle }}</v-card-subtitle>
  </v-card>
</template>

<script>
export default {
  name: 'SimpleCard',
  props: {
    icon: String,
    iconColor: String,
    message: String,
    subtitle: String,
    title: {
      type: String,
      required: true,
    },
  },
};
</script>
