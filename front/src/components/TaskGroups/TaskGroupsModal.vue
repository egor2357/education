<template>
  <a-modal
    :visible="true"
    :title="title"
    @cancel="handleCancel"
    class="ant-modal-task-groups"
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
            (isStaff || !field.staffOnly) &&
            (adding === true ||
              (field.name !== 'anonymously' && adding === false))
          "
        >
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
          <a-checkbox
            v-if="field.type === 'checkbox'"
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
import { mapGetters } from "vuex";
export default {
  name: "MissionsModal",
  props: {
    adding: {
      type: Boolean,
      default: true,
    },
    editableData: Object,
    questionsSelected: Boolean,
  },
  data() {
    return {
      form: {
        responsible_id: null,
        text: "",
        solution: "",
        deadline: null,
        anonymously: false,
      },
      title: "",
      layout: {
        labelCol: { span: 7 },
        wrapperCol: { span: 17 },
      },
      fields: [
        {
          name: "text",
          label: "Содержание",
          type: "textarea",
          validateStatus: "",
          help: "",
        },
        {
          name: "responsible_id",
          label: "Ответственный",
          type: "select",
          validateStatus: "",
          help: "",
          staffOnly: true,
        },
        {
          name: "deadline",
          label: "Срок исполнения",
          type: "date",
          validateStatus: "",
          help: "",
          staffOnly: true,
        },
        {
          name: "solution",
          label: "Решение",
          type: "textarea",
          validateStatus: "",
          help: "",
          staffOnly: true,
        },
        {
          name: "anonymously",
          label: "Анонимно",
          type: "checkbox",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        text: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите содержание",
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
              dispatchName = "taskGroups/addTaskGroup";
              successCode = 201;
              successMessage = "Интервенционная группа успешно добавлена";
            } else {
              dispatchName = "taskGroups/editTaskGroup";
              successCode = 200;
              successMessage = "Интервенционная группа успешно изменена";
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
        this.$refs.form !== undefined &&
        event.srcElement.localName !== "textarea"
      ) {
        this.handleOk();
      }
    },
  },
  created() {
    this.form.is_question = this.questionsSelected;
    if (this.adding) {
      this.title += "Добавление интервенционной группы";
    } else {
      this.title += "Изменение интервенционной группы";
      this.editableData.id ? (this.form.id = this.editableData.id) : "";
      if (this.editableData.responsible) {
        this.editableData.responsible.id
          ? (this.form.responsible_id = this.editableData.responsible.id)
          : null;
      }
      this.editableData.text
        ? (this.form.text = this.editableData.text)
        : (this.form.text = "");
      this.editableData.solution
        ? (this.form.solution = this.editableData.solution)
        : (this.form.solution = "");
      this.editableData.deadline
        ? (this.form.deadline = this.editableData.deadline)
        : (this.form.deadline = null);
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
      specialists: "specialists/getSpecialists",
    }),
    isStaff() {
      return this.$store.getters["auth/getUserInfo"].staff;
    },
  },
};
</script>

<style scoped></style>
