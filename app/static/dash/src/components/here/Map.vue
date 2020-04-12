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
  }),
  methods: {
    addPolyLine(pline) {
      const lineString = new window.H.geo.LineString();
      pline.points.forEach(point => lineString.pushPoint(point));

      const lineStyle = {
        strokeColor: 'black',
        fillColor: 'rgba(255, 255, 255, 0.5)',
        lineWidth: 2,
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
      this.lines.forEach(line => this.addPolyLine(line));
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
