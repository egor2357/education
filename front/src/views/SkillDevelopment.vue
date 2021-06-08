<template>
  <a-spin :spinning="loading">
    <router-view
      :dateRangeInit="dateRange"
      @changeRange="changeRange($event)"/>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
// import consts from "@/const";
import moment from "moment";
// import deleteAxios from "@/middleware/deleteAxios";
// import post from "@/middleware/post";

export default {
  components: {
  },
  name: "SkillDevelopment",
  data() {
    return {
      loading: true,

      dateRange: [
        moment(new Date()).weekday(0),
        moment(new Date()).weekday(6)
      ],
    };
  },
  async created() {
    let fetches = []

    // if (!this.areasFetched) {
    //   fetches.push(this.fetchAreas());
    // }

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

  },
  methods: {
    ...mapActions({
      // fetchAreas: "skills/fetchAreas",
    }),
    changeRange(value){
      this.dateRange[0] = value[0].clone();
      this.dateRange[1] = value[1].clone();
    }

    // async fetchJobs(){
    //   try {
    //     this.loading = true;
    //     let firstQParameter = `date__gte=${this.momentDateArr[0].format("YYYY-MM-DD")}`;
    //     let secondQParameter = `date__lte=${this.momentDateArr[this.momentDateArr.length-1].format("YYYY-MM-DD")}`;
    //     let res = await this.$axios.get(`/api/jobs/?${firstQParameter}&${secondQParameter}`);
    //     if (res.status === 200) {
    //       this.jobs = res.data;
    //     } else {
    //       this.$message.error("Произошла ошибка при загрузке занятий");
    //     }
    //   } catch (e) {
    //     this.$message.error("Произошла ошибка при загрузке занятий");
    //   } finally {
    //     this.loading = false;
    //   }
    // },

  },
  computed: {
    ...mapGetters({
      // areasFetched: "skills/getFetched",
      // areas: "skills/getAreas",
    }),
  },

};
</script>

<style lang="sass">
</style>
