<template>
  <v-skeleton-loader
    type="image, actions"
    :loading="loading"
  >
    <v-card>
      <v-card-text>
        place-map-here
      </v-card-text>
    </v-card>
  </v-skeleton-loader>
</template>


<script>
export default {
  data: () => ({
    loading: true,
    zoom: 11,
    polyline: {
      points: [
        [47.334852, -1.509485],
        [47.342596, -1.328731],
        [47.241487, -1.190568],
        [47.234787, -1.358337]
      ],
      color: "green"
    },
  }),
  computed: {
    center() {
      const points = this.polyline.points;
      return points.length ? points[points.length - 1] : null;
    },
  },
};
</script>
