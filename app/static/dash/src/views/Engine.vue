<template>
  <v-container justify="center">
    <v-row>
      <v-col>
        Engine
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <fuel-dashboard />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import FuelDashboard from '@/components/odb/fuel/FuelDashboard';

export default {
  name: 'Home',
  components: {
    FuelDashboard,
  },
}
</script>
