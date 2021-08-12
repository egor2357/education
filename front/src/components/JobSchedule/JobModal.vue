<template>
  <a-modal :visible="true" :title="title" @cancel="closeModal(null)">
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <a-form-model-item
        prop="date"
        label="Дата"
        key="date"
        :validateStatus="fields['date'].validateStatus"
        :help="fields['date'].help"
      >
        <a-date-picker
          v-model="form.date"
          type="date"
          placeholder="Выберите дату"
          format="DD.MM.YYYY"
          style="width: 100%"
          @change="fieldChanged($event, 'date')"
        />
      </a-form-model-item>

      <a-form-model-item
        prop="activity_id"
        label="Вид деятельности"
        key="activity_id"
        :validateStatus="fields['activity_id'].validateStatus"
        :help="fields['activity_id'].help"
      >
        <a-select
          v-model="form.activity_id"
          @change="fieldChanged($event, 'activity_id')"
        >
          <a-select-option v-for="activity in activities" :key="activity.id">
            {{ activity.name }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item
        prop="specialist_id"
        label="Специалист"
        key="specialist_id"
        :validateStatus="fields['specialist_id'].validateStatus"
        :help="fields['specialist_id'].help"
      >
        <a-select
          v-model="form.specialist_id"
          :disabled="!form.activity_id || !form.date"
          :allowClear="true"
          @change="fieldChanged($event, 'specialist_id')"
        >
          <a-select-option
            v-for="specialist in filteredSpecialists"
            :key="specialist.id"
          >
            {{ specialist.__str__ }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item
        prop="start_time"
        label="Время"
        key="start_time"
        :validateStatus="fields['start_time'].validateStatus"
        :help="fields['start_time'].help"
      >
        <a-input
          v-model="form.start_time"
          v-mask="timeMask"
          placeholder="ЧЧ:ММ"
          @change="fieldChanged($event, 'start_time')"
        />
      </a-form-model-item>
    </a-form-model>
    <template slot="footer">
      <a-button @click="closeModal(null)"> Отмена </a-button>
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
import consts from "@/const";
import post from "@/middleware/post";
import put from "@/middleware/put";
import moment from "moment";
import datetime from "@/mixins/datetime";

export default {
  name: "JobModal",
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
    },
  },
  mixins: [datetime],
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
        date: {
          validateStatus: "",
          help: "",
        },
        activity_id: {
          validateStatus: "",
          help: "",
        },
        specialist_id: {
          validateStatus: "",
          help: "",
        },
        start_time: {
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

      dayPresence: [],

      loadingButton: false,
    };
  },
  computed: {
    availableSpecialistsIds() {
      return this.dayPresence.map((item) => {
        if (item.is_available) {
          return item.specialist_id;
        }
      });
    },
    filteredSpecialists() {
      let curr_activity_id = this.form.activity_id;

      if (curr_activity_id == null) {
        return [];
      }

      return this.specialists.filter((item) => {
        if (item.is_staff) {
          return false;
        }

        if (!this.availableSpecialistsIds.includes(item.id)) {
          return false;
        }

        for (let activity of item.activities) {
          if (curr_activity_id == activity.activity.id) {
            return true;
          }
        }

        return false;
      });
    },
  },
  methods: {
    async fetchDayPresence() {
      try {
        let dateStr = moment(this.form.date).format("YYYY-MM-DD");
        let res = await this.$axios.get(
          `/api/presence/?interval_start=${dateStr}&interval_end=${dateStr}`
        );
        if (res.status == 200) {
          this.dayPresence = res.data;
        } else {
          this.$message.error("Ошибка при получении присутствия специалистов");
          return;
        }
      } catch {
        this.$message.error("Ошибка при получении присутствия специалистов");
        return;
      }
    },

    async fieldChanged(val, field_key) {
      if (field_key == "date") {
        this.form.specialist_id = null;
        await this.fetchDayPresence();
      }
      if (field_key == "activity_id") {
        this.form.specialist_id = null;
      }
      if (field_key == "specialist_id" && val == undefined) {
        this.form.specialist_id = null;
      }
      this.fields[field_key].validateStatus = "";
      this.fields[field_key].help = "";
    },

    closeModal(jobDate = null) {
      this.$emit("closeModal", jobDate);
    },

    async handleOk() {
      if (!this.loadingButton) {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
            try {
              this.loadingButton = true;
              let successCode = 0;
              let res = null;
              let successMessage = "";
              this.form.date = this.form.date.format("YYYY-MM-DD");
              if (this.form.id) {
                successCode = 200;
                successMessage = "Занятие успешно изменено";
                res = await put(
                  this.$axios,
                  `/api/jobs/${this.form.id}/`,
                  this.form
                );
              } else {
                successCode = 201;
                successMessage = "Занятие успешно добавлено";
                res = await post(this.$axios, "/api/jobs/", this.form);
              }

              if (res.status === successCode) {
                this.$message.success(successMessage);
                this.closeModal(moment(this.form.date, "YYYY-MM-DD"));
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
              this.form.date = moment(this.form.date, "YYYY-MM-DD");
              this.loadingButton = false;
            }
          } else {
            return false;
          }
        });
      }
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
      this.form.id = this.editableData.id;
      this.form.date = moment(this.editableData.date, "YYYY-MM-DD");
      this.fetchDayPresence();
      this.form.activity_id = this.editableData.activity.id;
      if (this.editableData.specialist) {
        this.form.specialist_id = this.editableData.specialist.id;
      } else {
        this.form.specialist_id = null;
      }
      this.form.start_time = this.editableData.start_time;
    } else {
      this.title = "Добавление занятия";
    }
    document.addEventListener("keydown", this.keydown);
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keydown);
  },
};
</script>

<style lang="sass"></style>
