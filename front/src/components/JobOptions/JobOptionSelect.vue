<template>
  <a-modal
    width="1000px"
    :visible="true"
    :title="Выбор варианта проведения занятия">

  </a-modal>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "JobOptionSelect",
  props: {
    activity: {
      type: Object,
      default: null,
    }
  },
  data() {
    return {
      options: [],
    };
  },
  computed: {
  },
  methods: {
    async fetchOptions(){
      try {
        this.loading = true;
        let res = await this.$axios.get("/api/options");
        if (res.status === 200) {
          this.options = res.data;
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
  },
  async created() {
    let fetches = [];

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
  },
};
</script>

<style lang="sass">


</style>
