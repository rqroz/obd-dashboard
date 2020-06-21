<template>
  <v-card elevation="3">
    <v-card-title class="justify-center">
      Driver Profile
    </v-card-title>
    <v-card-text style="position: relative;">
      <v-overlay
        :absolute="true"
        :value="loading"
      />
      <v-select
        dense
        outlined
        label="Select a session to see your unique blueprints"
        v-model="selected"
        :items="sessions"
        :loading="loading"
        :disabled="loading"
      />
      <charts
        ref="charts"
        :session="selected"
        @busy="loading = true"
        @ready="loading = false"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import Charts from './Charts';

export default {
  components: {
    Charts,
  },
  data: () => ({
    loading: false,
    sessions: [],
    selected: null,
  }),
  methods: {
    fetch() {
      this.loading = true;
      this.selected = null;
      this.sessions = [];

      this.$requests.get('/sessions/')
        .then(response => {
          this.sessions = response.data.list.map(session => ({
            value: session.id,
            text: this.$options.filters.datetime(session.date),
          }));
        })
        .catch(err => {
          console.log(err, err.response);
        })
        .then(() => { this.loading = false; });
    },
  },
  mounted() {
    this.fetch();
  },
};
</script>
