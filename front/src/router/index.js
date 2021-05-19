import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store/index";

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
        breadcrumbs: [{ title: "Навыки" }],
        staffOnly: true,
      },
    },
    {
      path: "/activities-types",
      name: "ActivitiesTypes",
      component: () => import("@/views/ActivitiesTypes"),
      meta: {
        breadcrumbs: [{ title: "Вид деятельности/навыки" }],
        staffOnly: true,
      },
    },
    {
      path: "/404",
      name: "Page404",
      component: () => import("@/views/Page404"),
      meta: {
        breadcrumbs: [{ title: "Страница не найдена" }],
      },
    },
  ],
});

function check404(name) {
  if (name === null) {
    router.push("/404/");
    return false;
  }
  return true;
}

function checkIsAuth(name) {
  if (!store.getters["auth/getIsAuth"] && name !== "Login") {
    router.push("/login/");
    return false;
  } else if (!store.getters["auth/getIsAuth"] && name === "Login") {
    return true;
  } else if (store.getters["auth/getIsAuth"] && name === "Login") {
    router.push({ name: "Flights", query: { type: 1 } });
    return false;
  } else {
    return true;
  }
}

router.beforeEach(async (to, from, next) => {
  if (store.getters["auth/getIsAuth"] === null) {
    await store
      .dispatch("auth/checkUser")
      .then(() => {
        let res1 = check404(to.name);
        if (res1) {
          let res2 = checkIsAuth(to.name);
          if (res2) {
            next();
          }
        }
      })
      .catch(() => {});
  } else {
    let res1 = check404(to.name);
    if (res1) {
      let res2 = checkIsAuth(to.name);
      if (res2) {
        next();
      }
    }
  }
});

export default router;
