export default {
  email: value => /.+@.+\..+/.test(value) || 'E-mail must be valid',
  emailPasswordMatch: () => ('The email and password you entered don\'t match'),
  passwordLength: value => value.length >= 8 || 'This field must have at least 8 characters',
  required: value => !!value || 'This field is required.',
};
