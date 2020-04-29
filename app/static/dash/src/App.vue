<template>
  <v-app>
    <v-navigation-drawer
      app
      clipped
      :mini-variant="mini"
      v-model="drawer"
    >
      <v-list dense>
        <v-list-item
          link
          v-for="item in navigationItems"
          :key="item.label"
          :to="item.route"
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.label }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <upload-dialog v-if="$store.getters.user"/>
        <user-edit-dialog v-if="$store.getters.user"/>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left>
      <v-app-bar-nav-icon @click.stop="handleDrawerToggle" />
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer/>
      <auth-logout v-if="user" />
    </v-app-bar>

    <v-content>
      <v-container>
        <base-loader v-if="busy" />
        <router-view v-else />
      </v-container>
    </v-content>

    <base-footer />
  </v-app>
</template>

<script>
import NAVIGATION_ITEMS from '@/resources/navigation/drawer';

import BaseFooter from '@/components/base/Footer';
import BaseLoader from '@/components/base/Loader';
import AuthLogout from '@/components/auth/Logout';
import UploadDialog from '@/components/upload/Dialog';
import UserEditDialog from '@/components/user/EditDialog';


export default {
  components: {
    AuthLogout,
    BaseFooter,
    BaseLoader,
    UploadDialog,
    UserEditDialog,
  },
  data: vm => ({
    mini: !vm.$vuetify.breakpoint.mdAndDown,
    drawer: false,
    title: 'OBD II - Dashboard',
  }),
  computed: {
    user() {
      return this.$store.getters.user;
    },
    busy() {
      return this.$store.getters.loading;
    },
    navigationItems() {
      return this.user ? NAVIGATION_ITEMS.auth : NAVIGATION_ITEMS.unauth;
    },
    small() {
      return this.$vuetify.breakpoint.mdAndDown;
    },
  },
  watch: {
    small(value) {
      if (value) {
        this.mini = false;
      } else {
        this.mini = true;
        this.drawer = true;
      }
    }
  },
  methods: {
    handleDrawerToggle() {
      if (this.small) {
        this.drawer = !this.drawer;
      } else {
        this.mini = !this.mini;
      }
    },
  },
}
</script>
