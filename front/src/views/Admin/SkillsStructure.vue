<template>
  <a-spin :spinning="loading">
    <div class="skills-structure">
      <div class="top-bar">
        <div class="top-bar__side-block left">
          <a-input v-model.trim="searchText" placeholder="Поиск" class="search-input" allow-clear/>
        </div>
        <div class="title">Структура навыков</div>
        <div class="top-bar__side-block right">
          <a-button icon="plus" type="secondary" @click="openModalAdd(1)" :disabled="showByDate"
            >Добавить образовательную область
          </a-button>
        </div>
      </div>
      <div class="table-container">
        <skills-table
          ref="table"
          :loading="loading"
          :areas="areas"
          :searchText="searchText"
          :disableActions="showByDate"
          @onDeleteItem="displayConfirmDelete"
          @onEditItem="openModalEdit"
          @onAddItem="openModalAdd($event.type, $event.item)"
        />
      </div>
      <div class="skills-structure__params-container">
        <div class="skills-structure__param">
          <a-checkbox v-model="showDeleted" @change="refetchAreas">Показывать удаленные элементы</a-checkbox>
        </div>
        <div class="skills-structure__param">
          <a-checkbox v-model="showByDate" @change="showByDateHandle">Показывать данные, актуальные на</a-checkbox>
          <a-date-picker
            v-model="calendarDate"
            type="date"
            format="DD.MM.YYYY"
            :open="calendarShown"
            @change="changeCalendarDate"
            @openChange="handleCalendarOpenChange"
          />
        </div>
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
      modalEditableData: {
        id: null,
        parentId: null,
        name: '',
        number: null
      },
      showDeleted: false,
      showByDate: false,
      calendarDate: null,
      calendarShown: false,
      searchText: ''
    };
  },
  async created() {
    this.loading = true;
    await this.fetchAreas({deletedState: false, byDate: null});
    this.loading = false;
    this.$refs.table.initShownAreas();
  },
  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas"
    }),
    openModalAdd(type, item) {  // добавление нового элемента, здесь в item приходит родительский элемнет, id=null, parentId получаем из item.id, name='', number вычисляем из item.nodes (без фильтрации по имени)
      this.modalAdding = true;
      this.modalType = type;
      this.displayModal = true;
      this.modalEditableData.id = null;
      this.modalEditableData.name = '';
      let list; 
      if (type === 1) // добавляется образовательная область
      {
        this.modalEditableData.parentId = null;
        list = this.areas.filter(el => !el.deleted);
      }
      else // добавляется другой элемент (направление развития и т.д.)
      {
        this.modalEditableData.parentId = item.id;
        list = item.nodes.filter(el => !el.deleted);
      }
      if (list.length)
        this.modalEditableData.number = list[list.length - 1].number + 1;
      else
        this.modalEditableData.number = 1;
    },
    openModalEdit(payload) { // изменение элемнта, здесь в payload.item приходит изменяемый элемент
      this.modalAdding = false;
      this.modalType = payload.type;
      this.modalEditableData = payload.item;
      this.displayModal = true;
    },
    async closeSuccess() {
      this.displayModal = false;
      this.refetchAreas();
    },
    async deleteRecord(itemId, type, forever) {      
      let dispatchName = "";
      let successMessage = "";
      this.loading = true;
      if (type === 1) {
        dispatchName = "skills/deleteArea" + (forever ? 'Forever' : '');
        successMessage = "Образовательная область успешно удалена";
      } else if (type === 2) {
        dispatchName = "skills/deleteDirection" + (forever ? 'Forever' : '');
        successMessage = "Направление развития успешно удалено";
      } else if (type === 3) {
        dispatchName = "skills/deleteSkill" + (forever ? 'Forever' : '');
        successMessage = "Навык успешно удален";
      } else if (type === 4) {
        dispatchName = "skills/deleteResult" + (forever ? 'Forever' : '');
        successMessage = "Ожидаемый результат успешно удален";
      } else if (type === 5) {
        dispatchName = "skills/deleteExercise" + (forever ? 'Forever' : '');
        successMessage = "Упражнение успешно удалено";
      } else {
        this.loading = false;
        return;
      }
      try {        
        let res = await this.$store.dispatch(dispatchName, itemId);
        console.log(res.status)      
        if (res.status === 204 || res.status === 200 ) {
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
        content = "Будут удалены все связанные направления развития, навыки, ожидаемые результаты и диагностические упражнения.";
      } else if (type === 2) {
        title = `Вы действительно хотите удалить направление развития "${name}"?`;
        content = "Будут удалены все связанные навыки, ожидаемые результаты и диагностические упражнения.";
      } else if (type === 3) {
        title = `Вы действительно хотите удалить навык "${name}"?`;
        content = "Будут удалены все связанные ожидаемые результаты и диагностические упражнения.";
      } else if (type === 4) {
        title = `Вы действительно хотите удалить ожидаемый результат "${name}"?`;
        content = "Будут удалены все связанные диагностические упражнения.";
      } else if (type === 5) {
        title = `Вы действительно хотите удалить диагностическое упражнение "${name}"?`;
        content = "";
      }
      let that = this;
      this.$confirm({
        title: title,
        content: content,
        okType: "danger",
        width: 800,
        onOk() {
          that.deleteRecord(payload.id, type, payload.forever);
        }
      });
    },
    async refetchAreas() {
      this.loading = true;
      await this.fetchAreas({deletedState: this.showDeleted, byDate: this.calendarDate ? this.calendarDate.format('YYYY-MM-DD') : null});
      this.loading = false;
    },
    handleCalendarOpenChange(status){
      console.log('handleCalendarOpenChange1')
      this.calendarShown = status;
      
      console.log(status)
      console.log(this.showByDate)
      if (status)
      this.showByDate = true;
      if (!status && !this.calendarDate && this.showByDate)
        this.showByDate = false;      
      console.log('handleCalendarOpenChange2')
    },
    showByDateHandle()
    {
      console.log('showByDateHandle1')
      this.calendarShown = this.showByDate;
      if (!this.showByDate)
      {
        this.calendarDate = null;
        this.refetchAreas();
      }
      console.log('showByDateHandle2')
    },
    changeCalendarDate()
    {
      if (!this.showByDate)
        this.showByDate = true;
      if (!this.calendarDate)
        this.showByDate = false;
      this.refetchAreas();
    }
  },
  computed: {
    ...mapGetters({
      areas: "skills/getAreas",
      fetched: "skills/getFetched"
    })
  }
};
</script>

<style lang="sass">
.skills-structure
  height: 100%
  display: flex
  flex-direction: column

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

    &.left
      .search-input
        width: 300px

    &.right
      text-align: right

  .table-container
    flex: 1
    overflow: hidden

  &__params-container
    margin-top: 20px
</style>
