<style scoped>
.app-footer {
  min-height: 36px !important;
}
</style>

<template>
  <v-footer app class="overline app-footer">
    &copy; {{year}} Rodolfo Queiroz
    <v-spacer/>
    <v-switch
      v-model="$vuetify.theme.dark"
      color="primary"
      class="mt-0"
      hide-details
    >
      <template v-slot:label>
        <span class="overline">Dark Theme</span>
      </template>
    </v-switch>
  </v-footer>
</template>


<script>
export default {
  data: () => ({
    year: (new Date()).getFullYear(),
  }),
};
</script>
