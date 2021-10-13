<template>
  <a-modal
    :visible="true"
    :title="title"
    :footer="isStaff ? undefined : null"
    @cancel="handleCancel(false)"
    width='70%'
  >
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <a-form-model-item
        :prop="fields[0].name"
        :key="fields[0].name"
        :validateStatus="fields[0].validateStatus"
        :help="fields[0].help"
      >
        <div class="modal-summary__specialist">
          <span class="modal-summary__specialist-label">Специалист:</span>
          <span class="modal-summary__specialist-value">{{editableSpecialist}}</span>          
        </div>
        <div class="modal-summary__period">
          <span class="modal-summary__period-label">Период:</span>
          <span class="modal-summary__period-value">{{editableData.presence.full_interval.date_from.split('-').reverse().join('.')}} - {{editableData.presence.full_interval.date_to.split('-').reverse().join('.')}}</span>
        </div>

        <a-textarea
          v-model="form[fields[0].name]"
          :rows="6"
          :ref="`field0`"
          v-if = "isStaff"
          @change="fieldChanged(fields[0])"
        />
        <div class="modal-summary__text" v-else :ref="`field0`">{{form[fields[0].name] || 'Отчет отсутствует'}}</div>
      </a-form-model-item>
    </a-form-model>
    <template slot="footer">
      <a-button @click="handleCancel(false)"> Отменить </a-button>
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
import patch from "@/middleware/patch";

export default {
  name: "ModalSummary",
  props: {
    editableData: Object,
    isStaff: Boolean,
    editableSpecialist: String,
  },
  data() {
    return {
      form: {
        summary: "",
      },
      title: "Отчет по пребыванию",
      layout: {
        labelCol: { span: 0 },
        wrapperCol: { span: 25 },
      },
      fields: [
        {
          name: "summary",
          label: "Отчет",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        summary: [
          {
            trigger: "blur",
            required: false,
            message: "",
          },
        ],
      },
      loadingButton: false,
    };
  },
  methods: {
    handleCancel(isSuccess = false) {
      this.form.summary = "";
      if (isSuccess) {
        this.$emit("close", true);
      } else {
        this.$emit("close", false);
      }
    },
    async handleOk() {
      if (!this.loadingButton) {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
            this.loadingButton = true;
            let res = await patch(
              this.$axios,
              `/api/presence/${this.editableData.presence.id}/`,
              this.form
            );
            if (res.status === 200) {
              this.$message.success("Отчет по пребыванию сохранен");
              this.handleCancel(true);
            } else if (res.status === 403) {
              this.$message.error("Недостаточно прав");
              this.loadingButton = false;
            } else if (res.status === 400) {
              this.$message.error("Проверьте введённые данные");
              this.loadingButton = false;
            } else {
              this.$message.error("Произошла ошибка");
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
    document.addEventListener("keydown", this.keydown);
    this.form.summary = this.editableData.presence.summary;
  },
  mounted() {
    this.$nextTick(() => {
      this.$refs["field0"].focus();
    });
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keydown);
  },
  computed: {},
};
</script>

<style lang="sass">
  .modal-summary__specialist
    line-height: 20px
    margin-bottom: 10px

  .modal-summary__specialist-label
    margin-right: 10px
    color: #999

  .modal-summary__text
    line-height: 20px
    white-space: pre-wrap

  .modal-summary__period
    line-height: 10px
    margin-bottom: 20px

  .modal-summary__period-label
    margin-right: 10px
    color: #999

</style>
