<template>
  <v-skeleton-loader
    type="image, actions"
    :loading="loading"
  >
    <v-card>
      <v-card-title>
        Recent Trips
      </v-card-title>
      <v-card-text class="d-flex justify-center">
        <here-map
          :width="mapWidth"
          :zoom="zoom"
          :center="center"
          :lines="polylines"
        />
      </v-card-text>
    </v-card>
  </v-skeleton-loader>
</template>


<script>
import fetchMixin from '@/mixins/fetchMixin';
import HereMap from '@/components/here/Map';

export default {
  mixins: [fetchMixin],
  components: {
    HereMap,
  },
  data: () => ({
    endpoint: '/locations/',
    polylines: [],
    zoom: 13,
    defaultCenter: { 'lat': -5.7793, 'lng': -35.2009 },
  }),
  computed: {
    mapWidth() {
      return `${3*this.$vuetify.breakpoint.width/4 - 178}px`;
    },
    center() {
      if (!this.polylines.length) { return this.defaultCenter; }
      const lastLine = this.polylines[this.polylines.length - 1];
      return lastLine.points.length ? lastLine.points[lastLine.points.length - 1] : this.defaultCenter;
    },
  },
  methods: {
    successHandler(response) {
      this.polylines = response.data.locations;
    },
  },
};
</script>
