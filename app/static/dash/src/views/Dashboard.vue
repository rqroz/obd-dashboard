<template>
  <v-container justify="center">
    <v-row>
      <v-col md="3">
        <user-card />
      </v-col>
      <v-col>
        <engine-average-load-card />
      </v-col>
      <v-col>
        <fuel-level-card />
      </v-col>
      <v-col>
        <v-skeleton-loader type="list-item-three-line" :boilerplate="true" />
      </v-col>
    </v-row>
    <v-row>
      <v-col md="3">
        <v-skeleton-loader type="list-item-three-line@3" :boilerplate="true" />
      </v-col>
      <v-col>
        <!-- <user-driver-map /> -->
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import EngineAverageLoadCard from '@/components/odb/engine/AverageLoadCard';
import FuelLevelCard from '@/components/odb/fuel/FuelLevelCard';
import UserCard from '@/components/user/Card';
// import UserDriverMap from '@/components/user/DriverMap';

export default {
  name: 'Home',
  components: {
    EngineAverageLoadCard,
    FuelLevelCard,
    UserCard,
    // UserDriverMap,
  },
}
</script>
