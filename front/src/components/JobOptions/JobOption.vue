<template>
  <div hoverable class="job-option"
    @click="$emit('optionSelect', option)">
    <div class="job-option-header">
      <div class="job-option-header-topic">
        {{ option.topic }}
      </div>
      <slot></slot>
    </div>
    <div class="job-option-body">
      <div class="job-option-skills">
        <div class="job-option-skill"
          v-for="skill in option.skills" :key="skill.id">
            {{ skill.area_number }}.{{ skill.direction_number }}.{{ skill.number }} {{ skill.name }}
          </div>
      </div>
      <div class="job-option-form" v-if="option.method">
        {{ option.method.form_name }}
        <a-divider type="vertical" />
        {{ option.method.name }}
      </div>
      <div class="job-option-comment">{{ option.comment }}</div>
      <div class="job-option-files" v-if="files.length">
        <a-divider orientation="left">
          Методические материалы
        </a-divider>
        <div @click="fileSwitcher=!fileSwitcher"
          class="job-option-header-action job-option-files-switcher">{{ fileSwitcherText }}</div>
        <a-upload
          multiple
          disabled
          list-type="picture"
          :file-list="files"
          class="job-option-files-upload"
          :class="{'all-the-files-are-shown': fileSwitcher}"/>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "JobOption",
  props: {
    option: {
      type: Object,
      default: null,
    }
  },
  data() {
    return {
      fileSwitcher: false,
    };
  },
  computed: {
    files() {
      return this.option.option_files.map((file)=>{
        return {
          uid: file.id,
          name: file.name,
          status: 'done',
          url: file.file,
        };
      });
    },
    fileSwitcherText(){
      return this.fileSwitcher ? 'Скрыть' : 'Показать все';
    },
  },
  methods: {

  },
  created() {

  },
  beforeDestroy() {

  }
};
</script>

<style lang="sass">
$border-color: #e8e8e8
.job-option
  display: flex
  flex-direction: column
  border: 1px solid $border-color
  border-radius: 4px
  transition: 0.2s ease-out
  margin-bottom: 10px
  &:hover
    box-shadow: 0px 1px 3px 1px #dedede

  &-header
    padding: 10px 15px
    border-bottom: 1px solid $border-color
    display: flex
    flex-direction: row
    align-items: center
    &-topic
      font-size: 18px
      flex: 1
    &-actions
      display: flex
      flex-direction: row
      align-items: center
      margin-left: 10px
    &-action
      color: #1890ff
      transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1)
      cursor: pointer
      &:hover
        color: #40a9ff

  &-body
    padding: 10px 15px
  &-skills
    display: flex
    flex-direction: row
    flex-wrap: wrap
    align-items: center
    margin-bottom: 10px
  &-skill
    padding: 4px 8px
    height: 30px
    border-radius: 15px
    border: 1px solid #e8e8e8
    background-color: #1890ff
    color: white
  &-form
    // font-style: italic
    font-weight: bold
    margin-bottom: 10px
  &-files
    position: relative
    &-upload
      display: flex
      flex-direction: column
      max-height: 80px
      &.all-the-files-are-shown
        max-height: none
      .ant-upload-list
        display: flex
        flex: 1
        flex-direction: row
        flex-wrap: wrap
        overflow-y: hidden
        .ant-upload-list-item
          min-width: 200px
          margin-right: 8px
    &-switcher
      padding-left: 5px
      background-color: white
      position: absolute
      top: 0
      right: 0

</style>
