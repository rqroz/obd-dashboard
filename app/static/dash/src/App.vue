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
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left>
      <v-app-bar-nav-icon @click.stop="mini = !mini" />
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer/>
      <v-dialog v-if="user" v-model="logoutDialog" persistent width="500">
          <template v-slot:activator="{ on }">
            <v-btn text v-on="on">
              <v-icon>mdi-logout</v-icon>
              Logout
            </v-btn>
          </template>

          <v-card>
            <v-card-title primary-title>
              Are you sure you want to log out?
            </v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="logoutDialog = false">
                Go Back
              </v-btn>
              <v-btn color="error" text @click="logout">
                Yes, log me out
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-app-bar>

    <v-content>
      <v-container>
        <router-view />
      </v-container>
    </v-content>

    <v-footer app class="overline" style="min-height: 36px !important;">
      &copy; {{year}} Rodolfo Queiroz
    </v-footer>
  </v-app>
</template>

<script>
import { CLEAR_USER } from '@/store/modules/user/actions';
import NAVIGATION_ITEMS from '@/resources/navigation/drawer';

export default {
  data: () => ({
    mini: true,
    logoutDialog: false,
    title: 'OBD II - Dashboard',
    year: (new Date()).getFullYear(),
  }),
  computed: {
    user() {
      return this.$store.getters.user;
    },
    navigationItems() {
      return this.user ? NAVIGATION_ITEMS.auth : NAVIGATION_ITEMS.unauth;
    },
  },
  methods: {
    logout() {
      this.$requests.post('/logout/')
        .then(() => {
          this.$store.dispatch(CLEAR_USER);
          this.logoutDialog = false
        })
        .catch((error) => console.log(error.response));
    },
  },
}
</script>
