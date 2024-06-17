import { required, email } from "@vuelidate/validators";

/**
 * Validation rules object for user input fields.
 * @type {Object}
 * @property {Function} username - Validator function to ensure username is required.
 * @property {Function} email - Validator function to ensure email format is valid.
 */
export default {
  username: required, // Validator function to ensure username is required
  email: email, // Validator function to ensure email format is valid
};
