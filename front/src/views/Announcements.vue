<template>
  <a-spin :spinning="loading">
    <div class="announcements-block">
      <div class="top-bar">
        <div class="top-bar__side-block left"></div>
        <div class="title">Важная информация</div>
        <div class="top-bar__side-block right">
          <a-button icon="plus" @click="displayAdd" v-if="isStaff">
            Добавить
          </a-button>
        </div>
      </div>
      <div class="announcements-block__cards">
        <AnnouncementCard
          v-for="announcement in announcements.results"
          :key="announcement.id"
          :data="announcement"
          @startLoading="loading = true"
          @endLoading="enterF"
        />
      </div>
      <AnnouncementsModal
        v-if="displayModal"
        :adding="modalAdding"
        :editableData="modalEditableData"
        @closeSuccess="closeModalSuccess"
        @close="displayModal = false"
      />
    </div>
  </a-spin>
</template>

<script>
import AnnouncementsModal from "@/components/Announcements/AnnouncementsModal";
import AnnouncementCard from "@/components/Announcements/AnnouncementCard";
import { mapActions, mapGetters } from "vuex";
export default {
  name: "Announcements",
  components: {
    AnnouncementsModal,
    AnnouncementCard,
  },
  data() {
    return {
      loading: true,
      displayModal: false,
      modalAdding: true,
      modalEditableData: null,
    };
  },
  async created() {
    await this.fetchAnnouncements();
    this.loading = false;
  },
  methods: {
    ...mapActions({
      fetchAnnouncements: "announcements/fetchAnnouncements",
    }),
    displayAdd() {
      this.displayModal = true;
      this.modalAdding = true;
    },
    async closeModalSuccess() {
      this.displayModal = false;
      this.loading = true;
      await this.fetchAnnouncements();
      this.loading = false;
    },
    enterF() {
      console.log(this.loading);
      console.log("e");
      this.loading = false;
    },
  },
  computed: {
    ...mapGetters({
      announcements: "announcements/getAnnouncements",
    }),
    isStaff() {
      return this.$store.getters["auth/getUserInfo"].staff;
    },
  },
};
</script>

<style lang="sass">
.announcements-block
  display: flex
  flex-direction: column
  overflow: hidden
  height: 100%

  .top-bar
    display: flex
    margin-bottom: 10px
    line-height: 32px

    .title
      font-size: 1rem
      text-align: center
      margin: 0 10px

  .top-bar__side-block
    flex: 1

    &.right
      text-align: right

  &__cards
    padding: 0 20%

    @media (max-width: 1300px)
      padding: 0 5%
</style>
