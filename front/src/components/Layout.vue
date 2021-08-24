<template>
  <a-layout style="height: 100%">
    <a-layout-sider v-model="collapsed" collapsible :width="220">
      <router-link :to="'/'">
        <div class="logo">
          <img src="../assets/logo.png" />
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
              (item.childrens.length && !item.staffOnly && !item.specOnly) ||
              (item.staffOnly && userInfo.staff) ||
              (item.specOnly && !userInfo.staff)
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
            <router-link
              :to="item.to"
              :class="item.twoLines ? 'menu-two-lines' : ''"
            >
              <a-icon :type="item.icon" />
              <span v-if="!item.twoLines">{{ item.title }}</span>
              <div v-else>{{ item.title }}</div>
              <a-badge
                v-if="item.unread && notifications[item.unread]"
                :number-style="{ backgroundColor: '#52c41a', 'box-shadow': 'unset' }"
                :count="notifications[item.unread]"
              />
            </router-link>
          </a-menu-item>
        </template>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header class="layout-header">
        <div class="user-info">
          <a-icon type="user" class="user-icon"></a-icon>
          <div class="user-info__text">
            <p class="user-info__name">
              {{ userInfo.name }}
            </p>
            <p class="user-info__status" v-if="userInfo.staff">Администратор</p>
            <p class="user-info__status" v-else>Специалист</p>
          </div>
          <a-icon class="icon-button icon-exit" type="import" @click="logout" />
        </div>
      </a-layout-header>
      <a-layout-content style="margin: 15px">
        <div class="content">
          <router-view />
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script>
import { mapGetters, mapActions } from "vuex";
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
          staffOnly: false,
          specOnly: false,
          to: { name: "JobWrapper" },
          childrens: [],
        },
        {
          icon: "rise",
          title: "Развитие навыков",
          key: "2",
          staffOnly: false,
          specOnly: false,
          to: { name: "AllSkills" },
          childrens: [],
        },
        {
          icon: "issues-close",
          title: "Задачи",
          key: "5",
          staffOnly: false,
          specOnly: false,
          to: { name: "Missions" },
          childrens: [],
          unread: "0",
        },
        {
          icon: "solution",
          title: "Интервенционные группы",
          key: "6",
          staffOnly: false,
          specOnly: false,
          to: { name: "TaskGroups" },
          childrens: [],
          twoLines: true,
        },
        {
          icon: "bulb",
          title: "Таланты",
          key: "7",
          staffOnly: false,
          specOnly: false,
          to: { name: "Talents" },
          childrens: [],
        },
        {
          icon: "mail",
          title: "Обращения к руководству",
          key: "8",
          staffOnly: false,
          specOnly: false,
          to: { name: "Appeals" },
          childrens: [],
          twoLines: true,
          childrenRoutes: ["AppealDetails"],
          unread: "1",
        },
        {
          icon: "bell",
          title: "Важная информация",
          key: "9",
          staffOnly: false,
          specOnly: false,
          to: { name: "Announcements" },
          childrens: [],
          twoLines: true,
          unread: "2",
        },
        {
          icon: "setting",
          key: "3",
          title: "Настройки",
          staffOnly: true,
          specOnly: false,
          childrens: [
            {
              key: "3.1",
              title: "Структура навыков",
              to: { name: "Skills" },
            },
            {
              key: "3.2",
              title: "Виды деятельности",
              to: { name: "ActivitiesTypes" },
            },
            {
              key: "3.3",
              title: "Пользователи",
              to: { name: "Specialists" },
            },
            {
              key: "3.4",
              title: "Расписание",
              to: { name: "Schedule" },
            },
            {
              key: "3.5",
              title: "Методы и формы занятий",
              class: "submenu--two-lines",
              to: { name: "Forms" },
            },
            {
              key: "3.6",
              title: "График присутствия специалистов",
              class: "submenu--two-lines",
              to: { name: "AvailableChart" },
            },
          ],
        },
        {
          icon: "user",
          title: "Личный кабинет",
          key: "4",
          staffOnly: false,
          specOnly: true,
          childrens: [
            {
              key: "4.1",
              title: "Профиль",
              to: { name: "SpecialistProfile" },
            },
            {
              key: "4.2",
              title: "Планы занятий",
              to: { name: "JobOptions" },
            },
          ],
        },
      ],
    };
  },
  methods: {
    ...mapActions({
      fetchNotifications: "auth/fetchNotifications",
    }),
    clearStore() {
      this.$store.commit("activities/clear");
      this.$store.commit("forms/clear");
      this.$store.commit("presence/clear");
      this.$store.commit("schedule/clear");
      this.$store.commit("skills/clear");
      this.$store.commit("specialists/clear");
    },
    async logout() {
      this.$router.push("/login/");
      await this.$store.dispatch("auth/logout");
      this.clearStore();
    },
    setSelectedMenuItem(to) {
      if (this.openKeys.length) this.openKeys.splice(0);
      if (this.selectedKeys.length) this.selectedKeys.splice(0);
      let matched = false;
      for (let parent of this.menu) {
        if (parent.childrens.length) {
          for (let children of parent.childrens) {
            if (children.to.name === to.name) {
              this.openKeys.push(parent.key);
              this.selectedKeys.push(children.key);
              matched = true;
              break;
            }
          }
        } else {
          if (parent.to.name === to.name) {
            this.openKeys.push(parent.key);
            this.selectedKeys.push(parent.key);
            matched = true;
          } else if (
            parent.childrenRoutes &&
            parent.childrenRoutes.indexOf(to.name) !== -1
          ) {
            this.openKeys.push(parent.key);
            this.selectedKeys.push(parent.key);
            matched = true;
          }
        }
        if (matched) break;
      }
    },
  },
  computed: {
    ...mapGetters({
      userInfo: "auth/getUserInfo",
      notifications: "auth/getNotifications",
    }),
  },
  beforeRouteUpdate(to, from, next) {
    this.setSelectedMenuItem(to);
    next();
  },
  async created() {
    await this.fetchNotifications();
    this.setSelectedMenuItem(this.$route);
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

.ant-layout-header
  &.layout-header
    background: #fff
    padding: 0
    .user-info
      line-height: 20px
      padding: 10px 15px
      display: flex
      justify-content: flex-end
      .user-icon
        font-size: 20px
        margin-right: 10px
        margin-top: 10px
      .icon-exit
        margin-top: 10px
        svg
          transform: rotate(180deg)
      &__text
        margin-right: 10px
      &__name
        margin-bottom: 0
        min-width: 120px
        text-align: center
      &__status
        text-align: center
        font-size: 0.8rem
        font-weight: bold

.submenu--two-lines
  line-height: 20px
  white-space: normal

.ant-menu
  .ant-menu-item
    .ant-badge
      float: right
      margin-top: 10px

    .menu-two-lines
      display: flex
      flex-direction: row
      .anticon
        align-self: center
      div
        line-height: 16px
        padding: 2px 0 2px 0
        white-space: normal

    .anticon
      font-size: 18px


  &.ant-menu-inline-collapsed
    .ant-badge
      float: unset
      margin-bottom: 10px
    .ant-menu-item
      .menu-two-lines
        .ant-badge
          margin-bottom: 0
          margin-top: 15px
        div
          opacity: 0
          max-width: 0
        .anticon
          align-self: baseline
          margin-top: 2px

      .anticon
        font-size: 18px

  .ant-menu-submenu
    .anticon
      font-size: 18px !important

.content
  .ant-spin-nested-loading
    height: 100%
  .ant-spin-container
    height: 100%

.flex-column
  display: flex
  flex-direction: column
</style>
