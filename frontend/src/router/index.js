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
    {
      path: "/commitpage/:url:id",
      name: "commits",
      component: () => import("../views/CommitPage.vue"),
    },
    {
      path: "/commentpage",
      name: "comments",
      component: () => import("../views/CommentPage.vue"),
    },
  ],
});

router.beforeEach((to, from, next) => {
  const authToken = localStorage.getItem("authToken");
  const isLoggedIn = !!authToken;

  const expiresAt = localStorage.getItem("expirationTime");

  if (!isLoggedIn) {
    if (to.path !== "/login") {
      localStorage.removeItem("data");
      next("/login"); // Redirect to login page if not logged in
    } else {
      next();
    }
  } else if (isLoggedIn && expiresAt > Date.now()) {
    // Token is valid, allow navigation
    next();
  } else {
    // Token expired, handle expiration:
    localStorage.removeItem("authToken");
    localStorage.removeItem("expirationTime");
    localStorage.removeItem("data");
    next("/login"); // Or redirect to a refresh token endpoint based on your logic
  }
});

const checkExpiration = () => {
  const storedData = localStorage.getItem("authToken");
  if (!storedData) {
    return; // No token stored
  }

  const expirationTime = localStorage.getItem("expirationTime");
  if (!storedData || expirationTime < Date.now()) {
    localStorage.removeItem("authToken");
    localStorage.removeItem("data"); // make sure all data is removed
    window.location.href = "http://localhost:5173/login";
  }
};

const intervalId = setInterval(checkExpiration, 1000 * 60); // Check every minute

// Clear the interval on page unload to avoid memory leaks
window.addEventListener("unload", () => clearInterval(intervalId));

export default router;
