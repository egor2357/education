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
      path: "/specialist-profile",
      name: "SpecialistProfile",
      component: () => import("@/components/SpecialistProfile/SpecialistProfile"),
      meta: {
        staffOnly: false,
        specOnly: true,
      },
    },
    {
      path: "/job-options",
      name: "JobOptions",
      component: () => import("@/views/JobOptions"),
      meta: {
        staffOnly: false,
        specOnly: true,
      },
    },
  ],
});


router.beforeEach(async (to, from, next) => {
  if (store.getters["auth/getIsAuth"] === null) {
    await store.dispatch("auth/checkUser");
  }

  let isAuth = false;
  isAuth = store.getters["auth/getIsAuth"];

  if (!isAuth) {
    if (to.name == "Login") {
      next();
    } else {
      next({name: "Login"});
    }
  } else {
    let userInfo = store.getters["auth/getUserInfo"];
    if (to.name == null) {
      next({name: "Page404"});
    } else {
      if (!to.meta.staffOnly && !to.meta.specOnly) {
        next();
      } else if (to.meta.staffOnly) {
        if (userInfo.staff) {
          next();
        }
      } else if (to.meta.specOnly) {
        if (!userInfo.staff) {
          next();
        }
      } else {
        next({name: "Page404"});
      }
    }
  }
});

export default router;
