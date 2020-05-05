<template>
  <v-container justify="center">
    <v-row class="text-center ">
      <v-col cols="12">
        <div class="ma-5 pt-5">
          <v-icon size="150">mdi-car-connected</v-icon>
        </div>
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-1 font-weight-bold mb-3">
          Welcome to your OBD II Dashboard
        </h1>

        <p class="subheading font-weight-regular">
          For help and collaboration to the project,
          <br>please open a pull request to
          <a
            href="https://github.com/rqroz/obd-dashboard"
            target="_blank"
          >our repository</a>.
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="d-flex justify-center mb-5" cols="12" >
        <auth-card />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import AuthCard from '@/components/auth/Card'

export default {
  name: 'HomeView',
  components: {
    AuthCard,
  },
}
</script>
