<template>
  <a-spin :spinning="loading">
    <div class="slills-structure">
      <div class="top-bar">
        <div class="top-bar__side-block left"></div>
        <div class="title">Структура навыков</div>
        <div class="top-bar__side-block right">
          <a-button icon="plus" type="secondary" @click="openModalAdd(1)">Добавить образовательную область
          </a-button>
        </div>
      </div>
      <div class="table-container">
        <skills-table
          :loading="loading"
          :tableData="areas"
          @onDeleteItem="displayConfirmDelete"
          @onEditItem="openModalEdit"
          @onAddItem="openModalAdd($event.type, $event.item)"
        />
      </div>
      <ModalSkills
        v-if="displayModal"
        :adding="modalAdding"
        :type="modalType"
        :editableData="modalEditableData"
        @close="displayModal = false"
        @closeSuccess="closeSuccess"
    />
    </div>
  </a-spin>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import ModalSkills from "@/components/Modals/ModalSkills";
import SkillsTable from "@/components/Skills/SkillsTable";
export default {
  name: "SkillsStructure",
  components: {
    ModalSkills,
    SkillsTable
  },
  data() {
    return {
      loading: false,
      displayModal: false,
      modalAdding: true,
      modalType: 0,
      modalEditableData: {},
    };
  },
  async created() {
    if (!this.fetched)
    {
      this.loading = true;
      await this.fetchAreas();
      this.loading = false;
    }
  },
  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas",
    }),
    deleteItem(payload){
      console.log(payload)
    },
    openModalAdd(type, item) {
      console.log(item)
      this.modalAdding = true;
      this.modalType = type;
      this.displayModal = true;
      if (type === 1) {
        this.modalEditableData.lastNumberArea = this.areas.length ? this.areas[this.areas.length - 1].number + 1 : 1;
      }
      if (type === 2) {
        this.modalEditableData.areaId = item.id;
        this.modalEditableData.lastNumberDirection = item.development_directions.length ? item.development_directions[item.development_directions.length-1].number + 1 : 1;
      }
      if (type === 3) {
        this.modalEditableData.directionId = item.id;
        this.modalEditableData.lastNumberSkill = item.skills.length ? item.skills[item.skills.length - 1].number + 1 : 1;
      }
    },
    openModalEdit(payload) {
      this.modalAdding = false;
      this.modalType = payload.type;
      this.modalEditableData = payload.item;
      this.displayModal = true;
    },
    async closeSuccess(){
      this.displayModal = false;
      this.loading = true;
      await this.fetchAreas();
      this.loading = false;
    },
    async deleteRecord(itemId, type) {
      let dispatchName = "";
      let successMessage = "";
      this.loading = true;
      if (type === 1) {
        dispatchName = "skills/deleteArea";
        successMessage = "Образовательная область успешно удалена";
      } else if (type === 2) {
        dispatchName = "skills/deleteDirection";
        successMessage = "Направление развития успешно удалено";
      } else if (type === 3) {
        dispatchName = "skills/deleteSkill";
        successMessage = "Навык успешно удален";
      } else {
        this.loading = false;
        return;
      }
      try {
        let res = await this.$store.dispatch(dispatchName, itemId);
        if (res.status === 204) {
          this.$message.success(successMessage);
          await this.closeSuccess();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.loading = false;
      }
    },
    displayConfirmDelete(payload) {
      let title = "";
      let content = "";
      let name = payload.name;
      let type = payload.type;
      if (type === 1) {
        title = `Вы действительно хотите удалить образовательную область "${name}"?`;
        content = "Будут удалены все связанные направления развития и навыки.";
      } else if (type === 2) {
        title = `Вы действительно хотите удалить направление развития "${name}"?`;
        content = "Будут удалены все связанные навыки.";
      } else if (type === 3) {
        title = `Вы действительно хотите удалить навык "${name}"?`;
        content = "";
      }
      let that = this;
      this.$confirm({
        title: title,
        content: content,
        okType: "danger",
        onOk() {
          that.deleteRecord(payload.id, type);
        },
      });
    },
  },
  computed: {
    ...mapGetters({
      areas: "skills/getAreas",
      fetched: "skills/getFetched"
    }),
  }
};
</script>

<style lang="sass">
  .slills-structure
    height: 100%
    display: flex
    flex-direction: column

    .top-bar
      display: flex
      margin-bottom: 10px

      .title
        font-size: 1rem
        text-align: center
        margin: 0 10px

    .top-bar__side-block
      flex: 1

      &.right
        text-align: right

    .table-container
      flex: 1
      overflow: hidden
</style>