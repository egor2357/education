<template>
  <a-card :title="data.caption" class="announcement-card">
    <a slot="extra" v-if="isStaff" @click="displayDelete(data)">Удалить</a>
    <p class="announcement-card__text">{{ data.text }}</p>
  </a-card>
</template>

<script>

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
    displayDelete({ id, caption }) {
      let that = this;
      this.$confirm({
        title: `Запись "${caption}" будет удалена.`,
        content: `Продолжить?`,
        okType: "danger",
        onOk() {
          that.$emit('deleteRecord', id);
        },
      });
    },
  }
};
</script>

<style lang="sass">
.announcement-card
  margin: 15px
  &__text
    white-space: pre-line
</style>
