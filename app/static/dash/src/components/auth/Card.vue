<template>
  <v-card class="mx-auto" :min-width="minWidth">
    <v-card-title>
      {{ login ? cardTitles.login : cardTitles.registration }}
      <v-spacer/>
      <v-btn class="overline" color="primary" text @click="login = !login">
        {{ login ? cardTitles.registration : cardTitles.login }}
      </v-btn>
    </v-card-title>
    <v-card-text class="text--primary">
      <login v-if="login" />
      <registration v-else />
    </v-card-text>
  </v-card>
</template>

<script>
import Login from './Login'
import Registration from './Registration'

export default {
  name: 'Home',
  components: {
    Login,
    Registration,
  },
  props: {
    minWidth: {
      type: [Number, String],
      default: 500,
    },
  },
  data: () => ({
    login: true,
    cardTitles: {
      login: 'LOGIN',
      registration: 'REGISTRATION',
    },
  }),
}
</script>
