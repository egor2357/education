<template>
  <a-modal
    :visible="true"
    @cancel="handleCancel"
    @ok="handleOk"
    okText="Сохранить"
    cancelText="Отмена"
    :title="title"
    v-if="type !== 0"
    @confirmLoading="loadingButton"
  >
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <a-form-model-item label="Название" key="name" prop="name">
        <a-input v-model="form.name" />
      </a-form-model-item>
    </a-form-model>
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
      },
      title: "",
      layout: {
        labelCol: { span: 5 },
        wrapperCol: { span: 19 },
      },
      rules: {
        name: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите название",
          },
        ],
      },
      loadingButton: false,
    };
  },
  methods: {
    handleCancel() {
      this.form.name = null;
      this.$emit("close");
    },
    async handleOk() {
      this.loadingButton = true;
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          let dispatchName = "";
          let successCode = 0;
          let successMessage = "";

          if (this.type === 1 && this.adding) {
            dispatchName = "skills/addArea";
            successCode = 201;
            successMessage = "Область образования успешно добавлена";
          } else if (this.type === 1 && !this.adding) {
            dispatchName = "skills/editArea";
            successCode = 200;
            successMessage = "Область образования успешно изменена";
          } else if (this.type === 2 && this.adding) {
            dispatchName = "skills/addDirection";
            successCode = 201;
            successMessage = "Направлние развития успешно добавлено";
          } else if (this.type === 2 && !this.adding) {
            dispatchName = "skills/editDirection";
            successCode = 200;
            successMessage = "Направлние развития успешно изменено";
          } else if (this.type === 3 && this.adding) {
            dispatchName = "skills/addSkill";
            successCode = 201;
            successMessage = "Навык успешно добавлен";
          } else if (this.type === 3 && !this.adding) {
            dispatchName = "skills/editSkill";
            successCode = 200;
            successMessage = "Навык успешно изменен";
          }

          try {
            let res = await this.$store.dispatch(dispatchName, this.form);
            if (res.status === successCode) {
              this.$message.success(successMessage);
              this.$emit("closeSuccess");
            } else if (res.status === 400) {
              this.$message.error("Проверьте введённые данные");
              // for (let key in res.data) {
              //   this.fields.forEach((field) => {
              //     if (field.name === key) {
              //       field.validateStatus = "error";
              //       field.help = res.data[key];
              //     }
              //   });
              // }
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
  },
  created() {
    if (this.adding) {
      this.title += "Добавление ";
    } else {
      this.title += "Изменение ";
      if (this.editableData.id) {
        this.form.id = this.editableData.id;
      }
      if (this.editableData.name) {
        this.form.name = this.editableData.name;
      }
    }
    if (this.type === 1) {
      this.title += "образовательной области";
    } else if (this.type === 2) {
      this.title += "направления развития";
    } else if (this.type === 3) {
      this.title += "навыка";
    }
  },
};
</script>

<style scoped></style>
