<template>
  <v-container justify="center">
    <user-header />
    <v-row>
      <v-col>
        <user-driver-map />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import UserHeader from '@/components/user/Header';
import UserDriverMap from '@/components/user/DriverMap';

export default {
  name: 'Home',
  components: {
    UserHeader,
    UserDriverMap,
  },
}
</script>
