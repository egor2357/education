<template>
  <div
    class="job-card"
    :style="{
      'background-color': `${job.activity.color}4d`,
      border: `1px solid ${job.activity.color}99`,
    }"
  >
    <div class="job-time">{{ job.start_time.substr(0, 5) }}</div>

    <a-dropdown :trigger="['click']"
      placement="bottomLeft"
      class="dropdown--hover">

      <a-icon class="icon-button" type="dash"></a-icon>
      <a-menu slot="overlay">
        <a-menu-item key="1" @click="openModalEdit(job)">
          Изменить
        </a-menu-item>
        <a-menu-item
          key="2"
          @click="displayConfirmDelete(job)"
        >
          <span> Удалить </span>
        </a-menu-item>
      </a-menu>
    </a-dropdown>

    <div class="job__name">{{ job.activity.name }}</div>
    <div class="job__specialist" v-if="job.specialist">
      <div class="job__specialist-label">Специалист:</div>
      <div class="job__specialist-name">{{ job.specialist.__str__ }}</div>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "JobCard",
  props: {
    job: {
      type: Object,
      default: null,
    }
  },
  data() {
    return {

    };
  },
  computed: {

  },
  methods: {
    displayConfirmDelete(job) {
      let component = this;
      let confirmObject = {
        title: `Занятие "${job.activity.name}" (${
          moment(job.date).format("dddd")
        }, ${job.start_time.substr(0, 5)}) будет удалено.`,
        content: "Продолжить?",
        okType: "danger",
        onOk() {
          component.$emit("deleteJob", job.id);
        },
      }
      this.$confirm(confirmObject);
    },
    openModalEdit(job) {
      this.$emit("editJob", job);
    }
  },
  created() {

  },
  beforeDestroy() {

  }
};
</script>

<style lang="sass">
.job-card
  padding: 10px
  border-radius: 4px
  display: flex
  flex-wrap: wrap

  .job-time
    flex: 0 0 95%

  .dropdown--hover
    display: none
    max-width: 0
    height: 20px
    svg
      transform: rotate(90deg)
      margin-top: 3px

  &:hover
    .dropdown--hover
      display: unset

  &__name
    flex: 0 0 100%
  &__specialist
    &-label
    &-name
</style>
