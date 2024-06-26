// Copyright 2024 Radboud University, Modern Software Development Techniques

// Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

// 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

// 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

// 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginForm from "../../LoginForm.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginForm,
    },
    {
      path: "/userpage",
      name: "user",
      component: () => import("../views/UserPage.vue"),
    },
    {
      path: "/repoinfo/:url/:date",
      name: "repoinfo",
      component: () => import("../views/RepositoryInfo.vue"),
    },
    {
      path: "/prpage/:url",
      name: "pullrequests",
      component: () => import("../views/PullRequestPage.vue"),
    },
    // {
    //   path: "/commitpage/:url:id",
    //   name: "commits",
    //   component: () => import("../views/CommitPage.vue"),
    // },
    // {
    //   path: "/commentpage",
    //   name: "comments",
    //   component: () => import("../views/CommentPage.vue"),
    // },
  ],
});

/**
 * Navigation guard to handle authentication and token expiration.
 * @param {Object} to - Target Route Object being navigated to.
 * @param {Object} from - Current Route Object being navigated away from.
 * @param {Function} next - Function to resolve the hook. Must be called to resolve the navigation.
 */
router.beforeEach((to, from, next) => {
  // Set authToken with data from local storage.
  const authToken = localStorage.getItem("authToken");
  const isLoggedIn = !!authToken;

  const expiresAt = localStorage.getItem("expirationTime");

  // Check if logged in.
  if (!isLoggedIn) {
    if (to.path !== "/login") {
      localStorage.removeItem("data");
      // Redirect to login page if not logged in.
      next("/login"); 
    } else {
      next();
    }
  } else if (isLoggedIn && expiresAt > Date.now()) {
    // Token is valid, allow navigation.
    next();
  } else {
    // Token expired, handle expiration:
    localStorage.removeItem("authToken");
    localStorage.removeItem("expirationTime");
    localStorage.removeItem("data");
    next("/login"); 
  }
});

/**
 * Checks for token expiration and removes token and data if expired.
 */
const checkExpiration = () => {
  // Set storedData with authToken locally stored.
  const storedData = localStorage.getItem("authToken");
  // Check if a token is stored locally.
  if (!storedData) {
    return; 
  }

  const expirationTime = localStorage.getItem("expirationTime");
  if (expirationTime < Date.now()) {
    localStorage.removeItem("authToken");
    localStorage.removeItem("data"); // make sure all data is removed
    window.location.href = "http://localhost:5173/login";
  }
};

const intervalId = setInterval(checkExpiration, 1000 * 60); // Check every minute

// Clear the interval on page unload to avoid memory leaks
window.addEventListener("unload", () => clearInterval(intervalId));

export default router;
