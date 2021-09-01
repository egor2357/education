<template>
  <a-modal :visible="true" :title="title" @cancel="handleCancel" :width="'600px'">
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
            <a-select-option v-for="area in areasAll" :key="area.id">
              {{ area.name }}
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
import { mapGetters } from "vuex";
export default {
  name: "TalentsModal",
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
        area_id: null,
        name: "",
        text: "",
      },
      title: "",
      layout: {
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
      },
      fields: [
        {
          name: "area_id",
          label: "Образовательная область",
          type: "select",
          validateStatus: "",
          help: "",
        },
        {
          name: "name",
          label: "Наименование таланта",
          type: "text",
          validateStatus: "",
          help: "",
        },
        {
          name: "text",
          label: "Описание",
          type: "textarea",
          validateStatus: "",
          help: "",
        },
      ],
      rules: {
        area_id: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, выберите образовательную область",
          },
        ],
        name: [
          {
            trigger: "blur",
            required: true,
            message: "Пожалуйста, введите наименование",
          },
        ],
      },
      loadingButton: false,
    };
  },
  methods: {
    handleCancel() {
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
              dispatchName = "talents/addTalent";
              successCode = 201;
              successMessage = "Талант успешно добавлен";
            } else {
              dispatchName = "talents/editTalent";
              successCode = 200;
              successMessage = "Талант успешно изменен";
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
    if (this.adding) {
      this.title += "Добавление таланта";
    } else {
      this.title += "Изменение таланта";
      this.editableData.id ? (this.form.id = this.editableData.id) : "";
      if (this.editableData.area) {
        this.editableData.area.id
          ? (this.form.area_id = this.editableData.area.id)
          : (this.form.area_id = null);
      }
      this.editableData.name
        ? (this.form.name = this.editableData.name)
        : (this.form.name = "");
      this.editableData.text
        ? (this.form.text = this.editableData.text)
        : (this.form.text = "");
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
      areasAll: "skills/getAreasAll",
    }),
  },
};
</script>

<style scoped></style>
