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
      <div class="announcements-block-cards flex-column">
        <template v-if="pagination.total > 0">
          <div class="announcements-block-cards__cards-list">
            <AnnouncementCard
              v-for="announcement in announcements.results"
              :key="announcement.id"
              :data="announcement"
              @startLoading="loading = true"
              @endLoading="loading = false"
            />
          </div>
          <a-pagination
            class="announcements-block-cards__pagination"
            :total="pagination.total"
            :current="pagination.page"
            @change="paginationChanged"
          />
        </template>
        <a-empty v-else :image="simpleImage" />
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
import { mapActions, mapGetters, mapMutations } from "vuex";
import { Empty } from "ant-design-vue";
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
    await this.fetchAnnouncements(`?page=${this.pagination.page}`);
    await this.fetchNotifications();
    this.loading = false;
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  methods: {
    ...mapActions({
      fetchAnnouncements: "announcements/fetchAnnouncements",
      fetchNotifications: "notifications/fetchNotifications",
    }),
    ...mapMutations({
      setQueryParams: "announcements/setQueryParams",
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
    async paginationChanged(page) {
      this.loading = true;
      this.pagination.page = page;
      this.setQueryParams(`?page=${page}`);
      await this.fetchAnnouncements();
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
    pagination() {
      let total = 0;
      let page = 1;
      if (this.announcements.pagination) {
        total = this.announcements.pagination.count;
        page = this.announcements.pagination.page;
      }
      return {
        total: total,
        page: page,
      };
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

  &-cards
    padding: 0 20%
    overflow: hidden


    .ant-pagination
      text-align: right
      margin: 5px 15px 0 15px

    &__cards-list
      overflow-y: auto

      @media (max-width: 1300px)
        padding: 0 5%
</style>
