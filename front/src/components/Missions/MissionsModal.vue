<template>
  <a-modal
    :visible="true"
    :title="title"
    @cancel="handleCancel"
    class="ant-modal-missions"
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
          <a-select
            v-if="field.type === 'select'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
            allowClear
          >
            <a-select-option
              v-for="specialist in specialists"
              :key="specialist.id"
            >
              {{ specialist.__str__ }}
            </a-select-option>
          </a-select>
          <a-date-picker
            v-if="field.type === 'date'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
            type="date"
            format="DD.MM.YYYY"
          />
          <a-textarea
            v-if="field.type === 'textarea'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
          />
        </a-form-model-item>
      </template>
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
import {mapGetters} from "vuex";
export default {
  name: "MissionsModal",
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
        executor_id: null,
        controller_id: null,
        caption: "",
        comment: "",
        deadline: null,
      },
      title: "",
      layout: {
        labelCol: { span: 7 },
        wrapperCol: { span: 17 },
      },
      fields: [
        {
          name: "deadline",
          label: "Срок исполнения",
          type: "date",
          validateStatus: "",
          help: "",
        },
        {
          name: "executor_id",
          label: "Исполнитель",
          type: "select",
          validateStatus: "",
          help: "",
        },
        {
          name: "controller_id",
          label: "Контролёр",
          type: "select",
          validateStatus: "",
          help: "",
        },
        {
          name: "caption",
          label: "Наименование",
          type: "textarea",
          validateStatus: "",
          help: "",
        },
        {
          name: "comment",
          label: "Комментарий",
          type: "textarea",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        executor_id: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, выберите исполнителя",
          },
        ],
        caption: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите описание",
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
      if (!this.loadingButton) {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
            this.loadingButton = true;
            let dispatchName = "";
            let successCode = 0;
            let successMessage = "";

            if (this.adding) {
              dispatchName = "missions/addMission";
              successCode = 201;
              successMessage = "Задача успешно добавлена";
            } else {
              dispatchName = "missions/editMission";
              successCode = 200;
              successMessage = "Задача успешно изменен";
            }
            try {
              let res = await this.$store.dispatch(dispatchName, this.form);
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
    if (this.adding) {
      this.title += "Добавление задачи";
    } else {
      this.title += "Изменение задачи";
      this.editableData.id ? (this.form.id = this.editableData.id) : "";
      if (this.editableData.executor) {
        this.editableData.executor.id
          ? (this.form.executor_id = this.editableData.executor.id)
          : null;
      }
      if (this.editableData.controller) {
        this.editableData.controller.id
          ? (this.form.controller_id = this.editableData.controller.id)
          : null;
      }
      this.editableData.caption
        ? (this.form.caption = this.editableData.caption)
        : "";
      this.editableData.comment
        ? (this.form.comment = this.editableData.comment)
        : "";
      this.editableData.deadline
        ? (this.form.deadline = this.editableData.deadline)
        : null;
    }
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
  computed: {
    ...mapGetters({
      specialists: "specialists/getOnlySpecialists",
      admins: "specialists/getOnlyAdmins"
    }),
  },
};
</script>

<style scoped></style>
