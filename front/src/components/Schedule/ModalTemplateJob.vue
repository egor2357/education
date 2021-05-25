<template>
  <a-modal
    :visible="true"
    @cancel="handleCancel"
    @ok="handleOk"
    okText="Сохранить"
    cancelText="Отмена"
    :title="title"
    @confirmLoading="loadingButton"
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
            v-if="field.type === 'time'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
            type="time"
            style="width: 90px"
          />
          <a-select
            v-if="field.type === 'select'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
          >
            <template v-if="field.name === 'activity_id'">
              <a-select-option
                v-for="activity in activities"
                :key="activity.id"
              >
                {{ activity.name }}
              </a-select-option>
            </template>
            <template v-if="field.name === 'day'">
              <a-select-option v-for="(day, index) in daysOfWeek" :key="index">
                {{ day.long }}
              </a-select-option>
            </template>
          </a-select>
        </a-form-model-item>
      </template>
    </a-form-model>
  </a-modal>
</template>

<script>
import consts from "@/const";
export default {
  name: "ModalTemplateJob",
  props: {
    adding: {
      type: Boolean,
      default: true,
    },
    activities: {
      type: Array,
    },
    editableData: Object,
  },
  data() {
    return {
      daysOfWeek: consts.daysOfWeek,
      form: {
        day: null,
        activity_id: null,
        start_time: null,
      },
      title: "",
      layout: {
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
      },
      fields: [
        {
          name: "day",
          label: "День недели",
          type: "select",
          validateStatus: "",
          help: "",
        },
        {
          name: "activity_id",
          label: "Вид деятельности",
          type: "select",
          validateStatus: "",
          help: "",
        },
        {
          name: "start_time",
          label: "Время",
          type: "time",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        day: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, выберите день недели",
          },
        ],
        activity_id: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, выберите вид деятельности",
          },
        ],
        start_time: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите время",
          },
        ],
      },
      loadingButton: false,
    };
  },
  methods: {
    handleCancel() {
      this.form.day = null;
      this.form.activity_id = null;
      this.form.start_time = null;
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
            dispatchName = "schedule/addJob";
            successCode = 201;
            successMessage = "Занятие успешно добавлено";
          } else if (!this.adding) {
            dispatchName = "schedule/editJob";
            successCode = 200;
            successMessage = "Занятие успешно изменено";
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
    this.form.day = null;
    this.form.activity_id = null;
    this.form.start_time = null;
    if (this.adding) {
      this.title += "Добавление занятия";
    } else {
      this.title += "Изменение занятия";
      this.editableData.id ? (this.form.id = this.editableData.id) : "";
      if (this.editableData.day || this.editableData.day === 0)
        this.form.day = this.editableData.day;
      this.editableData.activity
        ? (this.form.activity_id = this.editableData.activity.id)
        : "";
      this.editableData.start_time
        ? (this.form.start_time = this.editableData.start_time)
        : "";
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
  }
};
</script>

<style lang="sass"></style>
