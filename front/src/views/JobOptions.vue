<template>
  <a-spin :spinning="loading">
    <div class="job-options">
      <div class="job-options__header">Планы занятий</div>

    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  components: {
  },
  name: "JobOptions",
  data() {
    return {
      loading: true,

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
    // async fetchUserData(){
    //   try {
    //     this.loading = true;
    //     let res = await this.$axios.get("/api/users/current");
    //     if (res.status === 200) {
    //       this.userData = res.data;
    //     } else if (res.status === 400) {
    //       this.$message.error("Ошибка при загрузке данных специалиста");
    //     } else {
    //       this.$message.error("Ошибка при загрузке данных специалиста");
    //     }
    //   } catch (e) {
    //     this.$message.error("Ошибка при загрузке данных специалиста");
    //   } finally {
    //     this.loading = false;
    //   }
    // },

    ...mapActions({
      // fetchAreas: "skills/fetchAreas",
    }),
  },
  computed: {
    ...mapGetters({
    //   areasFetched: "skills/getFetched",
    //   areas: "skills/getFilteredAreas",
    }),
  },
};
</script>

<style lang="sass">
  .job-options
    display: flex
    flex-direction: column
    height: 100%
    overflow: hidden
    &__header
      text-align: center
      font-size: 16px
      margin-bottom: 10px
</style>
