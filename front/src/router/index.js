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
      path: "/",
      component: () => import("@/components/Layout"),
      meta: {
        staffOnly: false,
        specOnly: false,
      },
      children: [
        {
          path: "",
          redirect: "jobs",
        },
        {
          path: "skills",
          name: "Skills",
          // component: () => import("@/components/TableSkill"),
          component: () => import("@/views/Admin/SkillsStructure"),
          meta: {
            staffOnly: true,
            specOnly: false,
          },
        },
        {
          path: "activities-types",
          name: "ActivitiesTypes",
          component: () => import("@/views/Admin/ActivitiesTypes"),
          meta: {
            staffOnly: true,
            specOnly: false,
          },
        },
        {
          path: "specialists",
          name: "Specialists",
          component: () => import("@/views/Admin/Specialists"),
          meta: {
            staffOnly: true,
            specOnly: false,
          },
        },
        {
          path: "exercises-for-specialists",
          name: "ExercisesForSpecialists",
          component: () => import("@/views/Admin/ExercisesForSpecialists"),
          meta: {
            staffOnly: true,
            specOnly: false,
          },
        },
        {
          path: "schedule",
          name: "Schedule",
          component: () => import("@/views/Admin/Schedule"),
          meta: {
            staffOnly: true,
            specOnly: false,
          },
        },
        {
          path: "forms",
          name: "Forms",
          component: () => import("@/views/Admin/Forms"),
          meta: {
            staffOnly: true,
            specOnly: false,
          },
        },
        {
          path: "chart-available",
          name: "AvailableChart",
          component: () => import("@/views/Admin/AvailableChart"),
          meta: {
            staffOnly: true,
            specOnly: false,
          },
        },
        {
          path: "jobs",
          component: () => import("@/views/Jobs"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
          children: [
            {
              path: "/",
              name: "JobWrapper",
              component: () => import("@/components/JobSchedule/JobWrapper"),
              meta: {
                staffOnly: false,
                specOnly: false,
              },
            },
            {
              path: ":id",
              name: "JobDetails",
              component: () =>
                import("@/components/JobSchedule/JobDetailWrapper"),
              meta: {
                staffOnly: false,
                specOnly: false,
              },
            },
          ],
        },
        {
          path: "skill-development",
          component: () => import("@/views/SkillDevelopment"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
          children: [
            {
              path: "/",
              name: "AllSkillsNew",
              component: () =>
                import("@/components/SkillDevelopment/AllSkillsNew"),
              meta: {
                staffOnly: false,
                specOnly: false,
              },
            },
            {
              path: ":id",
              name: "ExerciseDetails",
              component: () =>
                import("@/components/SkillDevelopment/ExerciseDetails"),
              meta: {
                staffOnly: false,
                specOnly: false,
              },
            },
          ],
        },
        {
          path: "specialist-profile",
          name: "SpecialistProfile",
          component: () =>
            import("@/components/SpecialistProfile/SpecialistProfile"),
          meta: {
            staffOnly: false,
            specOnly: true,
          },
        },
        {
          path: "job-options",
          name: "JobOptions",
          component: () => import("@/views/JobOptions"),
          meta: {
            staffOnly: false,
            specOnly: true,
          },
        },
        {
          path: "missions",
          name: "Missions",
          component: () => import("@/views/Missions"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
        },
        {
          path: "task-groups",
          name: "TaskGroups",
          component: () => import("@/views/TaskGroups"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
        },
        {
          path: "talents",
          name: "Talents",
          component: () => import("@/views/Talents"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
        },
        {
          path: "appeals",
          component: () => import("@/views/AppealsWrapper"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
          children: [
            {
              path: "/",
              name: "Appeals",
              component: () => import("@/components/Appeals/Appeals"),
              meta: {
                staffOnly: false,
                specOnly: false,
              },
            },
            {
              path: ":id",
              name: "AppealDetails",
              component: () => import("@/components/Appeals/AppealDetails"),
              meta: {
                staffOnly: false,
                specOnly: false,
              },
            },
          ],
        },
        {
          path: "announcements",
          name: "Announcements",
          component: () => import("@/views/Announcements"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
        },
        {
          path: "summary",
          name: "Summary",
          component: () => import("@/views/Admin/AvailableChart"),
          meta: {
            staffOnly: false,
            specOnly: true,
          },
        },
        {
          path: "*",
          name: "Page404",
          component: () => import("@/views/Page404"),
          meta: {
            staffOnly: false,
            specOnly: false,
          },
        },
      ],
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
      next({ name: "Login" });
    }
  } else {
    let userInfo = store.getters["auth/getUserInfo"];
    if (to.name != null) {
      if (!to.meta.staffOnly && !to.meta.specOnly) {
        next();
      } else if (to.meta.staffOnly) {
        if (userInfo.staff) {
          next();
        } else {
          next({ name: "Page404" });
        }
      } else if (to.meta.specOnly) {
        if (!userInfo.staff) {
          next();
        } else {
          next({ name: "Page404" });
        }
      } else {
        next({ name: "Page404" });
      }
    } else {
      next({ name: "Page404" });
    }
  }
});

export default router;
