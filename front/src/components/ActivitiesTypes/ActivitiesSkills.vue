<template>
  <div class="table-skills-activities">
    <TableSkill
      :readOnly="true"
      :activities="true"
      :activitiesList="activities"
      @changeLink="changeLink"
      :tableLoadingActivity="tableLoading"
    />
  </div>
</template>

<script>
import TableSkill from "@/components/TableSkill";
import { mapGetters } from "vuex";
export default {
  name: "AcitivitiesSkills",
  components: {
    TableSkill,
  },
  data() {
    return {
      tableLoading: false,
    };
  },
  computed: {
    ...mapGetters({
      activities: "activities/getActivities",
    }),
  },
  methods: {
    changeLink(data) {
      this.tableLoading = true;
      if (data.value === true) {
        this.addLink(data);
      } else {
        this.deleteLink(data);
      }
    },
    async deleteLink(data) {
      try {
        let res = await this.$store.dispatch(
          "activities/deleteLinkSkill",
          data
        );
        if (res.status === 200) {
          this.$message.success("Успешно");
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.tableLoading = false;
      }
    },
    async addLink(data) {
      try {
        let res = await this.$store.dispatch("activities/addLinkSkill", data);
        if (res.status === 200) {
          this.$message.success("Успешно");
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.tableLoading = false;
      }
    },
  },
};
</script>

<style lang="sass">
.table-skills-activities
  @media (max-height: 1300px)
    max-height: 70vh
    overflow: hidden
  @media (max-height: 800px)
    max-height: 60vh
  .ant-table-body
    max-height: calc(-485px + 100vh) !important
    margin-bottom: 1px
</style>
