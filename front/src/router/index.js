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
        staffOnly: false,
        specOnly: false,
      },
    },
    {
      path: "/skills",
      name: "Skills",
      // component: () => import("@/components/TableSkill"),
      component: () => import("@/views/Admin/SkillsStructure"),
      meta: {
        staffOnly: true,
        specOnly: false,
      },
    },
    {
      path: "/activities-types",
      name: "ActivitiesTypes",
      component: () => import("@/views/Admin/ActivitiesTypes"),
      meta: {
        staffOnly: true,
        specOnly: false,
      },
    },
    {
      path: "/specialists",
      name: "Specialists",
      component: () => import("@/views/Admin/Specialists"),
      meta: {
        staffOnly: true,
        specOnly: false,
      },
    },
    {
      path: "/schedule",
      name: "Schedule",
      component: () => import("@/views/Admin/Schedule"),
      meta: {
        staffOnly: true,
        specOnly: false,
      },
    },
    {
      path: "/forms",
      name: "Forms",
      component: () => import("@/views/Admin/Forms"),
      meta: {
        staffOnly: true,
        specOnly: false,
      },
    },
    {
      path: "/chart-available",
      name: "AvailableChart",
      component: () => import("@/views/Admin/AvailableChart"),
      meta: {
        staffOnly: true,
        specOnly: false,
      },
    },
    {
      path: "/developing",
      name: "Developing",
      component: () => import("@/views/InDeveloping"),
      meta: {
        staffOnly: false,
        specOnly: false,
      },
    },
    {
      path: "/",
      name: "Developing",
      component: () => import("@/views/InDeveloping"),
      meta: {
        staffOnly: false,
        specOnly: false,
      },
    },
    {
      path: "/404",
      name: "Page404",
      component: () => import("@/views/Page404"),
      meta: {
        staffOnly: false,
        specOnly: false,
      },
    },
    {
      path: "/jobs",
      component: () => import("@/views/Jobs"),
      meta: {
        staffOnly: false,
        specOnly: false,
      },
      children: [
        {
          path: "/",
          name: "JobSchedule",
          component: () => import("@/components/JobSchedule/JobSchedule"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
        },
        {
          path: ":id",
          name: "JobDetails",
          component: () => import("@/components/JobDetails"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
        },
      ]
    },
    {
      path: "/skill-development",
      component: () => import("@/views/SkillDevelopment"),
      meta: {
        staffOnly: false,
        specOnly: false,
      },
      children: [
        {
          path: "/",
          name: "AllSkills",
          component: () => import("@/components/SkillDevelopment/AllSkills"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
        },
        {
          path: ":id",
          name: "SkillDetails",
          component: () => import("@/components/SkillDevelopment/SkillDetails"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
        },
      ]
    },
    {
      path: "/specialist-profile ",
      name: "SpecialistProfile",
      component: () => import("@/components/SpecialistProfile/SpecialistProfile"),
      meta: {
        staffOnly: false,
        specOnly: true,
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
