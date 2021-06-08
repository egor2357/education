<template>
  <div class="available-block">
    <div class="title">График присутствия специалистов</div>
    <div style="overflow: hidden; flex: 1">
      <Table :needUpdate="needUpdateTable" @successUpdate="needUpdateTable = false" @displayEdit="displayEdit" @onAddPeriod="onAddPeriod"/>
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
    },
    onAddPeriod(){
      this.modalAdding = true;
      this.modalEditableData = {};
      this.displayModal = true;
    }
  },
};
</script>

<style lang="sass">
.available-block
  display: flex
  flex-direction: column
  height: 100%
  overflow: hidden
  .title
    margin-bottom: 10px
    text-align: center
    font-size: 1rem
    font-weight: bold
</style>
