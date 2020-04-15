/*
* Mixin for fetching data through an axios request..
*
* Data Attributes:
*   - loading (Boolean): Whether or not the component is in a busy state (performing request);
*   - error: Map of errors got from request.
*
* Expected Attributes:
*   - endpoint (String): URL of the server to which the form will be submitted;
*
* Expected Methods:
*   - successHandler: Called when the request to <endpoint> was successful;
*   - errorHandler: Called when the request to <endpoint> returned with an error state;
*/

export default {
  data: () => ({
    loading: false,
    error: null,
  }),
  methods: {
    fetch() {
      this.loading = true;
      this.error = null;
      this.$requests.get(this.endpoint)
        .then(response => {
          this.successHandler(response);
          this.loading = false;
        })
        .catch(error => {
          const response = error.response;
          this.error = { message: response.data.message, items: response.data.errors};
          this.errorHandler(response);
          this.loading = false;
        })
    },
  },
  created() {
    this.fetch();
  },
};
