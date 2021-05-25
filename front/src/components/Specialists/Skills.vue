<template>
  <div class="table-skills-specialists">
    <TableSkill
      :readOnly="true"
      :specialists="true"
      :specialistSkills="specialistSkills"
      :specialistId="specialistId"
    />
  </div>
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
.table-skills-specialists
  .ant-table-body
    max-height: calc(-350px + 100vh) !important
    margin-bottom: 1px
</style>
