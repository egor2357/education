<template>
  <a-config-provider :locale="ru_RU">
    <div id="app">
      <router-view/>
    </div>
  </a-config-provider>
</template>

<script>
import ru_RU from "ant-design-vue/lib/locale-provider/ru_RU";
import moment from "moment";
import "moment/locale/ru";

moment.locale("ru");
export default {
  name: "App",
  data() {
    return {
      ru_RU,
    };
  },
  created() {
    document.title = "Обучение";
  },
};
</script>

<style lang="sass">
html
  min-height: 800px
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
.ant-modal-body
  max-height: 500px
  overflow: auto
  padding-bottom: 0 !important
  .ant-modal-confirm-body-wrapper
    padding-bottom: 24px
.content
  .ant-upload-list-picture
    .ant-upload-list-item-name
      max-width: 300px

.ant-select-tree-title
  white-space: normal

.ant-layout-sider .ant-layout-sider-trigger
  position: absolute

.ant-menu-item:not(:last-child)
  margin-bottom: unset !important
</style>
