<template>
  <div class="job-option">
    {{ option.topic }}
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "JobOption",
  props: {
    option: {
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

  },
  created() {

  },
  beforeDestroy() {

  }
};
</script>

<style lang="sass">
.job-option
</style>
