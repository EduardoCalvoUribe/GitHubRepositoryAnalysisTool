import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/userpage",
      name: "user",
      component: () => import("../views/UserPage.vue"),
    },
    {
      path: "/repoinfo/:url",
      name: "repoinfo",
      component: () => import("../views/RepositoryInfo.vue"),
    },
    {
      path: "/prpage/:url",
      name: "pullrequests",
      component: () => import("../views/PullRequestPage.vue"),
    },
    {
      path: "/commitpage/:url",
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

export default router;
