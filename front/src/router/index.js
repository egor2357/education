import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/login",
      name: "Login",
      component: () => import("@/views/Login"),
      meta: {
        breadcrumbs: [],
      },
    },
    {
      path: "/skills",
      name: "Skills",
      component: () => import("@/components/TableSkill"),
      meta: {
        breadcrumbs: [
          { title: "Навыки" }
        ],
        staffOnly: true
      },
    },
  ],
});

export default router;
