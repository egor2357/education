<template>
  <div class="exercises-for-specialists-container">
    <div class="top-bar">
      <div class="top-bar__side-block left">
        <a-input v-model.trim="searchText" placeholder="Поиск" class="search-input" allow-clear/>
      </div>
      <div class="title">Упражнения специалистов</div>
      <div class="top-bar__side-block right">
        <a-select
          v-model="showMode"
          class="mode-select"
        >
          <a-select-option
            :key="1"
          >
            Все упражнения
          </a-select-option>
          <a-select-option
            :key="2"
          >
            Только назначенные выбранным специалистам
          </a-select-option>
          <a-select-option
            :key="3"
          >
            Только неназначенные упражнения
          </a-select-option>
        </a-select>
      </div>
    </div>
    <ExercisesMatrix :showMode="showMode" :searchText="searchText" />
  </div>
</template>

<script>
import ExercisesMatrix from "@/components/ExercisesMatrix/ExercisesMatrix"
export default {
  name: "ExercisesForSpecialists",
  components: {
    ExercisesMatrix
  },
  data () {
    return {
      showMode: 1,
      searchText: '',
    }
  }
};
</script>

<style lang="sass">
.exercises-for-specialists-container
  height: 100%
  display: flex
  flex-direction: column

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

    &.left
      .search-input
        width: 300px

    &.right
      text-align: right
      .mode-select
        width: 400px

</style>
