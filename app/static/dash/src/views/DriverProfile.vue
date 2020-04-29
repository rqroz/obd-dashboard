<template>
  <v-container justify="center">
    <v-row>
      <v-col>
        <profile-chart />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProfileChart from '@/components/odb/graphs/Profile';

export default {
  name: 'DriverProfileView',
  components: {
    ProfileChart,
  },
}
</script>
