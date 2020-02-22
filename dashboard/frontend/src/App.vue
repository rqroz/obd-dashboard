<template>
  <v-app>
    <app-bar />

    <drawer />

    <content-view />

    <v-snackbar
      v-model="$root.snackbar.display"
      :timeout="$root.snackbar.timeout"
      :multi-line="$root.snackbar.multiline"
      :color="$root.snackbar.color"
    >
      <div v-html="$root.snackbar.html"></div>
    </v-snackbar>

    <BlockUI v-if="$root.blocker.display" :message="$root.blocker.message">
      <circle-loader color="#42A5F5" />
    </BlockUI>
  </v-app>
</template>

<script>
import AppBar from '@/components/base/AppBar';
import Drawer from '@/components/base/Drawer';
import ContentView from '@/components/base/ContentView';
import { CircleLoader } from '@saeris/vue-spinners';


export default {
  name: 'App',
  components: {
    AppBar,
    Drawer,
    ContentView,
    CircleLoader,
  },
};
</script>
