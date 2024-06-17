<template>
  <form @submit.prevent="handleSubmit">
    
    <!-- Username and password fields -->
    <div v-if="v$.username.$error">
      <span>Username is required.</span>
    </div>
    <input v-model="username" type="username" placeholder="username" required />
    <br>
    <div v-if="v$.password.$error">
      <span>Password is required.</span>
    </div>
    <input v-model="password" type="password" placeholder="password" required />
    <br>
    <!-- Submit button -->
    <button type="submit">Submit</button>
  </form>
</template>

<script>
import { ref } from 'vue';
import { required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useRouter } from 'vue-router';

export default {
  setup() {
    /**
     * @constant {Router} router - The router instance.
     */
    const router = useRouter();

    /**
     * @constant {Ref} username - A reactive reference to hold the username.
     */
    const username = ref('');

    /**
     * @constant {Ref} password - A reactive reference to hold the password.
     */
    const password = ref('');

    /**
     * Validation rules for the form fields.
     * @constant {Object} rules
     */
    const rules = {
      username: { required },
      password: { required }
    };

    /**
     * Validation instance.
     * @constant {Object} v$
     */
    const v$ = useVuelidate(rules, { username, password });

    /**
     * Handles the form submission.
     * @function handleSubmit
     */
    const handleSubmit = () => {
      v$.value.$touch();
      // Check for error.
      if (!v$.value.$error) {
        // Submit form data to backend API.
        fetch('http://127.0.0.1:8000/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username.value,
            password: password.value,
          }),
        })
          .then(response => response.json())
          .then(data => {
            if (data.error != false) {
              // Store token in local storage.
              localStorage.setItem("authToken", data.token);
              
              // Set expiration time to 1 hour and store it in local storage.
              const expirationTime = Date.now() + (1 * 60 * 60 * 1000);
              localStorage.setItem("expirationTime", expirationTime);
              
              // Redirect to the home page.
              router.push('/');
            } else {
              console.log('Invalid credentials');
            }
          })
          .catch(error => {
            console.error('Error:', error);
          });
      }
    };

    return { username, password, v$, handleSubmit };
  },
};
</script>
