<template>
  <div ref="map" v-bind:style="{ width: width, height: height }" />
</template>

<script>
export default {
  name: "HereMap",
  props: {
    center: {
      type: Object,
      default: () => ({ lat: -5.7793, lng: -35.2009}),
    },
    width: {
      type: [String, Number],
      default: '800px',
    },
    height: {
      type: [String, Number],
      default: '600px',
    },
    zoom: {
      type: Number,
      default: 10,
    },
    lines: {
      type: Array,
      default: () => ([]),
    },
  },
  data: () => ({
    map: {},
    platform: new window.H.service.Platform({apikey: process.env.VUE_APP_HERE_API_KEY}),
    behaviour: {},
    polylines: [],
    ui: {},
    colors: [
      '#000000',
      '#bf360c',
      '#5c6bc0',
      '#4a148c',
      '#f44336',
      '#0d47a1',
      '#00796b',
      '#2e7d32',
      '#795548',
      '#546e7a',
    ]
  }),
  methods: {
    addPolyLine(pline, color) {
      if (pline.points.length < 2) { return; }

      /*
      * Will set a max distance threshold between two points when ploting the graph.
      * If the next point surpass this threshold, it will be in the plot.
      * The value of 55.56m/s corresponds to 200km/h and will be the threshold considered since we're getting
      * data from TORQUE at a max rate of 1 request per second,
      */
      const maxDistance = 55.56;
      const lineString = new window.H.geo.LineString();

      let lastPoint = null;
      pline.points.forEach(point => {
        const currPoint = new window.H.geo.Point(point.lat, point.lng);
        if (lastPoint === null || currPoint.distance(lastPoint) < maxDistance) {
          lineString.pushPoint(currPoint);
          lastPoint = currPoint;
        }
      });

      const lineStyle = {
        strokeColor: color || 'black',
        fillColor: 'rgba(255, 255, 255, 0.5)',
        lineWidth: 3,
        lineCap: 'square',
        lineJoin: 'bevel'
      };
      const polyline = new window.H.map.Polyline(
        lineString,
        { style: lineStyle },
      );
      this.map.addObject(polyline);
      this.polylines.push(polyline);
    },
    drawPolyLines() {
      this.map.removeObjects(this.polylines);
      this.polylines = [];
      this.lines.forEach((line, idx) => this.addPolyLine(line, this.colors[idx%this.colors.length]));
    },
  },
  mounted() {
    const defaultLayers = this.platform.createDefaultLayers();
    this.map = new window.H.Map(
      this.$refs.map,
      defaultLayers.vector.normal.map,
      {
          zoom: this.zoom,
          center: { lng: this.center.lng, lat: this.center.lat }
      }
    );
    this.behavior = new window.H.mapevents.Behavior(new window.H.mapevents.MapEvents(this.map));
    this.ui = window.H.ui.UI.createDefault(this.map, defaultLayers);
    this.drawPolyLines();
  },
  watch: {
    lines() {
      this.drawPolyLines();
    },
  },
}
</script>
