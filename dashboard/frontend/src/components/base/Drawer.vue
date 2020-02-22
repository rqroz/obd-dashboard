<template>
  <v-navigation-drawer
    v-model="opened"
    :clipped="$vuetify.breakpoint.lgAndUp"
    app dark
  >
    <v-list dense>
      <template v-for="item in items">
        <v-list-item
          :key="item.text"
          @click="navigate(item)"
         >
        <v-list-item-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              {{ item.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { mapMutations, mapState } from 'vuex';


export default {
  data: () => ({
    items: [
      {
        icon: 'mdi-account-search',
        text: 'Users',
        route: { name: 'InvestorListPage' },
      },
    ],
  }),
  computed: {
    ...mapState('app', ['image', 'color']),
    opened: {
      get () {
        return this.$store.state.app.drawer;
      },
      set (val) {
        this.setDrawer(val);
      },
    },
  },
  methods: {
    ...mapMutations('app', ['setDrawer', 'toggleDrawer']),
    navigate(item) {
      this.$router.push(item.route).catch(() => {});
    },
  }
};
</script>
