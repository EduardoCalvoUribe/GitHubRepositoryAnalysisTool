<!-- Copyright 2024 Radboud University, Modern Software Development Techniques

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. -->

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
