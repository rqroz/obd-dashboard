/*
* Mixin to be used by form components.
*
* Data Attributes:
*   - loading (Boolean): Whether or not the component is in a busy state (performing request);
*   - validateBeforeRequest (Boolean): Whether or not the component should call the validate method before
*                                      performing the request.
*
* Expected Attributes:
*   - endpoint (String): URL of the server to which the form will be submitted;
*   - model (Object): Form data.
*
* Expected Methods:
*   - validate: Validation method to be called before submitting request;
*   - successHandler: Called when the request to <endpoint> was successful;
*   - errorHandler: Called when the request to <endpoint> returned with an error state;
*/

export default {
  data: () => ({
    loading: false,
    validateBeforeRequest: true,
  }),
  methods: {
    submit() {
      if (this.validateBeforeRequest && !this.validate()) { return; }

      this.loading = true;
      this.$requests.post(this.endpoint, this.model)
        .then(response => this.successHandler(response))
        .catch(error => this.errorHandler(error.response))
        .then(() => this.loading = false);
    },
  },
};
