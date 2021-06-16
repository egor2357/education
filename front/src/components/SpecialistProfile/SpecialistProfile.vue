<template>
  <a-spin :spinning="loading">

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
    };
  },
  async created() {
    let fetches = []

    // if (!this.activitiesFetched) {
    //   fetches.push(this.fetchActivities());
    // }
    fetches.push(this.fetchJobs())

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

  },
  methods: {
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

</style>
