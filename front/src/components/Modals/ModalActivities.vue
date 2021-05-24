<template>
  <a-modal
    :visible="true"
    @cancel="handleCancel"
    @ok="handleOk"
    okText="Сохранить"
    cancelText="Отмена"
    :title="title"
    @confirmLoading="loadingButton"
    class="modal-activities"
  >
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <template v-for="(field, index) in fields">
        <a-form-model-item
          :prop="field.name"
          :label="field.label"
          :key="field.name"
          :validateStatus="field.validateStatus"
          :help="field.help"
        >
          <a-input
            v-if="field.type === 'text'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
          />
          <v-swatches
            v-else-if="field.type === 'color'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            shapes="circles"
            :swatches="swatches"
          />
        </a-form-model-item>
      </template>
    </a-form-model>
  </a-modal>
</template>

<script>
import VSwatches from "vue-swatches";
export default {
  name: "ModalActivities",
  components: {
    VSwatches,
  },
  props: {
    adding: {
      type: Boolean,
      default: true,
    },
    editableData: Object,
  },
  data() {
    return {
      form: {
        name: null,
        color: null,
      },
      title: "",
      layout: {
        labelCol: { span: 5 },
        wrapperCol: { span: 19 },
      },
      fields: [
        {
          name: "name",
          label: "Название",
          type: "text",
          validateStatus: "",
          help: "",
        },
        {
          name: "color",
          label: "Цвет",
          type: "color",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        name: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите название",
          },
        ],
        color: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите цвет",
          },
        ],
      },
      loadingButton: false,
      swatches: [
        "#5c0011",
        "#a8071a",
        "#cf1322",
        "#ff4d4f",
        "#ffa39e",
        "#610b00",
        "#ad2102",
        "#fa541c",
        "#ff9c6e",
        "#ffbb96",
        "#612500",
        "#ad4e00",
        "#fa8c16",
        "#ffc069",
        "#613400",
        "#ad6800",
        "#faad14",
        "#ffd666",
        "#614700",
        "#ad8b00",
        "#fadb14",
        "#fff566",
        "#254000",
        "#5b8c00",
        "#a0d911",
        "#d3f261",
        "#092b00",
        "#237804",
        "#52c41a",
        "#95de64",
        "#002329",
        "#006d75",
        "#08979c",
        "#36cfc9",
        "#002766",
        "#0050b3",
        "#1890ff",
        "#69c0ff",
        "#120338",
        "#391085",
        "#722ed1",
        "#b37feb",
      ],
    };
  },
  methods: {
    handleCancel() {
      this.form.name = null;
      this.form.color = null;
      this.$emit("close");
    },
    async handleOk() {
      this.loadingButton = true;
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          let dispatchName = "";
          let successCode = 0;
          let successMessage = "";

          if (this.adding) {
            dispatchName = "activities/addActivity";
            successCode = 201;
            successMessage = "Вид деятельности успешно добавлен";
          } else if (!this.adding) {
            dispatchName = "activities/editActivity";
            successCode = 200;
            successMessage = "Вид деятельности успешно изменен";
          }
          try {
            let res = await this.$store.dispatch(dispatchName, this.form);
            if (res.status === successCode) {
              this.$message.success(successMessage);
              this.$store.commit("activities/setActivitiesCheckboxes", {});
              this.$emit("closeSuccess");
            } else if (res.status === 400) {
              this.$message.error("Проверьте введённые данные");
              for (let key in res.data) {
                this.fields.forEach((field) => {
                  if (field.name === key) {
                    field.validateStatus = "error";
                    field.help = res.data[key];
                  }
                });
              }
            } else {
              this.$message.error("Произошла ошибка");
            }
          } catch (e) {
            this.$message.error("Произошла ошибка");
          } finally {
            this.loadingButton = false;
          }
        } else {
          return false;
        }
      });
    },
    fieldChanged(field) {
      field.validateStatus = "";
      field.help = "";
    },
    keydown(event) {
      if (
        event.type === "keydown" &&
        event.keyCode === 13 &&
        this.$refs.form !== undefined
      ) {
        this.handleOk();
      }
    },
  },
  created() {
    this.form.name = null;
    this.form.color = null;
    if (this.adding) {
      this.title += "Добавление вида деятельности";
    } else {
      this.title += "Изменение вида деятельности";
      this.editableData.id ? (this.form.id = this.editableData.id) : "";
      this.editableData.name ? (this.form.name = this.editableData.name) : "";
      this.editableData.color
        ? (this.form.color = this.editableData.color)
        : "";
    }
    document.addEventListener("keydown", this.keydown);
  },
  mounted() {
    this.$nextTick(() => {
      this.$refs["field0"][0].focus();
    });
  },
};
</script>

<style lang="sass">
.vue-swatches__wrapper
  width: 320px !important
.modal-activities
  .ant-modal-body
    padding-bottom: 0
</style>
