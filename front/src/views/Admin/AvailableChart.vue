<template>
  <div class="available-block">
    <div class="title">
      <span class="text">График присутствия специалистов</span>
      <a-button
        class="button"
        @click="
          modalAdding = true;
          modalEditableData = {};
          displayModal = true;
        "
        >Добавить период</a-button
      >
    </div>
    <div>
      <Table :needUpdate="needUpdateTable" @successUpdate="needUpdateTable = false" @displayEdit="displayEdit" />
    </div>
    <ModalPeriod
      v-if="displayModal"
      :editableData="modalEditableData"
      :adding="modalAdding"
      @close="displayModal = false"
      @closeSuccess="displayModal = false; needUpdateTable = true;"
    />
  </div>
</template>

<script>
import Table from "@/components/AvailableChart/Table";
import ModalPeriod from "@/components/AvailableChart/ModalPeriod";
export default {
  name: "AvailableChart",
  components: {
    Table,
    ModalPeriod,
  },
  data() {
    return {
      displayModal: false,
      modalEditableData: {},
      modalAdding: true,
      needUpdateTable: false,
    };
  },
  methods: {
    displayEdit(item) {
      this.modalEditableData = item;
      this.modalAdding = false;
      this.displayModal = true;
    }
  },
};
</script>

<style lang="sass">
.available-block
  display: flex
  flex-direction: column
  .title
    margin-bottom: 10px
    display: flex
    .text
      flex: 1
      text-align: center
      font-size: 1rem
      font-weight: bold
</style>
