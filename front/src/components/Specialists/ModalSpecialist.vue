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
          v-if="
            field.name !== 'password' || adding || (!adding && displayPassword)
          "
        >
          <a-input
            v-if="field.type === 'text'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
          />
        </a-form-model-item>
      </template>
      <a-form-model-item v-if="adding === false && !displayPassword">
        <a-button
          @click="
            form.password = null;
            displayPassword = true;
          "
          >Сменить пароль</a-button
        >
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
export default {
  name: "ModalActivities",
  props: {
    adding: {
      type: Boolean,
      default: true,
    },
    editableData: Object,
    staffSelected: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      form: {
        name: null,
        surname: null,
        patronymic: null,
        username: null,
        password: null,
      },
      title: "",
      layout: {
        labelCol: { span: 5 },
        wrapperCol: { span: 19 },
      },
      fields: [
        {
          name: "surname",
          label: "Фамилия",
          type: "text",
          validateStatus: "",
          help: "",
        },
        {
          name: "name",
          label: "Имя",
          type: "text",
          validateStatus: "",
          help: "",
        },
        {
          name: "patronymic",
          label: "Отчество",
          type: "text",
          validateStatus: "",
          help: "",
        },
        {
          name: "username",
          label: "Логин",
          type: "text",
          validateStatus: "",
          help: "",
        },
        {
          name: "password",
          label: "Пароль",
          type: "text",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        name: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите имя",
          },
        ],
        surname: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите фамилию",
          },
        ],
        username: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите логин",
          },
        ],
        password: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите пароль",
          },
        ],
      },
      loadingButton: false,
      displayPassword: false,
    };
  },
  methods: {
    handleCancel() {
      this.clearFields();
      this.$emit("close");
    },
    async handleOk() {
      this.loadingButton = true;
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          let dispatchName = "";
          let successCode = 0;
          let successMessage = "";
          let dataForSend = JSON.parse(JSON.stringify(this.form));
          if (this.adding) {
            dispatchName = "specialists/addSpecialist";
            successCode = 201;
            this.staffSelected
              ? (successMessage = "Администратор успешно добавлен")
              : (successMessage = "Специалист успешно добавлен");
          } else if (!this.adding) {
            dispatchName = "specialists/editSpecialist";
            successCode = 200;
            this.staffSelected
              ? (successMessage = "Администратор успешно изменён")
              : (successMessage = "Специалист успешно изменён");
            if (!this.displayPassword) {
              delete dataForSend["password"];
            }
          }
          try {
            let res = await this.$store.dispatch(dispatchName, dataForSend);
            if (res.status === successCode) {
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
    clearFields() {
      this.form = {
        name: null,
        subname: null,
        patronymic: null,
        username: null,
        password: null,
      };
    },
    fillFields(data) {
      data.id ? (this.form.id = data.id) : "";
      data.name ? (this.form.name = data.name) : "";
      data.surname ? (this.form.surname = data.surname) : "";
      data.patronymic ? (this.form.patronymic = data.patronymic) : "";
      data.user.username ? (this.form.username = data.user.username) : "";
    },
  },
  created() {
    this.clearFields();
    if (this.adding) {
      this.staffSelected
        ? (this.title += "Добавление администратора")
        : (this.title += "Добавление специалиста");
    } else {
      this.staffSelected
        ? (this.title += "Изменение администратора")
        : (this.title += "Изменение специалиста");
      this.fillFields(this.editableData);
    }
    this.staffSelected
      ? (this.form.is_staff = true)
      : (this.form.is_staff = false);
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

<style lang="sass"></style>
