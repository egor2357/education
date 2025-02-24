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
        <a-divider orientation="left"> Основные виды деятельности </a-divider>
        <div class="activities">
          <div
            class="activity-block"
            v-for="specialty in mainSpecialties"
            :key="specialty.activity.id"
            :style="{
              'background-color': `${specialty.activity.color}4d`,
              border: `1px solid ${specialty.activity.color}99`,
            }"
          >
            <span class="activity-label">{{ specialty.activity.name }}</span>
          </div>
        </div>
        <template v-if="subSpecialties.length">
          <a-divider orientation="left">
            Дополнительные виды деятельности
          </a-divider>
          <div class="activities">
            <div
              class="activity-block"
              v-for="specialty in subSpecialties"
              :key="specialty.activity.id"
              :style="{
                'background-color': `${specialty.activity.color}4d`,
                border: `1px solid ${specialty.activity.color}99`,
              }"
            >
              <span class="activity-label">{{ specialty.activity.name }}</span>
            </div>
          </div>
        </template>
      </div>
      <a-divider orientation="left" v-else>
        Специалист не преподает ни одного вида деятельности
      </a-divider>
    </div>
  </a-spin>
</template>

<script>

export default {
  components: {},
  name: "SpecialistProfile",
  data() {
    return {
      loading: true,

      userData: null,
      specialties: [],
    };
  },
  async created() {
    let fetches = [];

    fetches.push(this.fetchUserData());
    fetches.push(this.fetchSpecialties());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
  },
  methods: {
    async fetchUserData() {
      try {
        this.loading = true;
        let res = await this.$axios.get("/api/users/current/");
        if (res.status === 200) {
          this.userData = res.data;
        } else if (res.status === 400) {
          this.$message.error("Ошибка при загрузке данных специалиста");
        } else {
          this.$message.error("Ошибка при загрузке данных специалиста");
        }
      } catch (e) {
        this.$message.error("Ошибка при загрузке данных специалиста");
      } finally {
        this.loading = false;
      }
    },

    async fetchSpecialties() {
      try {
        let res = await this.$axios.get("/api/specialties/");
        if (res.status === 200) {
          this.specialties = res.data;
        } else if (res.status === 400) {
          this.$message.error(
            "Ошибка при загрузке видов деятельности специалиста"
          );
        } else {
          this.$message.error(
            "Ошибка при загрузке видов деятельности специалиста"
          );
        }
      } catch (e) {
        this.$message.error(
          "Ошибка при загрузке видов деятельности специалиста"
        );
      } finally {
        this.loading = false;
      }
    },

  },
  computed: {
    mainSpecialties() {
      return this.specialties.filter((specialty) => {
        return specialty.is_main;
      });
    },
    subSpecialties() {
      return this.specialties.filter((specialty) => {
        return !specialty.is_main;
      });
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
    margin-bottom: 5px
    min-height: 30px
    &-login
      color: #1890ff
    .ant-divider
      height: 15px
      margin-top: 12px
  &__specialties
    .ant-divider
      margin: 0
      &::before, &::after
        position: unset
  &__competence
    overflow: auto

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

  &__table
    display: flex
    flex: 1
    flex-direction: column
    border-left: 1px solid #ccc
    &-header
      border-top: 1px solid #ccc
      display: flex
      flex: 1
      flex-direction: row
      background-color: #f4f4f4
      color: rgba(0, 0, 0, 0.85)
      z-index: 3
      position: sticky
      position: -webkit-sticky
      top: 0
      div
        display: flex
        align-items: center
    &-body
      display: flex
      flex: 1
      flex-direction: column
</style>
