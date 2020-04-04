<template>
  <v-app>
    <v-navigation-drawer app clipped :mini-variant="mini">
      <v-list dense>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Control Panel</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left>
      <v-app-bar-nav-icon @click.stop="mini = !mini" />
      <v-toolbar-title>{{ title }}</v-toolbar-title>
    </v-app-bar>

    <v-content>
      <v-container class="fill-height">
        <router-view />
      </v-container>
    </v-content>

    <v-footer app>
      <span>&copy; {{year}} Rodolfo Queiroz</span>
    </v-footer>
  </v-app>
</template>

<script>
  export default {
    data: () => ({
      mini: true,
      title: 'OBD II - Dashboard',
      year: (new Date()).getFullYear(),
    }),
  }
</script>
