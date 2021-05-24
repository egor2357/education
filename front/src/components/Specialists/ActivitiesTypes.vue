<template>
  <div>
    <a-list
      :loading="loadingList || loading"
      item-layout="horizontal"
      :data-source="activities"
      class="types-list"
    >
      <a-list-item slot="renderItem" slot-scope="item, index" style="height: 75px">
        <div slot="actions">
          <a-checkbox style="margin-right: 15px;" v-model="checkboxes[index]" @change="checkboxChanged($event, index)"/>
          <a-radio-group v-model="radios[index]" :disabled="!checkboxes[index]" >
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
export default {
  name: "ActivitiesTypes",
  props: {
    activities: {
      type: Array,
    }
  },
  data() {
    return {
      displayModal: false,
      modalAdding: true,
      modalEditableData: null,
      loading: false,
      checkboxes: [],
      radios: [],
    };
  },
  created() {
    this.checkboxes = [];
    this.radios = [];
    this.activities.forEach(() => {
      this.checkboxes.push(null)
      this.radios.push(null)
    })
  },
  methods: {
    async deleteRecord(id) {
      this.loading = true;
      try {
        let res = await this.$store.dispatch("activities/deleteActivity", id);
        if (res.status === 204) {
          this.$message.success("Вид деятельности успешно удалён");
          this.$emit("needUpdate");
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.loading = false;
      }
    },
    displayDelete(item) {
      let that = this;
      this.$confirm({
        title: `Вы действительно хотите удалить образовательную область ${item.name}?`,
        content: `Будут удалены все связанные занятия.`,
        okType: "danger",
        onOk() {
          that.deleteRecord(item.id);
        },
      });
    },
    checkboxChanged(event, index) {
      if (event.target.checked === false) {
        this.radios[index] = null;
      }
    },
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
