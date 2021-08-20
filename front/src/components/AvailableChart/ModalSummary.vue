<template>
  <a-modal :visible="true" :title="title" @cancel="handleCancel">
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <a-form-model-item
        :prop="fields[0].name"
        :key="fields[0].name"
        :validateStatus="fields[0].validateStatus"
        :help="fields[0].help"
      >
        <a-textarea
          v-model="form[fields[0].name]"
          @change="fieldChanged(fields[0])"
          :rows="6"
          :ref="`field0`"
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
import patch from "@/middleware/patch";

export default {
  name: "ModalSummary",
  props: {
    editableData: Object,
  },
  data() {
    return {
      form: {
        summary: ''
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
    handleCancel() {
      this.form.summary = '';
      this.$emit("close");
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
              this.handleCancel();
            } else if (res.status === 400) {
              this.$message.error("Проверьте введённые данные");
            } else {
              this.$message.error("Произошла ошибка");
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
  computed: {
  },
};
</script>

<style scoped>

</style>
