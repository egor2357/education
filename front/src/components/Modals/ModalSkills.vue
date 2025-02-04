<template>
  <a-modal
    :visible="true"
    :title="title"
    v-if="type !== 0"
    @cancel="handleCancel"
    :width="800"
  >
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <a-form-model-item v-for="(field, index) in fields"
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
          type="textarea"
          allow-clear
        />
        <a-input-number
          v-else-if="field.type === 'number'"
          v-model="form[field.name]"
          @change="fieldChanged(field)"
          :min="0"
        />
      </a-form-model-item>
    </a-form-model>
    <template slot="footer">
      <a-button @click="handleCancel"> Отмена </a-button>
      <a-button
        type="primary"
        :loading="loadingButton"
        :disabled="loadingButton"
        @click="handleOk"
      >
        {{ loadingButton ? "Загрузка..." : "Сохранить" }}
      </a-button>
    </template>
  </a-modal>
</template>

<script>
export default {
  name: "ModalSkills",
  props: {
    adding: {
      type: Boolean,
      default: true,
    },
    type: {
      type: Number,
    },
    editableData: Object,
  },
  data() {
    return {
      form: {
        name: null,
        number: null,
      },
      title: "",
      layout: {
        labelCol: { span: 6 },
        wrapperCol: { span: 18 },
      },
      fields: [
        {
          name: "name",
          label: "Наименование",
          type: "text",
          validateStatus: "",
          help: "",
        },
        {
          name: "number",
          label: "Номер",
          type: "number",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        name: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите наименование",
          },
        ],
        number: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите номер",
          },
        ],
      },
      loadingButton: false,
    };
  },
  methods: {
    handleCancel() {
      this.form.name = null;
      this.form.number = null;
      this.$emit("close");
    },
    async handleOk() {
      if (!this.loadingButton) {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
            this.loadingButton = true;
            let dispatchName = "";
            let successMessage = "";
            let statusCode = 0;
            
            if (this.adding) {
              statusCode = 201;
              if (this.type === 1){
                dispatchName = "skills/addArea";
                successMessage = "Образовательная область успешно добавлена";
              } else if (this.type === 2) {
                dispatchName = "skills/addDirection";
                successMessage = "Направление развития успешно добавлено";
              } else if (this.type === 3) {
                dispatchName = "skills/addSkill";
                successMessage = "Навык успешно добавлен";
              } else if (this.type === 4) {
                dispatchName = "skills/addResult";
                successMessage = "Ожидаемый результат успешно добавлен";
              } else if (this.type === 5) {
                dispatchName = "skills/addExercise";
                successMessage = "Диагностическое упражнение успешно добавлено";
              }
            } else {
              statusCode = 200;
              if (this.type === 1){
                dispatchName = "skills/editArea";
                successMessage = "Образовательная область успешно изменена";
              } else if (this.type === 2) {
                dispatchName = "skills/editDirection";
              successMessage = "Направлние развития успешно изменено";
              } else if (this.type === 3) {
                dispatchName = "skills/editSkill";
                successMessage = "Навык успешно изменен";
              } else if (this.type === 4) {
                dispatchName = "skills/editResult";
                successMessage = "Ожидаемый результат успешно изменен";
              } else if (this.type === 5) {
                dispatchName = "skills/editExercise";
                successMessage = "Диагностическое упражнение успешно изменено";
              }
            }

            try {
              let res = await this.$store.dispatch(dispatchName, this.form);
              if (res.status === statusCode) {
                this.$message.success(successMessage);
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
      }
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
    let titles = {
      1: "образовательной области",
      2: "направления развития",
      3: "навыка",
      4: "ожидаемого результата",
      5: "диагностического упражнения"
    };
    if (this.adding) {
      this.title = "Добавление ";
      if (this.type === 2)
        this.form.area_id = this.editableData.parentId;
      else if (this.type === 3)
        this.form.direction_id = this.editableData.parentId;
      else if (this.type === 4)
        this.form.skill_id = this.editableData.parentId;
      else if (this.type === 5)
        this.form.result_id = this.editableData.parentId;

    } else {
      this.title += "Изменение ";
      this.form.id = this.editableData.id
      this.form.name = this.editableData.name;
    }
    this.form.number = this.editableData.number
    this.title += titles[this.type];
    document.addEventListener("keydown", this.keydown);
  },
  mounted() {
    this.$nextTick(() => {
      this.$refs["field0"][0].focus();
    });
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keydown);
  },
};
</script>

<style scoped></style>
