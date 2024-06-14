<template>
  <form @submit.prevent="handleSubmit">
    <!-- Username and email fields -->

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
    <button type="submit">Submit</button>
  </form>
</template>

<script>
import { ref } from 'vue';
import { required, email } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const username = ref('');
    const email = ref('');
    const password = ref(''); // Add password ref
    const rules = { 
      username: { required }, 
      password: { required } // Add password to validation rules
    };
    const v$ = useVuelidate(rules, { username, email, password });

    const handleSubmit = () => {
      v$.value.$touch();
      if (!v$.value.$error) {
        // Submit form data to backend API
        fetch('http://127.0.0.1:8000/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username.value,
            password: password.value, // Include password in form data
          }),
        })
        .then(response => response.json())
        .then(data => {
          console.log(data.error);
          if (data.error != false) {
            console.log('Success:', data);
            localStorage.setItem("authToken", data.token); // Store token in local storage
            const expirationTime = Date.now() + (1 * 60 * 60 * 1000); // Set expiration time to 1 hour
            localStorage.setItem("expirationTime", expirationTime); // Store expiration time in local storage
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

    return { username, email, password, v$, handleSubmit }; // Return password
  },
};
</script>