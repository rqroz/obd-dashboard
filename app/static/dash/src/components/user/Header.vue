<template>
  <v-row>
    <v-col>
      <user-card />
    </v-col>
    <v-col>
      <simple-card
        :icon="fuel.icon"
        :subtitle="fuel.subtitle"
        :message="fuel.messages"
        :icon-color="fuel.iconColor"
        :title="fuel.level ? `${fuel.level.toFixed(2)} %` : '-'"
      />
    </v-col>
    <v-col>
      <simple-card
        :icon="battery.icon"
        :subtitle="battery.subtitle"
        :message="battery.messages"
        :icon-color="battery.iconColor"
        :title="battery.value ? `${battery.value.toFixed(2)} V` : '-'"
      />
    </v-col>
    <v-col>
      <simple-card
        :icon="speed.icon"
        :subtitle="speed.subtitle"
        :title="typeof speed.value === 'number' ? `${speed.value.toFixed(2)} Km/h` : '-'"
      />
    </v-col>
    <v-col>
      <simple-card
        :icon="rpm.icon"
        :subtitle="rpm.subtitle"
        :title="rpm.value ? rpm.value.toFixed(0) : '-'"
      />
    </v-col>
    <v-col>
      <simple-card
        :icon="load.icon"
        :subtitle="load.subtitle"
        :title="load.value ? `${load.average.toFixed(2)} %` : '-'"
      />
    </v-col>
  </v-row>
</template>

<script>
import UserCard from '@/components/user/Card';
import SimpleCard from '@/components/utils/cards/SimpleCard';

export default {
  name: 'UserHeader',
  components: {
    SimpleCard,
    UserCard,
  },
  data: () => ({
    thresholds: {
      battery: null,
    },
    fuel: {
      icon: 'mdi-gas-station',
      iconColor: null,
      message: null,
      subtitle: 'Fuel Level',
      value: null,
    },
    battery: {
      icon: 'mdi-car-battery',
      iconColor: null,
      message: null,
      subtitle: 'Battery Status',
      value: null,
    },
    speed: {
      icon: 'mdi-speedometer',
      subtitle: 'Historical Speed Average',
      value: null,
    },
    rpm: {
      icon: 'mdi-gauge',
      subtitle: 'Historical RPM Average',
      value: null,
    },
    load: {
      icon: 'mdi-engine',
      subtitle: 'Historical Engine Load Average',
      value: null,
    },
  }),
  computed: {
    batteryLevel() {
      return this.battery.value;
    },
    fuelLevel() {
      return this.fuel.value;
    },
  },
  watch: {
    batteryLevel(value) {
      const isInDanger = value < this.thresholds.battery;
      this.battery.message = isInDanger ?
      'Your battery\'s voltage is under the minimum threshold. Please change the battery ASAP.' :
      'Your car battery level is within the ideal range.';
      this.battery.iconColor = isInDanger ? 'error' : 'primary';
    },
    fuelLevel(value) {
      if (value) {
        if (value < 25) {
          this.fuel.message = 'You are starting to run out of gas...';
          this.fuel.iconColor = 'warning';
        } else if (value < 10) {
          this.fuel.message = 'Time to refuel!';
          this.fuel.iconColor = 'error';
        } else {
          this.fuel.message = 'You don\'t need to worry about gas for now.';
          this.fuel.iconColor = 'primary';
        }
      }
    },
  },
};
</script>
