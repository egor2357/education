<template>
  <a-spin :spinning="loading">
    <div class="appeal-details">
      <div class="appeal-details__title">
        <div class="top-bar">
          <div class="button-back">
            <a-button icon="left" @click="$router.go(-1)">Назад</a-button>
          </div>
          <div class="label">Обращения к руководству</div>
        </div>
        <div class="theme">Тема: {{ appealInfo.theme }}</div>
      </div>
      <div class="appeal-details__content">
        <div
          class="message-block"
          v-for="message in messages.results"
          :key="message.id"
          :class="
            message.author.id === userInfo.specialistId
              ? 'message-block_my'
              : 'message-block_other'
          "
        >
          <div class="message-block-wrapper">
            <div class="message-block-wrapper__text">
              {{ message.text }}
            </div>
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
            class="message-send-block__text-input"
            :rows="4"
          />
          <div class="buttons">
            <a-upload name="file">
              <a-button> <a-icon type="upload" /> Прикрепить файл </a-button>
            </a-upload>
            <a-button class="buttons__send-button" type="primary"
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
    };
  },
  async created() {
    await this.fetchAppealInfo(this.$route.params.id);
    this.loading = false;
  },
  methods: {
    ...mapActions({
      fetchAppealInfo: "appeals/fetchAppealInfo",
    }),
    ...mapMutations({
      setMessages: "appeals/setMessages",
    }),
  },
  computed: {
    ...mapGetters({
      messages: "appeals/getMessages",
      appealInfo: "appeals/getAppealInfo",
      userInfo: "auth/getUserInfo",
    }),
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

    .theme
      font-size: 1rem
      text-align: center
      margin-left: 92px


  &__content
    flex: 1 1 auto
    overflow-y: auto
    margin-bottom: 10px

    .message-block
      margin: 10px
      display: flex
      flex-direction: column

      &_my
        align-items: flex-end

      &_other
        align-items: flex-start

      .message-block-wrapper
        border: 3px solid
        border-radius: 10px
        padding: 10px

        &__time
          font-size: 0.8rem

  &__bottom
    .message-send-block
      display: flex
      flex-direction: row

    .buttons
      padding-left: 10px
      display: flex
      flex-direction: column
      justify-content: space-between

      &__send-button
        margin-top: 5px
</style>
