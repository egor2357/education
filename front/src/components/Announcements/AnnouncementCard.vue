<template>
  <a-card :title="data.caption" class="announcement-card">
    <a slot="extra" v-if="isStaff" @click="displayDelete(data)">Удалить</a>
    <p class="announcement-card__text">{{ data.text }}</p>
  </a-card>
</template>

<script>
import { mapActions, mapMutations, mapGetters } from "vuex";

export default {
  name: "AnnouncementCard",
  props: {
    data: Object,
  },
  computed: {
    isStaff() {
      return this.$store.getters["auth/getUserInfo"].staff;
    },
    ...mapGetters({
      queryParams: "announcements/getQueryParams",
    }),
  },
  methods: {
    ...mapActions({
      fetchAnnouncements: "announcements/fetchAnnouncements",
      deleteAnnouncement: "announcements/deleteAnnouncement",
    }),
    ...mapMutations({
      setQueryParams: "announcements/setQueryParams",
    }),
    displayDelete({ id, caption }) {
      let that = this;
      this.$confirm({
        title: `Запись "${caption}" будет удалена.`,
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
          this.$message.success("Запись успешно удалена");
          let res = this.fetchAnnouncements();
          if (res.status !== 200) {
            let page = Number(this.queryParams.replace("?page=", ""));
            if (page > 1) {
              page -= 1;
            }
            this.setQueryParams(`?page=${page}`);
            this.fetchAnnouncements();
          }
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
