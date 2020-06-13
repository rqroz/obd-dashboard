<template>
  <v-container justify="center">
    <v-row>
      <v-col>
        <line-chart />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import LineChart from '@/components/obd/graphs/Line';

export default {
  name: 'LineChartView',
  components: {
    LineChart,
  },
}
</script>
