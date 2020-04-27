<style scoped>
.trip-selector {
  max-width: 350px;
}
</style>

<template>
  <v-skeleton-loader
    type="image, actions"
    :loading="loading"
  >
    <v-card>
      <v-card-title>
        Recent Trips
        <v-spacer/>
        <v-select
          v-if="trips.length"
          v-model="selected"
          :items="items"
          label="Select Trip"
          class="trip-selector"
          prepend-icon="mdi-road-variant"
          outlined dense dark hide-details
        ></v-select>
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
    endpoint: '/gps/locations/',
    trips: [],
    selected: null,
    zoom: 13,
    defaultCenter: { 'lat': -5.7793, 'lng': -35.2009 },
  }),
  computed: {
    items() {
      return this.trips.map(trip => ({ text: this.$options.filters.datetime(new Date(trip.date)), value: trip }));
    },
    mapWidth() {
      return `${3*this.$vuetify.breakpoint.width/4 - 178}px`;
    },
    center() {
      if (!this.selected) { return this.defaultCenter; }
      return this.selected.points.length ?
        this.selected.points[this.selected.points.length - 1] :
        this.defaultCenter;
    },
    polylines() {
      if (!this.selected) { return []; }
      return [this.selected];
    },
  },
  methods: {
    successHandler(response) {
      this.trips = response.data.trips || [];
      if (this.trips.length) {
        this.selected = this.trips[this.trips.length - 1];
      }
    },
    errorHandler(error) {
      console.log(error);
    },
  },
};
</script>
