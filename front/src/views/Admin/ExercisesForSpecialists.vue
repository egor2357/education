<template>
  <div class="exercises-for-specialists-container">
    <div class="top-bar">
      <div class="top-bar__side-block left"></div>
      <div class="title">Упражнения специалистов</div>
      <div class="top-bar__side-block right"></div>
    </div>
    <ExercisesMatrix />
  </div>
</template>

<script>
import ExercisesMatrix from "@/components/ExercisesMatrix/ExercisesMatrix"
export default {
  name: "ExercisesForSpecialists",
  components: {
    ExercisesMatrix
  },
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

    &.right
      text-align: right

</style>
