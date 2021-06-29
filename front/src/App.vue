<template>
  <a-config-provider :locale="ru_RU">
    <div id="app">
      <Layout v-if="isAuth" />
      <Login v-else-if="isAuth === false" />
    </div>
  </a-config-provider>
</template>

<script>
import Layout from "@/components/Layout";
import Login from "@/views/Login";
import { mapGetters } from "vuex";
import ru_RU from "ant-design-vue/lib/locale-provider/ru_RU";
import moment from "moment";
import "moment/locale/ru";

moment.locale("ru");
export default {
  name: "App",
  components: {
    Layout,
    Login,
  },
  data() {
    return {
      ru_RU,
    };
  },
  created() {
    document.title = "Обучение";
  },
  computed: {
    ...mapGetters({
      isAuth: "auth/getIsAuth",
    }),
  },
};
</script>

<style lang="sass">
html
  min-height: 600px
  min-width: 1300px

#app
  height: 100%
  overflow: hidden
.icon-button
  &:hover
    cursor: pointer
    color: #1890ff
  &.icon-exit
    font-size: 20px
    margin-top: 2px
.ant-menu.ant-menu-dark .ant-menu-item-selected, .ant-menu-submenu-selected
  background: #0060B9 !important

.ant-layout-sider, .ant-menu-dark, .ant-menu-inline, .ant-layout-sider-trigger, .ant-menu-sub
  background: #1890FF !important

.ant-menu
  &.ant-menu-inline
    &.ant-menu-sub
      box-shadow: none !important

.ant-layout
  .ant-layout-content
    flex: 1
</style>
