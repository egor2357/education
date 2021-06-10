<template>
  <TableSkill
    :readOnly="true"
    :specialists="true"
    :specialistSkills="specialistSkills"
    :specialistId="specialistId"
  />
</template>

<script>
import TableSkill from "@/components/TableSkill";
export default {
  name: "Skills",
  components: {
    TableSkill,
  },
  props: {
    specialistSkills: {
      type: Array,
    },
    specialistId: {
      type: [Number, String]
    }
  },
};
</script>

<style lang="sass">

</style>
