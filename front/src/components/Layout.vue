<template>
  <a-layout style="height: 100%">
    <a-layout-sider v-model="collapsed" collapsible :width="220">
      <router-link :to="'/'">
        <div class="logo">
          <img src="../assets/logo.png">
          <p>Обучение</p>
        </div>
      </router-link>
      <a-menu
        theme="dark"
        :defaultSelectedKeys="selectedKeys"
        :defaultOpenKeys="openKeys"
        mode="inline"
      >
        <template v-for="item in menu">
          <a-sub-menu
            :key="item.key"
            v-if="
              (item.childrens.length > 0 && !item.staffOnly) ||
              (item.staffOnly && userInfo.staff)
            "
          >
            <span slot="title">
              <a-icon :type="item.icon" />
              <span>{{ item.title }}</span>
            </span>
            <a-menu-item :key="child.key" v-for="child in item.childrens">
              <router-link :to="child.to" :class="child.class">
                {{ child.title }}</router-link
              >
            </a-menu-item>
          </a-sub-menu>
          <a-menu-item :key="item.key" v-else-if="item.childrens.length === 0">
            <router-link :to="item.to">
              <a-icon :type="item.icon" />
              <span>{{ item.title }}</span></router-link
            >
          </a-menu-item>
        </template>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0">
        <div class="user-info">
          <a-icon
            type="user"
            style="font-size: 20px; margin-right: 10px; margin-top: 10px"
          ></a-icon>
          <div style="margin-right: 10px">
            <p style="margin-bottom: 0; min-width: 120px; text-align: center">
              {{ userInfo.name }}
            </p>
            <p
              style="text-align: center; font-size: 0.8rem; font-weight: bold"
              v-if="userInfo.staff"
            >
              Администратор
            </p>
          </div>
          <a-icon
            class="icon-button icon-exit"
            style="margin-top: 10px"
            type="import"
            @click="logout"
          />
        </div>
      </a-layout-header>
      <a-layout-content style="margin: 15px">
        <div class="content">
          <router-view v-if="$route.name !== 'Login'" />
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      collapsed: false,
      openKeys: [],
      selectedKeys: [],
      menu: [
        {
          icon: "schedule",
          title: "Занятия",
          key: "1",
          to: { name: "JobSchedule" },
          childrens: [],
        },
        {
          icon: "rise",
          title: "Развитие навыков",
          key: "2",
          to: { name: "AllSkills" },
          childrens: [],
        },
        {
          icon: "tool",
          key: "3",
          title: "Настройки",
          staffOnly: true,
          childrens: [
            {
              key: "2.1",
              title: "Структура навыков",
              to: { name: "Skills" },
            },
            {
              key: "2.2",
              title: "Виды деятельности",
              to: { name: "ActivitiesTypes" },
            },
            {
              key: "2.3",
              title: "Пользователи",
              to: { name: "Specialists" },
            },
            {
              key: "2.4",
              title: "Расписание",
              to: { name: "Schedule" },
            },
            {
              key: "2.5",
              title: "Формы и способы занятий",
              class: "submenu--two-lines",
              to: { name: "Forms" },
            },
            {
              key: "2.6",
              title: "График присутствия специалистов",
              class: "submenu--two-lines",
              to: { name: "AvailableChart" },
            },
          ],
        },
      ],
      breadcrumbs: [],
    };
  },
  methods: {
    async logout() {
      await this.$store.dispatch("auth/logout");
      this.$router.push("/login/");
    },
  },
  computed: {
    ...mapGetters({
      userInfo: "auth/getUserInfo",
    }),
  },
  watch: {
    $route(value) {
      if (this.openKeys.length > 0) this.openKeys = [];
      if (this.selectedKeys.length > 0) this.selectedKeys = [];
      for (let parent of this.menu) {
        for (let children of parent.childrens) {
          if (
            children.to.query &&
            children.to.query.type === value.query.type
          ) {
            this.openKeys.push(parent.key);
            this.selectedKeys.push(children.key);
            break;
          } else if (!children.to.query && children.to.name === value.name) {
            this.openKeys.push(parent.key);
            this.selectedKeys.push(children.key);
            break;
          }
        }
      }
      this.breadcrumbs = value.meta.breadcrumbs;
    },
  },
};
</script>

<style lang="sass">
.logo
  max-height: 75px
  margin: 10px
  color: rgba(255, 255, 255, 1)
  text-align: center
  font-size: 1.1rem
  font-weight: bold

  img
    max-width: 48px

.content
  background: #fff
  height: 100%
  padding: 15px
  overflow: hidden

.ant-layout-sider-collapsed
  .logo
    font-size: 0.9rem
    margin: 16px 5px

    img
      max-width: 32px

.user-info
  line-height: 20px
  padding: 10px 15px
  display: flex
  justify-content: flex-end
.submenu--two-lines
  line-height: 20px
  white-space: normal

.content
  .ant-spin-nested-loading
    height: 100%
  .ant-spin-container
    height: 100%
</style>
