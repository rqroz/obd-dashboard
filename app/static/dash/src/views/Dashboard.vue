<template>
  <v-container justify="center">
    <v-row>
      <v-col>
        <user-card />
      </v-col>
      <v-col>
        <fuel-level-card />
      </v-col>
      <v-col>
        <battery-card />
      </v-col>
      <v-col>
        <speed-average-card />
      </v-col>
      <v-col>
        <engine-rpm-average-card />
      </v-col>
      <v-col>
        <engine-load-average-card />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <user-driver-map />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import BatteryCard from '@/components/odb/engine/battery/BatteryCard';
import EngineLoadAverageCard from '@/components/odb/engine/load/AverageCard';
import EngineRpmAverageCard from '@/components/odb/engine/rpm/AverageCard';
import SpeedAverageCard from '@/components/odb/engine/speed/AverageCard';
import FuelLevelCard from '@/components/odb/fuel/FuelLevelCard';
import UserCard from '@/components/user/Card';
import UserDriverMap from '@/components/user/DriverMap';

export default {
  name: 'Home',
  components: {
    BatteryCard,
    EngineLoadAverageCard,
    EngineRpmAverageCard,
    SpeedAverageCard,
    FuelLevelCard,
    UserCard,
    UserDriverMap,
  },
}
</script>
