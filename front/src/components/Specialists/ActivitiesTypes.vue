<template>
  <div class="activities-types-container">
    <a-list
      :loading="loading"
      item-layout="horizontal"
      :data-source="handledActivities"
      class="activities-types-container__list"
    >
      <a-list-item
        slot="renderItem"
        slot-scope="item"
        style="min-height: 75px"
      >
        <div slot="actions">
          <a-checkbox
            style="margin-right: 15px"
            :checked="item.isForUser"
            @change="checkboxChanged($event, item)"
          />
          <a-radio-group
            :value="item.isMain"
            :disabled="!item.linkId"
            @change="radioChanged(item)"
          >
            <a-radio-button :value="true"> Основной </a-radio-button>
            <a-radio-button :value="false"> Дополнительный </a-radio-button>
          </a-radio-group>
        </div>
        <a-list-item-meta style="width: 50px">
          <div
            class="type-color"
            slot="avatar"
            :style="{ 'background-color': item.color }"
          ></div>
        </a-list-item-meta>
        <span class="type-label">{{ item.name }}</span>
      </a-list-item>
    </a-list>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  name: "ActivitiesTypes",
  props: {
    userActivities: {
      type: Array,
    },
    specialistId: [Number, String],
  },
  data() {
    return {
      displayModal: false,
      modalAdding: true,
      modalEditableData: null,
      loading: false,
    };
  },
  computed: {
    ...mapGetters({
      activities: "activities/getActivities",
      activitiesFetched: "activities/getFetched"
    }),
    handledUserActivities(){
      let res = {};
      this.userActivities.forEach(activity => res[activity.activity.id] = {linkId: activity.id, isMain: activity.is_main});
      return res;
    },
    handledActivities(){
      return this.activities.map((activity) => {
        return {
          id: activity.id,
          name: activity.name,
          color: activity.color,
          isForUser: !!this.handledUserActivities[activity.id],
          isMain: !!this.handledUserActivities[activity.id] && this.handledUserActivities[activity.id].isMain,
          linkId: !!this.handledUserActivities[activity.id] && this.handledUserActivities[activity.id].linkId
        }
      });
    }
  },
  async created() {
    if (!this.activitiesFetched)
    {
      this.loading = true;
      await this.fetchActivities();
      this.loading = false;
    }
  },
  methods: {
    async checkboxChanged(event, item) {
      this.loading = true;
      if (event.target.checked === false) {
        let res = await this.deleteActivity({linkId: item.linkId, specialistId: this.specialistId});
        if (res.status === 204) {
          this.$message.success(
            "Вид деятельности у специалиста успешно удалён"
          );
        } else {
          this.$message.error("Произошла ошибка");
        }
      } else {
        let res = await this.addActivity({
          activity_id: item.id,
          specialist_id: this.specialistId,
          is_main: true,
        });
        if (res.status === 201) {
          this.$message.success(
            "Вид деятельности у специалиста успешно добавлен"
          );
        } else {
          this.$message.error("Произошла ошибка");
        }
      }
      this.loading = false;
    },
    async radioChanged(item) {
      this.loading = true;
      let res = await this.editActivity({
        linkId: item.linkId,
        specialistId: this.specialistId,
        isMain: !item.isMain,
      });
      this.loading = false;
      if (res.status === 200) {
        this.$message.success(
          "Вид деятельности у специалиста успешно изменён"
        );
      } else {
        this.$message.error("Произошла ошибка");
      }

    },
    ...mapActions({
      fetchActivities: "activities/fetchActivities",
      addActivity: "specialists/addSpecialistActivity",
      editActivity: "specialists/editSpecialistActivity",
      deleteActivity: "specialists/deleteSpecialistActivity",
    }),
  },
};
</script>

<style lang="sass">
.activities-types-container
  height: 100%
  overflow: auto

  &__list
    max-width: 900px
    margin: 0 auto

  .type-color
    width: 32px
    height: 32px
    -webkit-border-radius: 16px
    -moz-border-radius: 16px
    border-radius: 16px
  .type-label
    width: 100%
    font-size: 1.1rem
</style>
