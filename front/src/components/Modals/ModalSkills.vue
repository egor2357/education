<template>
  <a-modal
    :visible="true"
    @cancel="handleCancel"
    @ok="handleOk"
    okText="Сохранить"
    cancelText="Отмена"
    :title="title"
    v-if="type !== 0"
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
    };
  },
  methods: {
    handleCancel() {
      this.form.name = null;
      this.$emit("close");
    },
    handleOk() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          console.log("send");
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
