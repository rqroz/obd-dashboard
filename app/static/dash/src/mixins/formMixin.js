/*
* Mixin to be used by form components.
*
* Expected $refs:
*   - form: Instance of the form component;
*
* Expected Attributes:
*   - endpoint (str): URL of the server to which the form will be submitted;
*   - form (Object): Form data.
*
* Expected Methods:
*   - successHandler: Called when the request to <endpoint> was successful;
*   - errorHandler: Called when the request to <endpoint> returned with an error state;
*/

export default {
  methods: {
    submit() {
      if (!this.$refs.form.validate()) { return; }

      this.$requests.post(this.endpoint, this.model)
        .then(response => this.successHandler(response))
        .catch(error => this.errorHandler(error.response));
    },
  },
};
