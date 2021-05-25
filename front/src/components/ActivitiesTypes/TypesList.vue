<template>
  <div>
    <a-list
      :loading="loadingList || loading"
      item-layout="horizontal"
      :data-source="data"
      class="types-list"
    >
      <a-list-item slot="renderItem" slot-scope="item" style="height: 75px">
        <a
          slot="actions"
          @click="
            displayModal = true;
            modalEditableData = item;
            modalAdding = false;
          "
          >Изменить</a
        >
        <a slot="actions" @click="displayDelete(item)">Удалить</a>
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
    <div style="text-align: center; width: 100%; margin-top: 10px">
      <a-button
        icon="plus"
        type="primary"
        @click="
          displayModal = true;
          modalAdding = true;
        "
        >Добавить</a-button
      >
    </div>
    <ModalActivities
      v-if="displayModal"
      :adding="modalAdding"
      :editableData="modalEditableData"
      @close="displayModal = false"
      @closeSuccess="
        displayModal = false;
        $emit('needUpdate');
      "
    />
  </div>
</template>

<script>
import ModalActivities from "@/components/ActivitiesTypes/ModalActivities";
export default {
  name: "TypesList",
  props: {
    data: Array,
    loadingList: Boolean,
  },
  components: {
    ModalActivities,
  },
  data() {
    return {
      displayModal: false,
      modalAdding: true,
      modalEditableData: null,
      loading: false,
    };
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
