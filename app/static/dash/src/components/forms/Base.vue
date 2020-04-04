<template>
  <v-form ref="form" v-model="valid" @keyup.native.enter="submit">
    <v-row>
      <v-col>
        <v-row v-if="error" class="text-center">
          <v-col class=" red--text">
            {{ error.message }}
            <div class="d-block" v-for="(message, idx) in errorMessages" :key="idx">
              {{ message }}
            </div>
          </v-col>
        </v-row>
        <slot></slot>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="d-flex justify-end">
        <v-btn color="primary" :loading="loading" :disabled="!valid" @click="submit">
          <v-icon class="mr-1">{{ btnIcon }}</v-icon>
          {{ btnText }}
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import postMixin from '@/mixins/postMixin';

export default {
  mixins: [postMixin],
  props: {
    btnText: {
      type: String,
      required: true,
    },
    btnIcon: String,
    endpoint: {
      type: String,
      required: true,
    },
    model: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    valid: false,
  }),
  computed: {
    errorMessages() {
      if (!this.error) { return []; }

      const items = this.error.items;
      return Object.keys(items).map(key => (
          key === 'invalid' ?
            items[key] :
            `${this.$options.filters.titleCase(key)}: ${items[key]}`
          )
      );
    },
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },
    successHandler(response) {
      this.$emit('success', response);
    },
    errorHandler(error) {
      this.$emit('error', error);
    }
  },
}
</script>
