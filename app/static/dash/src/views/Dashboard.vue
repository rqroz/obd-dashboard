<template>
  <v-container justify="center">
    <v-row>
      <v-col md="3">
        <user-card />
      </v-col>
      <v-col>
        <engine-load-average-card />
      </v-col>
      <v-col>
        <v-skeleton-loader type="list-item-three-line" :boilerplate="true" />
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
        <user-driver-map />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import EngineLoadAverageCard from '@/components/engine/load/AverageCard';
import UserCard from '@/components/user/Card';
import UserDriverMap from '@/components/user/DriverMap';

export default {
  name: 'Home',
  components: {
    EngineLoadAverageCard,
    UserCard,
    UserDriverMap,
  },
}
</script>
