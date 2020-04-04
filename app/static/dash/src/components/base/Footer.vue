<style scoped>
.app-footer {
  min-height: 36px !important;
}
</style>

<template>
  <v-footer app class="overline app-footer">
    &copy; {{year}} Rodolfo Queiroz
  </v-footer>
</template>


<script>
export default {
  data: () => ({
    year: (new Date()).getFullYear(),
  }),
};
</script>
