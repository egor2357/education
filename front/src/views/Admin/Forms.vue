<template>
  <div class="forms">
    <div class="top-bar">
      <div class="placeholder"></div>
      <div class="title">Формы и способы проведения занятий</div>
      <div class="add-button">
        <a-button
          type="secondary"
          icon="plus"
          @click="
            displayModal = true;
            modalEditableData = {};
            modalAdding = true;
            modalType = 1;
          "
          >Добавить форму</a-button>
      </div>
    </div>

    <div class="block">
      <FormMethods
        class="block-collapse"
        @needUpdate="fetchForms()"
        @displayAdd="displayAdd"
        @displayEdit="displayEdit"
      />
    </div>
    <ModalForms
      v-if="displayModal"
      :adding="modalAdding"
      :editableData="modalEditableData"
      :type="modalType"
      @closeSuccess="
        displayModal = false;
        fetchForms();
      "
      @close="displayModal = false"
    />
  </div>
</template>

<script>
import FormMethods from "@/components/Forms/FormMethods";
import ModalForms from "@/components/Forms/ModalForms";
import { mapActions } from "vuex";
export default {
  name: "Forms",
  components: {
    FormMethods,
    ModalForms,
  },
  data() {
    return {
      modalAdding: true,
      displayModal: false,
      modalEditableData: {},
      modalType: 1,
    };
  },
  created() {
    this.fetchForms();
  },
  methods: {
    ...mapActions({
      fetchForms: "forms/fetchForms",
    }),
    displayAdd(type, form_id) {
      this.displayModal = true;
      this.modalAdding = true;
      this.modalType = type;
      this.modalEditableData.form_id = form_id;
    },
    displayEdit(type, data) {
      this.displayModal = true;
      this.modalAdding = false;
      this.modalType = type;
      this.modalEditableData = data;
    },
  },
};
</script>

<style lang="sass">
.forms
  height: 100%
  display: flex
  flex-direction: column
  .top-bar
    display: flex
    margin-bottom: 10px
    line-height: 32px

    .placeholder
      flex: 1

    .add-button
      flex: 1
      display: flex
      justify-content: flex-end

  .title
    text-align: center
    font-size: 1rem
    margin: 0 10px
  .block
    overflow-y: auto
    flex: 1
    .block-collapse
      margin-right: 250px
      margin-left: 250px
      @media (max-width: 1400px)
        margin-right: 50px
        margin-left: 50px
      @media (max-width: 900px)
        margin-right: 0
        margin-left: 0
</style>