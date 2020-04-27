<template>
  <v-container justify="center">
    <v-row>
      <v-col>
        <fuel-level-card />
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
import FuelLevelCard from '@/components/odb/fuel/FuelLevelCard';

export default {
  name: 'Home',
  components: {
    FuelDashboard,
    FuelLevelCard,
  },
}
</script>
