<template>
  <v-app-bar
    app
    :clipped-left="$vuetify.breakpoint.lgAndUp"
  >
    <v-app-bar-nav-icon v-if="user" @click.stop="toggleDrawer" />
    <v-toolbar-title class="headline pointer-cursor">
      <router-link :to="{ name: 'Index' }" tag="button" class="text-uppercase">
        <span class="font-weight-light">ODB II - Dashboard</span>
      </router-link>
    </v-toolbar-title>
  </v-app-bar>
</template>

<script>
import { mapMutations, mapState } from 'vuex';

export default {
  computed: {
    ...mapState('user', ['user']),
  },
  methods: {
    ...mapMutations('app', ['toggleDrawer']),
  },
};
</script>
