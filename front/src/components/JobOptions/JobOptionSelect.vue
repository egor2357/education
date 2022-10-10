<template>
    <a-modal
      width="1000px"
      :visible="true"
      :title="'Выбор варианта проведения занятия'"
      :footer="null"
      @cancel="closeModal(null)"
    >
    <a-spin :spinning="loading">

      <div class="job-option-select__params">

        <div class="job-option-select__params-label">Специалист:</div>
        <a-select v-model="currSpecialistId"
          @change="fetchOptions"
          class="job-option-select__params-select">
          <a-select-option v-for="specialist in specialists"
            :key="specialist.id">
            {{specialist.__str__}}
          </a-select-option>
        </a-select>

        <div class="job-option-select__params-label">Вид деятельности:</div>
        <a-select v-model="currActivityId"
          @change="fetchOptions"
          class="job-option-select__params-select">
          <a-select-option v-for="activity in activities"
            :key="activity.id">
            {{activity.name}}
          </a-select-option>
        </a-select>
      </div>
      <div class="job-options__filters-container">
        <a-input
          v-model="search"
          @change="searchOptions"
          class="job-options__filters-search"
          placeholder="Поиск по карточкам"
        />
        <a-select
          v-model="orderingType"
          @change="fetchOptions"
          class="job-options__filters-select"
        >
          <a-select-option value="-date">По дате добавления <a-icon type="caret-down" /></a-select-option>
          <a-select-option value="date">По дате добавления <a-icon type="caret-up" /></a-select-option>
          <a-select-option value="topic">По алфавиту <a-icon type="sort-ascending" /></a-select-option>
          <a-select-option value="-topic">По алфавиту <a-icon type="sort-descending" /></a-select-option>
        </a-select>
      </div>

      <div class="job-option-select__cards" v-if="options.length">
        <div class="job-option-select__card" v-for="option in options" :key="option.id">
          <job-option :option="option">
            <div class="job-option-header-actions">
              <div class="job-option-header-action"
                @click="closeModal(option, false)">
                Добавить к существующему
              </div>
              <a-divider type="vertical"/>
              <div class="job-option-header-action"
                @click="closeModal(option, true)">
                Выбрать
              </div>
            </div>
          </job-option>
        </div>
      </div>
      <div v-else>
        <a-empty :image="simpleImage"/>
      </div>

    </a-spin>
    </a-modal>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import JobOption from "@/components/JobOptions/JobOption";
import { Empty } from 'ant-design-vue';

export default {
  name: "JobOptionSelect",
  components: {
    JobOption,
  },
  props: {
    job: {
      type: Object,
      default: null,
    }
  },
  data() {
    return {
      loading: false,

      search: '',
      searchTimeoutId: 0,
      orderingType: '-date',

      options: [],
      currSpecialistId: this.job.specialist.id,
      currActivityId: this.job.activity.id,
    };
  },
  computed: {
    ...mapGetters({
      specialists: "specialists/getOnlySpecialists",
      activities: "activities/getActivities",
    }),
  },

  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  async created() {
    let fetches = [];
    fetches.push(this.fetchOptions());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
  },

  methods: {
    closeModal(option=null, replace=true){
      this.$emit('closeModal', {option, replace});
    },
    async fetchOptions() {
      try {
        this.loading = true;
        let activityParam = `activity_id=${this.currActivityId}`;
        let specialistParam = `specialist_id=${this.currSpecialistId}`;
        let filterParams = `ordering=${this.orderingType}`;
        if (this.search) {
          filterParams += `&search=${this.search}`
        }
        let res = await this.$axios.get(`/api/options/?${activityParam}&${specialistParam}&${filterParams}`);
        if (res.status === 200) {
          this.options = res.data;
          this.isOptionFetched = true;
        } else if (res.status === 400) {
          this.$message.error("Ошибка при загрузке планов занятий специалиста");
        } else {
          this.$message.error("Ошибка при загрузке планов занятий специалиста");
        }
      } catch (e) {
        this.$message.error("Ошибка при загрузке планов занятий специалиста");
      } finally {
        this.loading = false;
      }
    },

    searchOptions() {
      if (this.searchTimeoutId) {
        clearTimeout(this.searchTimeoutId);
      }
      this.searchTimeoutId = setTimeout(this.fetchOptions, 400);
    },
  },
};
</script>

<style lang="sass">
.job-option-select
  &__params
    margin-bottom: 20px
    display: flex
    flex-direction: row
    align-items: center

    &-label
      margin-right: 10px
    &-select
      margin-right: 20px
      display: flex
      flex: 1
      &:last-child
        margin-right: 0
      .ant-select-selection
        width: 100%

  &__cards
    height: 100%
    overflow-y: auto
    padding: 3px

.job-options
  &__filters-container
    display: flex
    flex-direction: row
    align-items: center
    width: 100%
    padding: 3px
  &__filters-search
    margin-right: 10px
    flex: 2
  &__filters-select
    flex: 1

</style>
