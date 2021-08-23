<template>
  <a-card :title="data.caption" class="announcement-card">
    <a slot="extra" v-if="isStaff" @click="displayDelete(data)">Удалить</a>
    <p class="announcement-card__text">{{ data.text }}</p>
  </a-card>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "AnnouncementCard",
  props: {
    data: Object,
  },
  computed: {
    isStaff() {
      return this.$store.getters["auth/getUserInfo"].staff;
    },
  },
  methods: {
    ...mapActions({
      fetchAnnouncements: "announcements/fetchAnnouncements",
      deleteAnnouncement: "announcements/deleteAnnouncement",
    }),
    displayDelete({ id, caption }) {
      let that = this;
      this.$confirm({
        title: `Объявление "${caption}" будет удалено.`,
        content: `Продолжить?`,
        okType: "danger",
        onOk() {
          that.deleteRecord(id);
        },
      });
    },
    async deleteRecord(id) {
      try {
        this.$emit("startLoading");
        let res = await this.deleteAnnouncement(id);
        if (res.status === 204) {
          this.$message.success("Объявление успешно удалено");
          this.fetchAnnouncements();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.$emit("endLoading");
      }
    },
  },
};
</script>

<style lang="sass">
.announcement-card
  margin: 15px
  &__text
    white-space: pre-line
</style>
