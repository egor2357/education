<template>
  <a-spin :spinning="loading">
    <div v-if="job">
      <JobDetails v-if="isEditable" :jobProp="job" />
      <JobReadOnly :job="job" v-else />
    </div>
    <div class="loader-full-page" v-else />
  </a-spin>
</template>

<script>
import JobReadOnly from "@/components/JobSchedule/JobReadOnly";
import JobDetails from "@/components/JobDetails";
import { mapGetters } from "vuex";
export default {
  components: {
    JobReadOnly,
    JobDetails,
  },
  name: "JobDetailWrapper",
  data() {
    return {
      loading: true,
      job: null,
    };
  },
  async created() {
    await this.fetchJob();
  },
  methods: {
    async fetchJob() {
      try {
        this.loading = true;
        let jobId = this.$route.params.id;
        let res = await this.$axios.get(`/api/jobs/${jobId}`);
        if (res.status === 200) {
          this.job = res.data;
          if (!this.isEditable) {
            this.job.option_files = this.job.job_files;
            this.job.skills = this.job.reports.map((item) => item.skill);
          }
        } else {
          this.$message.error("Произошла ошибка при загрузке занятия");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при загрузке занятия");
      } finally {
        this.loading = false;
      }
    },
  },
  computed: {
    ...mapGetters({
      userInfo: "auth/getUserInfo",
    }),
    isEditable() {
      return (this.job && this.userInfo.specialistId === this.job.specialist.id);
    },
  },
};
</script>

<style lang="sass">
.loader-full-page
  width: 100%
  height: 100%
</style>
