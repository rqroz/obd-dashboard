<template>
  <v-skeleton-loader
    type="image, actions"
    :loading="loading"
  >
    <v-card>
      <v-card-text class="d-flex justify-center">
        <here-map
          :width="mapWidth"
          :zoom="zoom"
          :center="center"
          :lines="[polyline]"
        />
      </v-card-text>
    </v-card>
  </v-skeleton-loader>
</template>


<script>
import HereMap from '@/components/here/Map';

export default {
  components: {
    HereMap,
  },
  data() {
    return {
      loading: false,
      zoom: 13,
      polyline: {
        points: [
          {lat: 47.334852, lng: -1.509485},
          {lat: 47.342596, lng: -1.328731},
          {lat: 47.241487, lng: -1.190568},
          {lat: 47.234787, lng: -1.358337},
        ],
      },
    };
  },
  computed: {
    mapWidth() {
      return `${3*this.$vuetify.breakpoint.width/4 - 200}px`;
    },
    center() {
      const points = this.polyline.points;
      return points.length ? points[points.length - 1] : null;
    },
  },
};
</script>
