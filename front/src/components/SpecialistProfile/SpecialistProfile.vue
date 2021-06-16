<template>
  <a-spin :spinning="loading">
    <div class="specialist-profile">
      <div class="specialist-profile__header">Профиль</div>
      <div class="specialist-profile__wrapper" v-if="userData">
        <div class="specialist-profile__name">
          <div class="specialist-profile__name-full">
            {{ userData.specialist.surname }}
            {{ userData.specialist.name }}
            {{ userData.specialist.patronymic }}
          </div>
          <div class="specialist-profile__name-login">
            {{ userData.username }}
          </div>
        </div>
        <div class="specialist-profile__specialties">Виды деятельности</div>
      </div>
    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  components: {
  },
  name: "SpecialistProfile",
  data() {
    return {
      loading: true,

      userData: null,
    };
  },
  async created() {
    let fetches = []

    // if (!this.activitiesFetched) {
    //   fetches.push(this.fetchActivities());
    // }
    await this.fetchUserData();

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

  },
  methods: {
    async fetchUserData(){
      try {
        this.loading = true;
        let res = await this.$axios.get("/api/users/current");
        if (res.status === 200) {
          this.userData = res.data;
        } else if (res.status === 400) {
          this.$message.error("Ошибка при загрузке данных пользователя");
        } else {
          this.$message.error("Ошибка при загрузке данных пользователя");
        }
      } catch (e) {
        this.$message.error("Ошибка при загрузке данных пользователя");
      } finally {
        this.loading = false;
      }
    },
    ...mapActions({
      // fetchSpecialists: "specialists/fetchSpecialists",
      // fetchActivities: "activities/fetchActivities",
      // fetchSchedule: "schedule/fetchJobs",
    }),
  },
  computed: {
    ...mapGetters({
      // specialists: "specialists/getSpecialists",
      // specialistsFetched: "activities/getFetched",
    }),
  },
};
</script>

<style lang="sass">
  .specialist-profile
    display: flex
    flex-direction: column
    height: 100%
    overflow: hidden
    &__header
      text-align: center
      font-size: 16px
      margin-bottom: 10px
    &__wrapper
      display: flex
      flex-direction: column
      flex: 1
    &__name
      display: flex
      flex-direction: row
      font-size: 22px
      &-full
        margin-right: 10px
        padding-right: 10px
        border-right: 1px solid #e8e8e8
      &-login
        color: #1890ff



</style>
