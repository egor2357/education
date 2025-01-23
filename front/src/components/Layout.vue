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
              (item.specOnly && !userInfo.staff && item.childrens.length)
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
          <a-menu-item
            v-else-if="
              item.childrens.length === 0 && !(userInfo.staff && item.specOnly)
            "
            :key="item.key"
          >
            <router-link
              :to="item.to"
              :class="item.twoLines ? 'menu-two-lines' : ''"
            >
              <a-icon :type="item.icon" />
              <span v-if="!item.twoLines">{{ item.title }}</span>
              <div v-else>{{ item.title }}</div>
              <a-badge
                v-if="
                  item.unread &&
                  notificationKeysRoutes[item.unread] !== $route.name &&
                  notifications[item.unread]
                "
                :number-style="{
                  backgroundColor: '#52c41a',
                  'box-shadow': 'unset',
                }"
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
import { mapGetters, mapActions, mapMutations } from "vuex";
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
          to: { name: "AllSkillsNew" },
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
          icon: "calendar",
          title: "Итоговые отчёты",
          key: "10",
          staffOnly: false,
          specOnly: true,
          to: { name: "Summary" },
          childrens: [],
          twoLines: false,
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
            {
              key: "3.7",
              title: "Упражнения специалистов",
              class: "submenu--two-lines",
              to: { name: "ExercisesForSpecialists" },
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
      notificationKeysRoutes: {
        0: "Missions",
        1: "",
        2: "Announcements",
      },
      wasClosed0: false,
      wasClosed1: false,
      wasClosed2: false,
      reconnectInterval: null,
      timer: null,
      timer2: null,
    };
  },
  methods: {
    ...mapActions({
      fetchNotifications: "notifications/fetchNotifications",
      fetchAnnouncements: "announcements/fetchAnnouncements",
      fetchMissions: "missions/fetchMissions",
      fetchAppeals: "appeals/fetchAppeals",
      fetchAppealInfo: "appeals/fetchAppealInfo",
      fetchMessages: "appeals/fetchMessages",
    }),
    ...mapMutations({
      setSocket: "notifications/setSocket",
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
    openMissionNotification() {
      this.$notification["info"]({
        message: "Задачи",
        description: `Количество новых задач: ${this.notifications[0]}`,
        duration: 0,
        btn:
          this.$route.name !== "Missions"
            ? (h) => {
                return h(
                  "a-button",
                  {
                    props: {
                      type: "primary",
                      size: "small",
                    },
                    on: {
                      click: () => {
                        this.$router.push({ name: "Missions" });
                      },
                    },
                  },
                  "Просмотреть"
                );
              }
            : null,
        key: "0",
        onClose: () => {
          this.wasClosed0 = true;
          close();
        },
      });
    },
    openAppealNotification() {
      this.$notification["info"]({
        message: "Обращения к руководству",
        description: `Количество новых сообщений: ${this.notifications[1]}`,
        duration: 0,
        btn:
          this.$route.name !== "Appeals"
            ? (h) => {
                return h(
                  "a-button",
                  {
                    props: {
                      type: "primary",
                      size: "small",
                    },
                    on: {
                      click: () => {
                        this.$router.push({ name: "Appeals" });
                        this.wasClosed1 = true;
                      },
                    },
                  },
                  "Просмотреть"
                );
              }
            : null,
        key: "1",
        onClose: () => {
          this.wasClosed1 = true;
          close();
        },
      });
    },
    openAnnouncementNotification() {
      this.$notification["info"]({
        message: "Важная информация",
        description: `Количество новых сообщений: ${this.notifications[2]}`,
        duration: 0,
        btn:
          this.$route.name !== "Announcements"
            ? (h) => {
                return h(
                  "a-button",
                  {
                    props: {
                      type: "primary",
                      size: "small",
                    },
                    on: {
                      click: () => {
                        this.$router.push({ name: "Announcements" });
                      },
                    },
                  },
                  "Просмотреть"
                );
              }
            : null,
        key: "2",
        onClose: () => {
          this.wasClosed2 = true;
          close();
        },
      });
    },
    socketConnect() {
      let socket = null;
      if (this.socket === null) {
        socket = new WebSocket(`ws://${document.location.hostname}:8765`);
        if (!socket.onerror) {
          socket.onerror = () => {
            if (!this.timer && !this.timer2) {
              if (!this.reconnectInterval) {
                this.reconnectInterval = 3000;
              }
              const periodicall = () => {
                this.reconnectInterval *= 2;
                if (this.reconnectInterval < 30 * 60 * 1000) {
                  this.socketConnect();
                  this.timer2 = setTimeout(periodicall, this.reconnectInterval);
                } else {
                  clearInterval(this.timer);
                  clearInterval(this.timer2);
                }
              };
              this.timer = periodicall();
            }
          };
        }
        socket.onmessage = async (message) => {
          let data = JSON.parse(message.data);
          if (data.action === "notifications.update.0") {
            this.wasClosed0 = false;
            await this.fetchNotifications();
            if (this.$route.name === "Missions") {
              await this.fetchMissions();
              await this.fetchNotifications();
            }
          }
          if (data.action === "missions.update") {
            if (this.$route.name === "Missions") {
              await this.fetchMissions();
            }
          }

          if (data.action === "notifications.update.1") {
            this.wasClosed1 = false;
            await this.fetchNotifications();
            if (this.$route.name === "Appeals") {
              await this.fetchAppeals();
              await this.fetchNotifications();
            } else if (this.$route.name === "AppealDetails") {
              if (data.appeal_id && data.appeal_id == this.$route.params.id) {
                await this.fetchMessages(data.appeal_id);
                await this.fetchNotifications();
              }
            }
          }
          if (data.action === "appeals.update") {
            if (this.$route.name === "Appeals") {
              await this.fetchAppeals();
            } else if (this.$route.name === "AppealDetails") {
              await this.fetchAppealInfo(this.$route.params.id);
            }
          }

          if (data.action === "notifications.update.2") {
            this.wasClosed2 = false;
            await this.fetchNotifications();
            if (this.$route.name === "Announcements") {
              await this.fetchAnnouncements();
              await this.fetchNotifications();
            }
          }
          if (data.action === "announcements.update") {
            if (this.$route.name === "Announcements") {
              await this.fetchAnnouncements();
            }
          }
        };
        socket.onopen = async () => {
          this.socketReg();
          this.reconnectInterval = null;
          clearInterval(this.timer);
          clearInterval(this.timer2);
        };
        socket.onclose = () => {
          this.setSocket(null);
          this.socketConnect();
        };
        this.setSocket(socket);
      }
    },
    socketReg() {
      let obj = { type: "reg", id: this.userInfo.id };
      this.socket.send(JSON.stringify(obj));
    },
  },
  computed: {
    ...mapGetters({
      userInfo: "auth/getUserInfo",
      notifications: "notifications/getNotifications",
      socket: "notifications/getSocket",
    }),
  },
  async beforeRouteUpdate(to, from, next) {
    this.setSelectedMenuItem(to);
    if (to.name === "Missions") {
      this.$notification.close("0");
      this.wasClosed0 = true;
    }
    if (to.name === "Appeals") {
      this.$notification.close("1");
      this.wasClosed1 = true;
    }
    if (to.name === "Announcements") {
      this.$notification.close("2");
      this.wasClosed2 = true;
    }
    next();
  },
  async created() {
    this.setSelectedMenuItem(this.$route);
    await this.fetchNotifications();
    await this.socketConnect();
  },
  watch: {
    async notifications(values) {
      if (values[0] === 0) {
        setTimeout(() => {
          this.$notification.close("0");
        }, 5000);
      } else if (values[0]) {
        if (!this.wasClosed0) {
          await this.openMissionNotification();
        }
      }

      if (values[1] === 0) {
        setTimeout(() => {
          this.$notification.close("1");
        }, 5000);
      } else if (values[1]) {
        if (!this.wasClosed1) {
          await this.openAppealNotification();
          if (this.$route.name === "Appeals") {
            setTimeout(() => {
              this.$notification.close("1");
            }, 5000);
          }
        }
      }

      if (values[2] === 0) {
        if (this.$route.name === "Announcements") {
          setTimeout(() => {
            this.$notification.close("2");
          }, 5000);
        }
      } else if (values[2]) {
        if (!this.wasClosed2) {
          await this.openAnnouncementNotification();
        }
      }
    },
    userInfo(value) {
      if (value.id) {
        this.socketReg();
      }
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
        max-width: 125px

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
