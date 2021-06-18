<template>
  <div class="job"
    @click="goToJob(job)"
    :style="{
      'background-color': `${job.activity.color}10`,
      border: `1px solid ${job.activity.color}99`,
    }">
    <div class="job__time">{{ job.start_time.substr(0, 5) }}</div>

    <a-dropdown :trigger="['click']"
      placement="bottomLeft"
      class="dropdown--hover">

      <a-icon class="icon-button" type="dash"
        @click.stop></a-icon>
      <a-menu slot="overlay">
        <a-menu-item key="1" @click="openModalEdit(job)">
          Изменить
        </a-menu-item>
        <a-menu-item key="2"
          @click="displayConfirmDelete(job)">
          <span> Удалить </span>
        </a-menu-item>
      </a-menu>
    </a-dropdown>

    <div class="job__activity">
      <div class="job__activity-name">
        {{ job.activity.name }}
      </div>
    </div>
    <div class="job__specialist" v-if="job.specialist">
      <div class="job__specialist-label">Специалист:</div>
      <div class="job__specialist-name">{{ job.specialist.__str__ }}</div>
    </div>
    <div class="job__specialist_empty" v-else>
      <a-icon type="info-circle"></a-icon>
      Специалист не назначен
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
    },
    goToJob(job){
      if (job){
        this.$router.push({name: "JobDetails", params: {id: job.id}});
      }
    }
  },
  created() {

  },
  beforeDestroy() {

  }
};
</script>

<style lang="sass">
.job
  padding: 5px 10px
  border-radius: 4px
  display: flex
  flex-wrap: wrap
  transition: box-shadow ease-out .3s
  &:hover
    cursor: pointer
    box-shadow: 0 0 2px 1px rgba(0,0,0,.15)

  &__time
    flex: 0 0 95%
    color: #0b0b0b

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

  &__activity
    &-label
    &-name
      flex: 0 0 100%
      color: #0b0b0b

  &__specialist
    &-label
    &-name
      color: #0b0b0b
    &_empty
      color: #ff2222
</style>
