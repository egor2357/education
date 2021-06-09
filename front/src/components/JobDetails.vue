<template>
  <a-spin :spinning="loading">
    <div class="job-details">
      <div class="job-details__header">

        <div class="job-details__header-title">
          Занятие
        </div>

        <div class="job-details__header__options">
          <div class="job-details__header__options__back">
            <a-button icon="left" @click="goBack">Назад</a-button>
          </div>
          <div class="job-details__header__options__title">

          </div>
        </div>

      </div>

      <div class="job-details__body">
      </div>
    </div>
  </a-spin>
</template>

<script>
// import moment from "moment";

export default {
  name: "JobDetails",
  props: {
  },
  data() {
    return {
      loading: true,
    };
  },
  computed: {

  },
  methods: {
    goBack(){
      this.$router.go(-1);
    },
  },
  async created() {
  },
  beforeDestroy() {

  }
};
</script>

<style lang="sass">
.job-details
  display: flex
  flex-direction: column
  overflow: hidden
  height: 100%
  &__header
    display: flex
    flex-direction: column
    &-title
      flex-grow: 1
      text-align: center
      font-size: 1rem
      margin-bottom: 10px
    &__options
      display: flex
      flex-direction: row
      align-items: center
      justify-content: space-between
      margin-bottom: 10px
      &__back
        display: flex
        flex-direction: row
        justify-content: flex-start
        flex: 1
      &__title
        display: flex
        flex-direction: row
        justify-content: center
        flex: 1
        font-size: 20px
      &__date-range
        display: flex
        flex-direction: row
        flex: 1
        align-items: center
        justify-content: flex-end
        &__label
          margin-right: 10px

  &__body


</style>
