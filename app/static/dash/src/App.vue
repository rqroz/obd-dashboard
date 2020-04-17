<template>
  <v-app>
    <v-navigation-drawer app clipped :mini-variant="mini">
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
        <upload-dialog />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left>
      <v-app-bar-nav-icon @click.stop="mini = !mini" />
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


export default {
  components: {
    AuthLogout,
    BaseFooter,
    BaseLoader,
    UploadDialog,
  },
  data: () => ({
    mini: true,
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
  },
}
</script>
