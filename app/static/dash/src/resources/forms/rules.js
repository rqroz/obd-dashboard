export default {
  email: value => /.+@.+\..+/.test(value) || 'E-mail must be valid',
  emailPasswordMatch: () => ('The email and password you entered don\'t match'),
  passwordLength: value => value.length >= 8 || 'This field must have at least 8 characters',
  required: value => !!value || 'This field is required.',
  fileSize: value => !value || value.size < 5 * 1000000 || 'File size should be less than 5MB!',
};
