<template>
  <a-spin :spinning="loading">
    <div class="specialist-profile">
      <div class="specialist-profile__header">Профиль</div>
      <div class="specialist-profile__name" v-if="userData">
        <div class="specialist-profile__name-full">
          {{ userData.specialist.surname }}
          {{ userData.specialist.name }}
          {{ userData.specialist.patronymic }}
        </div>
        <a-divider type="vertical" />
        <div class="specialist-profile__name-login">
          {{ userData.username }}
        </div>
      </div>
      <div class="specialist-profile__specialties" v-if="specialties.length">
        <a-divider orientation="left">
          Основные виды деятельности
        </a-divider>
        <div class="activities">
          <div class="activity-block" v-for="specialty in mainSpecialties"
            :key="specialty.activity.id"
            :style="{
              'background-color': `${specialty.activity.color}4d`,
              border: `1px solid ${specialty.activity.color}99`,
            }">
            <span class="activity-label">{{
              specialty.activity.name
            }}</span>
          </div>
        </div>
        <a-divider orientation="left">
          Дополнительные виды деятельности
        </a-divider>
        <div class="activities">
          <div class="activity-block" v-for="specialty in subSpecialties"
            :key="specialty.activity.id"
            :style="{
              'background-color': `${specialty.activity.color}4d`,
              border: `1px solid ${specialty.activity.color}99`,
            }">
            <span class="activity-label">{{
              specialty.activity.name
            }}</span>
          </div>
        </div>
      </div>
      <div class="specialist-profile__header">Развиваемые навыки</div>
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
      specialties: [],
    };
  },
  async created() {
    let fetches = []

    if (!this.areasFetched) {
      fetches.push(this.fetchAreas());
    }
    fetches.push(this.fetchUserData());
    fetches.push(this.fetchSpecialties());


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

    async fetchSpecialties(){
      try {
        let res = await this.$axios.get("/api/specialties/");
        if (res.status === 200) {
          this.specialties = res.data;
        } else if (res.status === 400) {
          this.$message.error("Ошибка при загрузке видов деятельности пользователя");
        } else {
          this.$message.error("Ошибка при загрузке видов деятельности пользователя");
        }
      } catch (e) {
        this.$message.error("Ошибка при загрузке видов деятельности пользователя");
      } finally {
        this.loading = false;
      }
    },
    ...mapActions({
      fetchAreas: "skills/fetchAreas",
    }),
  },
  computed: {
    ...mapGetters({
      areasFetched: "skills/getFetched",
      areas: "skills/getFilteredAreas",
    }),
    mainSpecialties(){
      return this.specialties.filter((specialty)=>{
        return specialty.is_main;
      })
    },
    subSpecialties(){
      return this.specialties.filter((specialty)=>{
        return !specialty.is_main;
      })
    },
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
      &-login
        color: #1890ff

    .activities
        display: flex
        flex-wrap: wrap
        .activity-block
          margin: 5px
          padding: 3px
          -webkit-border-radius: 4px
          -moz-border-radius: 4px
          border-radius: 4px
          .activity-label
            margin: 5px
            color: #111111



</style>
