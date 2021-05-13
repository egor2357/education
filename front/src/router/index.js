import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes: [
    // {
    //   path: "/",
    //   name: "Main",
    //   component: () => import("@/views/Main"),
    //   meta: {
    //     breadcrumbs: [{ title: "Главная" }],
    //     roles: [1, 2]
    //   },
    // },
  ],
});

export default router;
