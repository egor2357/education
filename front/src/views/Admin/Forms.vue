<template>
  <div class="forms">
    <div class="title">Формы и способы проведения занятий</div>
    <FormMethods
      class="block"
      @needUpdate="fetchForms()"
      @displayAdd="displayAdd"
      @displayEdit="displayEdit"
    />
    <div class="add-button">
      <a-button
        type="primary"
        icon="plus"
        @click="
          displayModal = true;
          modalEditableData = null;
          modalAdding = true;
        "
        >Добавить форму</a-button
      >
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
    displayAdd(type, formId) {
      this.displayModal = true;
      this.modalAdding = true;
      this.modalType = type;
      this.modalEditableData.form_id = formId;
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
  .title
    text-align: center
    font-size: 1rem
    font-weight: bold
    margin-bottom: 20px
  .block
    overflow-y: auto
    margin-right: 250px
    margin-left: 250px
    @media (max-width: 1400px)
      margin-right: 50px
      margin-left: 50px
    @media (max-width: 900px)
      margin-right: 0
      margin-left: 0
    @media (max-height: 1300px)
      max-height: 70vh
    @media (max-height: 800px)
      max-height: 60vh
  .add-button
    margin-top: 10px
    text-align: center
</style>
