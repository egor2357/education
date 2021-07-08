<template>
  <a-modal :visible="true" :title="title" @cancel="handleCancel">
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <template v-for="(field, index) in fields">
        <a-form-model-item
          :prop="field.name"
          :label="field.label"
          :key="field.name"
          :validateStatus="field.validateStatus"
          :help="field.help"
        >
          <a-select
            v-if="field.type === 'select'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
          >
            <a-select-option
              v-for="specialist in specialists"
              :key="specialist.id"
            >
              {{ specialist.__str__ }}
            </a-select-option>
          </a-select>
          <a-range-picker
            v-if="field.type === 'range'"
            v-model="form[field.name]"
            @change="fieldChanged(field)"
            :ref="`field${index}`"
            format="DD.MM.YYYY"
            separator="-"
          />
        </a-form-model-item>
      </template>
      <a-form-model-item prop="quarantine" label="Карантин" key="quarantine">
        <a-checkbox v-model="form.with_quarantine" />
        <span style="margin: 10px" v-if="form.with_quarantine"
          >Количество дней:</span
        >
        <a-input-number
          v-model="form.quarantine_days"
          :min="0"
          :max="maxDays"
          v-if="form.with_quarantine"
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
import { mapGetters } from "vuex";
import moment from "moment";
import common from "@/mixins/common";
export default {
  name: "ModalPeriod",
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
        date: null,
        specialist_id: null,
        with_quarantine: false,
        quarantine_days: 1,
      },
      title: "",
      layout: {
        labelCol: { span: 7 },
        wrapperCol: { span: 17 },
      },
      fields: [
        {
          name: "specialist_id",
          label: "Специалист",
          type: "select",
          validateStatus: "",
          help: "",
        },
        {
          name: "date",
          label: "Дата присутствия",
          type: "range",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        specialist_id: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, выберите специалиста",
          },
        ],
        date: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, выберите дату",
          },
        ],
      },
      maxDays: 0,
      loadingButton: false,
    };
  },
  methods: {
    handleCancel() {
      this.form.name = null;
      this.form.date = null;
      this.form.with_quarantine = null;
      this.form.quarantine_days = null;
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
              dispatchName = "presence/addPresence";
              successCode = 201;
              successMessage =
                "Период присутствия специалиста успешно добавлен";
            } else if (!this.adding) {
              dispatchName = "presence/editPresence";
              successCode = 200;
              successMessage = "Период присутствия специалиста успешно изменен";
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
                if (res.data["non_field_errors"]) {
                  for (let error of res.data["non_field_errors"]) {
                    this.$message.error(error);
                  }
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
      if (field.name === "date") {
        if (this.form.date[0])
          this.form.date_from = this.form.date[0].format("YYYY-MM-DD");
        if (this.form.date[1])
          this.form.date_to = this.form.date[1].format("YYYY-MM-DD");
        if (
          this.form.date[0] &&
          this.form.date[1] &&
          this.form.date[1].diff(this.form.date[0], "days") > 0
        ) {
          this.maxDays = this.form.date[1].diff(this.form.date[0], "days") - 1;
        }
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
    if (this.adding) {
      this.title += "Добавление периода присутствия специалиста";
    } else {
      this.title += "Изменение периода присутствия специалиста";
      this.form.id =
        this.editableData.presence.main_interval_id === null
          ? this.editableData.presence.id
          : this.editableData.presence.main_interval_id;
      if (this.editableData.presence.specialist_id) {
        this.form.specialist_id = this.editableData.presence.specialist_id;
      }
      if (
        this.editableData.presence.full_interval.date_from &&
        this.editableData.presence.full_interval.date_to
      ) {
        this.form.date = [];
        this.form.date[0] = moment(
          this.editableData.presence.full_interval.date_from,
          "YYYY-MM-DD"
        );
        this.form.date[1] = moment(
          this.editableData.presence.full_interval.date_to,
          "YYYY-MM-DD"
        );
        if (this.form.date[1].diff(this.form.date[0], "days") > 0) {
          this.maxDays = this.form.date[1].diff(this.form.date[0], "days") - 1;
        }
        this.form.date_from = this.editableData.presence.full_interval.date_from;
        this.form.date_to = this.editableData.presence.full_interval.date_to;
      }
      if (this.editableData.presence.full_interval.quarantine_days === 0) {
        this.form.with_quarantine = false;
        this.form.quarantine_days = 0;
      } else {
        this.form.with_quarantine = true;
        this.form.quarantine_days = this.editableData.presence.full_interval.quarantine_days;
      }
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
  },
};
</script>

<style scoped></style>
