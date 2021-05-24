<template>
  <div>
    <a-list
      :loading="loading"
      item-layout="horizontal"
      :data-source="activities"
      class="types-list"
    >
      <a-list-item
        slot="renderItem"
        slot-scope="item, index"
        style="height: 75px"
      >
        <div slot="actions">
          <a-checkbox
            style="margin-right: 15px"
            v-model="checkboxes[index]"
            @change="checkboxChanged($event, index, item)"
          />
          <a-radio-group
            v-model="radios[index]"
            :disabled="!checkboxes[index]"
            @change="radioChanged(index, item)"
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
import { mapActions } from "vuex";
export default {
  name: "ActivitiesTypes",
  props: {
    activities: {
      type: Array,
    },
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
      checkboxes: [],
      radios: [],
      specialtyLinks: [],
    };
  },
  created() {
    this.prepareData();
  },
  methods: {
    async checkboxChanged(event, index, item) {
      if (event.target.checked === false) {
        this.radios[index] = true;
        let res = await this.deleteActivity(this.specialtyLinks[index]);
        if (res.status === 204) {
          this.$message.success(
            "Вид деятельности у специалиста успешно удалён"
          );
        } else {
          this.$message.error("Произошла ошибка");
        }
      } else {
        if (this.specialtyLinks[index] === null) {
          let res = await this.addActivity({
            activity_id: item.id,
            specialist_id: this.specialistId,
            is_main: this.radios[index],
          });
          if (res.status === 201) {
            this.$message.success(
              "Вид деятельности у специалиста успешно добавлен"
            );
            this.specialtyLinks[index] = res.data.id;
          } else {
            this.$message.error("Произошла ошибка");
          }
        }
      }
    },
    async radioChanged(index, item) {
      if (this.specialtyLinks[index] !== null) {
        let res = await this.editActivity({
          id: this.specialtyLinks[index],
          activity_id: item.id,
          specialist_id: this.specialistId,
          is_main: this.radios[index],
        });
        if (res.status === 200) {
          this.$message.success(
            "Вид деятельности у специалиста успешно изменён"
          );
        } else {
          this.$message.error("Произошла ошибка");
        }
      }
    },
    prepareData() {
      this.checkboxes = [];
      this.radios = [];
      let activityInUser = false;
      let activityIsMain = true;
      let specialtyLink = null;
      this.activities.forEach((activity) => {
        activityInUser = false;
        activityIsMain = true;
        specialtyLink = null;
        for (let userActivity of this.userActivities) {
          if (activity.id === userActivity.activity.id) {
            activityInUser = true;
            activityIsMain = userActivity.is_main;
            specialtyLink = userActivity.id;
            break;
          }
        }
        this.checkboxes.push(activityInUser);
        this.radios.push(activityIsMain);
        this.specialtyLinks.push(specialtyLink);
      });
    },
    ...mapActions({
      addActivity: "specialists/addSpecialistActivity",
      editActivity: "specialists/editSpecialistActivity",
      deleteActivity: "specialists/deleteSpecialistActivity",
    }),
  },
};
</script>

<style lang="sass">
.types-list
  padding-right: calc(50% - 400px)
  padding-left: calc(50% - 400px)
  overflow-y: auto
  @media (max-height: 1300px)
    max-height: 70vh
  @media (max-height: 800px)
    max-height: 60vh
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
