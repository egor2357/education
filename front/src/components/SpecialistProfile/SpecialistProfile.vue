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
      <div class="specialist-profile__header">Развиваемые навыки</div>
      <div class="specialist-profile__competence" v-if="competence.length">
        <div class="specialist-profile__table">
          <div>
            <div class="specialist-profile__table-header">
              <div class="specialist-profile__table-area">
                Образовательная область
              </div>
              <div class="specialist-profile__table-direction">
                Направление развития
              </div>
              <div class="specialist-profile__table-skill">Навык</div>
              <div class="specialist-profile__table-coefficient">
                Коэффициент
              </div>
            </div>
            <div class="specialist-profile__table-body">
              <div class="specialist-profile__table-areas">
                <div
                  class="specialist-profile__table-area-row"
                  v-for="area in areas"
                  :key="area.id"
                >
                  <div class="specialist-profile__table-area">
                    {{ area.number }}. {{ area.name }}
                  </div>

                  <div
                    class="specialist-profile__table-directions"
                    v-if="area.development_directions.length"
                  >
                    <div
                      class="specialist-profile__table-direction-row"
                      v-for="direction in area.development_directions"
                      :key="direction.id"
                    >
                      <div class="specialist-profile__table-direction">
                        {{ area.number }}.{{ direction.number }}.
                        {{ direction.name }}
                      </div>

                      <div
                        class="specialist-profile__table-skills"
                        v-if="direction.skills.length"
                      >
                        <div
                          class="specialist-profile__table-skill-row"
                          v-for="skill in direction.skills"
                          :key="skill.id"
                        >
                          <div class="specialist-profile__table-skill">
                            <span>
                              {{ area.number }}.{{ direction.number }}.{{
                                skill.number
                              }}. {{ skill.name }}
                            </span>
                          </div>
                          <div class="specialist-profile__table-coefficient">
                            {{ coefficientBySkillId[skill.id] }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <a-divider orientation="left" v-else>
        Специалист не развивает ни одного навыка
      </a-divider>
    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  components: {},
  name: "SpecialistProfile",
  data() {
    return {
      loading: true,

      userData: null,
      specialties: [],
      competence: [],
      coefficientBySkillId: {},
    };
  },
  async created() {
    let fetches = [];

    if (!this.areasFetched) {
      fetches.push(this.fetchAreas());
    }
    fetches.push(this.fetchUserData());
    fetches.push(this.fetchSpecialties());
    fetches.push(this.fetchCompetence());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
  },
  methods: {
    async fetchUserData() {
      try {
        this.loading = true;
        let res = await this.$axios.get("/api/users/current");
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

    setCoefficientBySkillId(competence) {
      for (let comp of competence) {
        this.coefficientBySkillId[comp.skill_id] = comp.coefficient;
      }
    },

    async fetchCompetence() {
      try {
        let res = await this.$axios.get("/api/competence/");
        if (res.status === 200) {
          this.competence = res.data;
          this.setCoefficientBySkillId(res.data);
        } else if (res.status === 400) {
          this.$message.error("Ошибка при загрузке навыков специалиста");
        } else {
          this.$message.error("Ошибка при загрузке навыков специалиста");
        }
      } catch (e) {
        this.$message.error("Ошибка при загрузке навыков специалиста");
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
    height: 40px
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

    &-areas, &-directions, &-skills
      display: flex
      flex: 1
      flex-direction: column
    &-area-row, &-direction-row, &-skill-row
      display: flex
      flex: 1
      flex-direction: row
    &-area, &-direction, &-coefficient
      min-width: 200px
      width: 200px
      padding: 10px 15px
      border-right: 1px solid #ccc
      border-bottom: 1px solid #ccc
    &-skill
      min-width: 200px
      flex: 1
      padding: 10px 15px
      border-right: 1px solid #ccc
      border-bottom: 1px solid #ccc
      &-link
        color: #1890ff
        transition: all .3s cubic-bezier(.645,.045,.355,1)
        cursor: pointer
        &:hover
          color: #40a9ff
</style>
