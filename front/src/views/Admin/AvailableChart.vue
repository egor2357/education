<template>
  <div class="specialist-presence">
    <div class="top-bar">
      <div class="top-bar__side-block left">
        <a-button type="link" icon="swap" @click="specialistMode = !specialistMode">Изменить представление</a-button>
      </div>
      <div class="title">График присутствия специалистов</div>
      <div class="top-bar__side-block right">
        <a-button icon="plus" @click="onAddPeriod">Добавить период</a-button>
      </div>
    </div>
    <div style="overflow: hidden; flex: 1">
      <Table
        :needUpdate="needUpdateTable"
        :specialistMode="specialistMode"
        @successUpdate="needUpdateTable = false"
        @displayEdit="displayEdit"
      />
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
      specialistMode: true
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
.specialist-presence
  display: flex
  flex-direction: column
  height: 100%
  overflow: hidden

  .top-bar
    display: flex
    margin-bottom: 10px
    line-height: 32px

    .title
      font-size: 1rem
      text-align: center
      margin: 0 10px

  .top-bar__side-block
    flex: 1

    &.right
      text-align: right
</style>
