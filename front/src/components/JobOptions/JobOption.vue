<template>
  <div hoverable class="job-option">
    <div class="job-option-header">
      <div class="job-option-header-topic">
        {{ option.topic ? option.topic : 'Тема не указана' }}
      </div>
      <slot></slot>
    </div>
    <div class="job-option-body">
      <div class="job-option-skills">
        <template v-if="option.skills.length">
          <div
            class="job-option-skill"
            v-for="skill in option.skills"
            :key="skill.id"
          >
            {{ skill.area_number }}.{{ skill.direction_number }}.{{
              skill.number
            }}.
            {{ skill.name }}
          </div>
        </template>
        <div class="job-option-skill job-option-skill--empty" v-else>
          Навыки не выбраны
        </div>
      </div>
      <div class="job-option-form" v-if="option.method">
        {{ option.method.form_name }}
        <a-divider type="vertical" />
        {{ option.method.name }}
      </div>
      <div class="job-option-form" v-else>
        Форма и способ не выбраны
      </div>
      <div class="job-option-comment">{{ option.comment }}</div>
      <div class="job-option-files" v-if="files.length">
        <a-divider orientation="left"> Методические материалы </a-divider>
        <div class="files-upload-with-arrows">
          <a-icon
            type="left"
            class="arrow-left"
            @click="clickLeftArrow"
            v-if="scrollable"
          />
          <a-upload
            multiple
            disabled
            list-type="picture"
            :file-list="files"
            class="job-option-files-upload"
            @preview="clickOnFile($event)"
            ref="files-list"
          />
          <a-icon
            type="right"
            class="arrow-right"
            @click="clickRightArrow"
            v-if="scrollable"
          />
        </div>
      </div>
    </div>
    <MediaLightBox
      v-if="displayMedia"
      :files="files"
      @close="displayMedia = false"
      :selectedFile="selectedFile"
    />
  </div>
</template>

<script>
import consts from "@/const";
import MediaLightBox from "@/components/MediaLightBox";
export default {
  name: "JobOption",
  components: {
    MediaLightBox,
  },
  props: {
    option: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      displayMedia: false,
      photoFormats: consts.photoFormats,
      videoFormats: consts.videoFormats,
      selectedFile: null,
      filesEl: null,
    };
  },
  computed: {
    files() {
      return this.option.option_files.map((file) => {
        return {
          uid: file.id,
          name: file.name,
          status: "done",
          url: file.file,
          thumbUrl: file.thumbnail,
          photo:
            file.name.split(".").pop() !== file.name &&
            this.photoFormats.indexOf(file.name.split(".").pop()) !== -1,
          video:
            file.name.split(".").pop() !== file.name &&
            this.videoFormats.indexOf(file.name.split(".").pop()) !== -1,
        };
      });
    },
    scrollable() {
      if (this.filesEl) {
        return this.filesEl.scrollWidth > this.filesEl.clientWidth;
      } else {
        return false;
      }
    },
  },
  methods: {
    clickOnFile(file) {
      if (file.video || file.photo) {
        this.selectedFile = file;
        this.displayMedia = true;
      } else {
        window.open(file.url);
      }
    },
    clickRightArrow() {
      this.filesEl.scrollLeft += 600;
    },
    clickLeftArrow() {
      this.filesEl.scrollLeft -= 600;
    },
  },
  mounted() {
    this.$nextTick(() => {
      if (this.files.length) {
        this.filesEl = this.$refs["files-list"].$el.children[1];
      }
    });
  },
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
    margin-right: 5px
    margin-bottom: 5px

    &--empty
      background-color: #f9f9f9
      color: #000

  &-form
    font-weight: bold
    margin-bottom: 10px
  &-files
    position: relative
    &-upload
      display: flex
      flex-direction: column
      max-height: 80px
      .ant-upload-list
        overflow-y: hidden
        .ant-upload-list-item
          min-width: 200px
          margin-right: 8px
          &-name
            max-width: 300px
            line-height: 1.5rem
            height: 3rem
            text-overflow: ellipsis
            white-space: pre-line


.files-upload-with-arrows
  display: flex
  .arrow-left, .arrow-right
    margin: 0 5px
    align-self: center
    font-size: 18px
  .job-option-files-upload
    flex: auto
    overflow-x: hidden
  .ant-upload-list
    max-height: 80px
    white-space: nowrap
    overflow-x: hidden
    div
      display: inline-block
</style>
