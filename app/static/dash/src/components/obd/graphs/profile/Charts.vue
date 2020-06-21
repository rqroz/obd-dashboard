<style lang="scss" scoped>
.chart-area {
  margin: 0 auto;

  .chart-container {
    max-width: 500px;

    .chart {
      padding: 30px;
    }
  }
}
</style>

<template>
  <v-card
    class="mx-auto"
    :light="$vuetify.theme.isDark"
    :dark="!$vuetify.theme.isDark"
  >
    <v-card-text>
      <v-slider
        class="ma-5 pt-4"
        thumb-label="always"
        v-model="slider.value"
        :thumb-size="36"
        :max="slider.max"
        :light="$vuetify.theme.isDark"
        :dark="!$vuetify.theme.isDark"
        :disabled="!ready"
      >
        <template v-slot:thumb-label>
          <v-icon :color="$vuetify.theme.isDark ? 'white' : 'black'">mdi-car-hatchback</v-icon>
        </template>
      </v-slider>

      <div class="chart-area d-flex">
        <v-spacer />
        <div class="chart-container mr-5">
          <radar-chart class="chart" :chart-data="radarChart" />
        </div>
        <div class="chart-container ml-5">
          <line-chart class="chart" :chart-data="lineChart" />
        </div>
        <v-spacer />
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import LineChart from './charts/Line';
import RadarChart from './charts/Radar';


export default {
  components: {
    LineChart,
    RadarChart,
  },
  props: {
    session: String,
  },
  data: () => ({
    ready: false,
    values: {
      radar: [],
      line: [],
    },
    slider: {
      value: 0,
      max: 100,
    },
    labelsMap: {
      'engine_map': 'Manifold Pressure',
      'engine_maf': 'Mass Air Flow',
      'engine_rpm': 'RPM',
      'engine_load': 'Engine Load',
      'engine_coolant_temp': 'Engine Coolant Temperature',
      'fuel_lambda': 'Commanded Equivalence Ratio (lambda)',
      'throttle_position': 'Throttle Position',
      'speed': 'Speed',
      'fuel_ratio': 'Fuel Ratio',
    },
  }),
  computed: {
    currentTheme() {
      return this.$vuetify.theme.themes[this.$vuetify.theme.isDark ? 'dark' : 'light'];
    },
    radarChart() {
      return {
        labels: Object.values(this.labelsMap),
        datasets: [{
          label: 'Driving Profile - Visual Representation',
          backgroundColor: this.currentTheme.primary,
          data: this.values.radar.length === 0 ?
            [] :
            Object.keys(this.labelsMap).map(key => this.values.radar[this.slider.value][key]),
        }],
      };
    },
    lineChart() {
      return {
        labels: this.values.line.map(line => this.$options.filters.datetime(line.date)),
        datasets: [{
          label: 'Driving Profile - Metric',
          borderColor: this.currentTheme.info,
          data: this.values.line.map(line => line.value),
          fill: false,
          showLine: true,
          steppedLine: true,
          pointRadius: this.values.line.map((_, idx) => (idx === this.slider.value ? 5 : 0)),
          pointBackgroundColor: 'black',
        }]
      };
    },
  },
  methods: {
    reset() {
      this.values = { radar: [], line: [] };
      this.slider.max = 100;
      this.ready = false;
    },
    fetch() {
      this.$emit('busy');
      this.reset();

      this.$requests.get(`/sessions/${this.session}/profile/`)
        .then(response => {
          this.values = {
            radar: response.data.radar,
            line: response.data.profile,
          };
          this.slider.max = this.values.radar.length - 1;
          this.ready = true;
        })
        .catch(err => {
          console.log(err, err.response);
        })
        .then(() => this.$emit('ready'));
    },
  },
  watch: {
    session() { this.fetch(); },
  },
};
</script>
