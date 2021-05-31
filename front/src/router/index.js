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
      component: () => import("@/views/Admin/ActivitiesTypes"),
      meta: {
        breadcrumbs: [{ title: "Вид деятельности / навыки" }],
        staffOnly: true,
      },
    },
    {
      path: "/specialists",
      name: "Specialists",
      component: () => import("@/views/Admin/Specialists"),
      meta: {
        breadcrumbs: [{ title: "Специалисты" }],
        staffOnly: true,
      },
    },
    {
      path: "/schedule",
      name: "Schedule",
      component: () => import("@/views/Admin/Schedule"),
      meta: {
        breadcrumbs: [{ title: "Шаблон расписания занятий" }],
        staffOnly: true,
      },
    },
    {
      path: "/forms",
      name: "Forms",
      component: () => import("@/views/Admin/Forms"),
      meta: {
        breadcrumbs: [{ title: "Формы и способы проведения занятий" }],
        staffOnly: true,
      },
    },
    {
      path: "/chart-available",
      name: "AvailableChart",
      component: () => import("@/views/Admin/AvailableChart"),
      meta: {
        breadcrumbs: [{ title: "График присутствия специалистов" }],
        staffOnly: true,
      },
    },
    {
      path: "/developing",
      name: "Developing",
      component: () => import("@/views/InDeveloping"),
      meta: {
        breadcrumbs: [{ title: "Раздел находится в разработке" }],
      },
    },
    {
      path: "/",
      name: "Developing",
      component: () => import("@/views/InDeveloping"),
      meta: {
        breadcrumbs: [{ title: "Раздел находится в разработке" }],
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
    {
      path: "/job-schedule",
      name: "JobSchedule",
      component: () => import("@/views/JobSchedule"),
      meta: {
        breadcrumbs: [{ title: "Расписание занятий" }],
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
    router.push("/schedule");
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
