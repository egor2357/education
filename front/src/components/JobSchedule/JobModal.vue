<template>
  <a-modal
    okText="Сохранить"
    cancelText="Отмена"
    :visible="true"
    :title="title"
    @cancel="closeModal(false)"
    @ok="handleOk"
    @confirmLoading="loadingButton">
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">

      <a-form-model-item prop="date" label="Дата" key="date"
        :validateStatus="fields['date'].validateStatus" :help="fields['date'].help">
        <a-date-picker
          v-model="form.date"
          type="date"
          placeholder="Выберите дату"
          format="DD.MM.YYYY"
          style="width: 100%;"
          @change="fieldChanged('date')"
        />
      </a-form-model-item>

      <a-form-model-item prop="activity_id" label="Вид деятельности" key="activity_id"
        :validateStatus="fields['activity_id'].validateStatus" :help="fields['activity_id'].help">
        <a-select v-model="form.activity_id"
          @change="form.specialist_id=null; fieldChanged('activity_id')">
          <a-select-option v-for="activity in activities" :key="activity.id">
            {{ activity.name }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item prop="specialist_id" label="Специалист" key="specialist_id"
        :validateStatus="fields['specialist_id'].validateStatus" :help="fields['specialist_id'].help">
        <a-select v-model="form.specialist_id"
          @change="fieldChanged('specialist_id')">
          <a-select-option v-for="specialist in filteredSpecialists" :key="specialist.id">
            {{ specialist.__str__ }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item prop="start_time" label="Время" key="start_time"
        :validateStatus="fields['start_time'].validateStatus" :help="fields['start_time'].help">
        <a-input
          v-model="form.start_time"
          type="time"
          @change="fieldChanged('start_time')"
        />
      </a-form-model-item>

    </a-form-model>

  </a-modal>
</template>

<script>
import consts from "@/const";
import post from "@/middleware/post";
import put from "@/middleware/put";

export default {
  name: "ModalTemplateJob",
  props: {
    activities: {
      type: Array,
      required: true,
    },
    specialists: {
      type: Array,
      required: true,
    },
    editableData: {
      type: Object,
      default: null,
    }
  },
  data() {
    return {
      daysOfWeek: consts.daysOfWeek,
      form: {
        date: null,
        activity_id: null,
        specialist_id: null,
        start_time: null,
      },
      title: "",
      layout: {
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
      },
      fields: {
        'date': {
          validateStatus: "",
          help: "",
        },
        'activity_id': {
          validateStatus: "",
          help: "",
        },
        'specialist_id': {
          validateStatus: "",
          help: "",
        },
        'start_time': {
          validateStatus: "",
          help: "",
        },
      },
      rules: {
        date: [
          {
            trigger: "change",
            required: true,
            message: "Пожалуйста, выберите дату",
          },
        ],
        activity_id: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, выберите вид деятельности",
          },
        ],
        specialist_id: [
          {
            trigger: "blur",
            required: false,
            message: "Пожалуйста, выберите специалиста",
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
  computed: {
    filteredSpecialists(){
      let curr_activity_id = this.form.activity_id;

      if (curr_activity_id == null) {
        return [];
      }

      return this.specialists.filter((item)=>{
        if (item.is_staff) {
          return false;
        }

        for (let activity of item.activities) {
          if (curr_activity_id == activity.activity.id) {
            return true;
          }
        }

        return false;
      });
    }
  },
  methods: {
    fieldChanged(field_key) {
      this.fields[field_key].validateStatus = "";
      this.fields[field_key].help = "";
    },

    closeModal(isSuccess){
      this.$emit('closeModal', isSuccess);
    },

    async handleOk() {
      this.loadingButton = true;
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          try {
            let successCode = 0;
            let res = null;
            let successMessage = "";
            if (this.form.id) {
              successCode = 200;
              successMessage = "Занятие успешно изменено";
              res = await put(this.$axios, `/api/jobs/${this.form.id}/`, this.form);
            } else {
              successCode = 201;
              successMessage = "Занятие успешно добавлено";
              res = await post(this.$axios, "/api/jobs/", this.form);
            }

            if (res.status === successCode) {
              this.$message.success(successMessage);
              this.closeModal(true);
            } else if (res.status === 400) {
              this.$message.error("Проверьте введённые данные");
              for (let key in res.data) {
                this.fields[key].validateStatus = "error";
                this.fields[key].help = res.data[key];
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
    if (this.editableData) {
      this.title = "Изменение занятия";
      this.form.id = this.editableData.id
      this.form.date = this.editableData.date
      this.form.activity_id = this.editableData.activity_id
      this.form.specialist_id = this.editableData.specialist_id
      this.form.start_time = this.editableData.start_time
    } else {
      this.title = "Добавление занятия";
    }
    document.addEventListener("keydown", this.keydown);
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keydown);
  }
};
</script>

<style lang="sass"></style>
