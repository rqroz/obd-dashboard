<template>
  <v-row>
    <v-col>
      <profile-chart />
    </v-col>
  </v-row>
</template>

<script>
import ProfileChart from '@/components/obd/graphs/profile/Profile';

export default {
  name: 'DriverProfileView',
  components: {
    ProfileChart,
  },
}
</script>
