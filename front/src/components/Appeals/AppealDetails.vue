<template>
  <a-spin :spinning="loading">
    <div class="appeal-details">
      <div class="appeal-details__title">
        <div class="top-bar">
          <div class="button-back">
            <a-button icon="left" @click="$router.go(-1)">Назад</a-button>
          </div>
          <div class="label">Обращения к руководству</div>
          <div class="button-close" @click="displayClose">
            <a-button :disabled="appealInfo.closed" v-if="userInfo.staff">Закрыть обращение</a-button>
          </div>
        </div>
        <div class="theme">Тема: {{ appealInfo.theme }}</div>
      </div>
      <div class="appeal-details__content">
        <div
          class="message-block"
          v-for="message in messages"
          :key="message.id"
          :class="
            message.author.id === userInfo.specialistId
              ? 'message-block_my'
              : 'message-block_other'
          "
        >
          <div class="message-block-wrapper">
            <div class="message-block-wrapper__author">
              {{ message.author.__str__ }}
            </div>
            <div class="message-block-wrapper__text" v-if="message.text">{{ message.text }}</div>
            <a
              class="message-block-wrapper__file"
              target="_blank"
              :href="message.file"
              v-if="message.file"
            >
              {{ message.filename }}
            </a>
            <div class="message-block-wrapper__time">
              {{ formatDateTime(message.creation_date) }}
            </div>
          </div>
        </div>
      </div>
      <div class="appeal-details__bottom">
        <div class="message-send-block">
          <a-textarea
            v-model="text"
            ref="messageTextarea"
            :disabled="appealInfo.closed"
            :rows="4"
            placeholder="Введите текст сообщения"
          />
          <div class="buttons">
            <a-upload
              name="file"
              :fileList="fileList"
              @change="changeFiles"
              :beforeUpload="
                () => {
                  return false;
                }
              "
              class="file-input"
            >
              <a-button :disabled="appealInfo.closed" v-if="!fileList.length">
                <a-icon type="upload" /> Прикрепить файл
              </a-button>
            </a-upload>
            <a-button
              type="primary"
              @click="sendMessage"
              :disabled="
                appealInfo.closed || (!fileList.length && text.trim() === '')
              "
              >Отправить</a-button
            >
          </div>
        </div>
      </div>
    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from "vuex";
import datetime from "@/mixins/datetime";
export default {
  name: "AppealDetails",
  mixins: [datetime],
  data() {
    return {
      loading: true,
      text: "",
      file: null,
      fileList: [],
    };
  },
  async created() {
    await this.fetchAppealInfo(this.$route.params.id);
    await this.fetchMessages(this.$route.params.id);
    await this.fetchNotifications();
    this.loading = false;
    this.$refs.messageTextarea.focus();
  },
  methods: {
    ...mapActions({
      fetchAppealInfo: "appeals/fetchAppealInfo",
      fetchMessages: "appeals/fetchMessages",
      addMessage: "appeals/addMessage",
      setClosed: "appeals/setAppealClosed",
      fetchNotifications: "notifications/fetchNotifications",
    }),
    ...mapMutations({
      setMessages: "appeals/setMessages",
    }),
    async sendMessage() {
      let formData = new FormData();
      formData.set("appeal_id", this.$route.params.id);
      formData.set("text", this.text);
      if (this.file) {
        formData.append("file", this.file, this.file.name);
      }
      let res = await this.addMessage(formData);
      if (res.status === 201) {
        this.$message.success("Сообщение успешно отправлено");
        this.text = "";
        this.fileList = [];
        this.file = null;
      } else {
        this.$message.error("При отправке сообщения произошла ошибка");
      }
      await this.fetchMessages(this.$route.params.id);
    },
    changeFiles(info) {
      if (info.fileList.length > 1) {
        this.fileList = info.fileList.splice(1, 1);
      } else {
        this.fileList = info.fileList;
      }
      if (!info.file.status) {
        this.file = info.file;
      } else {
        this.file = null;
      }
    },
    displayClose() {
      let that = this;
      this.$confirm({
        title: `Данная тема будет закрыта.`,
        content: `Продолжить?`,
        okType: "danger",
        onOk() {
          that.closeTheme();
        },
      });
    },
    async closeTheme() {
      try {
        let res = await this.setClosed(this.appealInfo.id);
        if (res.status === 200) {
          await this.fetchAppealInfo(this.$route.params.id);
          this.$message.success("Тема успешно закрыта");
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      }
    },
  },
  computed: {
    ...mapGetters({
      messages: "appeals/getMessages",
      appealInfo: "appeals/getAppealInfo",
      userInfo: "auth/getUserInfo",
    }),
  },
  watch: {
    messages(value) {
      const element = document.getElementsByClassName(
        "appeal-details__content"
      )[0];
      this.$nextTick(() => {
        element.scrollTop = element.scrollHeight - element.clientHeight;
      });
    },
  },
  destroyed() {
    this.setMessages([]);
  },
};
</script>

<style lang="sass">
.appeal-details
  display: flex
  flex-direction: column
  height: 100%
  overflow: hidden

  &__title
    flex-basis: 100px
    line-height: 32px

    .top-bar
      display: flex
      flex-direction: row

      .label
        flex: auto
        font-size: 1rem
        text-align: center

      .button-close, .button-back
        flex: 1

      .button-close
        text-align: right

    .theme
      font-size: 1rem
      text-align: center


  &__content
    flex: 1 1 auto
    overflow-y: auto
    margin: 0 auto 10px auto
    width: 900px

    .message-block
      margin: 10px
      display: flex
      flex-direction: column

      .message-block-wrapper
        border: 1px solid
        border-radius: 10px
        padding: 10px

        &__time
          font-size: 0.8rem
          opacity: 0.65
          text-align: right

        &__author
          font-size: 0.8rem
          opacity: 0.65
          text-align: left

        &__text
          white-space: pre-wrap

      &_other
        align-items: flex-start
        max-width: 60%

        .message-block-wrapper
          border-color: #90c6e6
          background: #eaf7ff

      &_my
        align-items: flex-end
        margin-left: 40%

        .message-block-wrapper
          border-color: #a7deab
          background: #ecffec

  &__bottom
    width: 900px
    margin: 0 auto

    .message-send-block
      display: flex
      flex-direction: column

      .buttons
        display: flex
        flex-direction: row
        justify-content: space-between
        margin-top: 10px
        height: 35px

        .file-input
          max-width: 795px

      .ant-upload-list-item-name
        padding-right: 10px
</style>
