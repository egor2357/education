<template>
  <router-view
    :dateRangeInit="dateRange"/>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import moment from "moment";

export default {
  components: {
  },
  name: "SkillDevelopment",
  data() {
    return {
      dateRange: [
        moment(new Date()).weekday(0),
        moment(new Date()).weekday(6)
      ],
    };
  },
  async created() {
  },
  methods: {
  },
  computed: {
  },

};
</script>

<style lang="sass">
</style>
