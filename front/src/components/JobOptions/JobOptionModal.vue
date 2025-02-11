<template>
  <a-modal
    width="900px"
    class="option-details"
    :visible="true"
    :title="title"
    @cancel="closeModal(false)"
  >
    <a-form-model
      :model="form" v-bind="layout"
      :rules="rules" ref="form"
    >
      <a-form-model-item
        prop="topic"
        label="Тема занятия"
        key="topic"
        :validateStatus="fields['topic'].validateStatus"
        :help="fields['topic'].help"
      >
        <a-input v-model="form.topic" />
      </a-form-model-item>

      <a-form-model-item
        prop="exercises"
        label="Упражнения"
        key="exercises"
        :validateStatus="fields['exercises'].validateStatus"
        :help="fields['exercises'].help"
      >
        <treeselect
          v-model="form.exercises"
          :multiple="true"
          :options="exercisesOptions"
          placeholder="Выберите упражнения"
          valueConsistsOf="LEAF_PRIORITY"
          :disableBranchNodes="true"
          :backspaceRemoves="false"
          noChildrenText="У этого узла нет элементов"
          noOptionsText="Структура навыков не определена"
          noResultsText="Поиск не дал результатов"
        />
      </a-form-model-item>

      <a-form-model-item
        prop="methods"
        label="Формы проведения занятия"
        key="methods"
        :validateStatus="fields['methods'].validateStatus"
        :help="fields['methods'].help"
      >
        <treeselect
          v-model="form.methods"
          :multiple="true"
          :options="methodsOptions"
          placeholder="Выберите упражнения"
          valueConsistsOf="LEAF_PRIORITY"
          :disableBranchNodes="true"
          :backspaceRemoves="false"
          noChildrenText="У этого узла нет элементов"
          noOptionsText="Структура навыков не определена"
        />
      </a-form-model-item>

      <a-form-model-item
        prop="comment"
        label="Дополнительная информация по занятию"
        key="comment"
        :validateStatus="fields['comment'].validateStatus"
        :help="fields['comment'].help"
      >
        <a-input
          v-model="form.comment"
          allow-clear
          :auto-size="{ minRows: 4, maxRows: 6 }"
          @change="fieldChanged($event, 'comment')"
          type="textarea"
        />
      </a-form-model-item>

      <a-form-model-item
        prop="option_files"
        label="Прикрепленные файлы"
        key="option_files"
        :validateStatus="fields['option_files'].validateStatus"
        :help="fields['option_files'].help"
      >
        <a-upload
          multiple
          list-type="picture"
          :file-list="form.option_files"
          :remove="handleRemoveOptionFile"
          :before-upload="beforeUploadOptionFile"
          class="option-details__body__form-files"
        >
          <a-button> <a-icon type="upload" /> Прикрепить файл </a-button>
        </a-upload>
      </a-form-model-item>
    </a-form-model>

    <template slot="footer">
      <a-button @click="closeModal(false)"> Отмена </a-button>
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
import { mapActions, mapGetters } from "vuex";
import post from "@/middleware/post";
import put from "@/middleware/put";
import patch from "@/middleware/patch";

import Treeselect from "@riophae/vue-treeselect";
import "@riophae/vue-treeselect/dist/vue-treeselect.css";

export default {
  name: "JobOptionModal",
  components: {
    Treeselect,
  },
  props: {
    activity: {
      type: Object,
      default: null,
    },
    option: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      title: "",
      form: {
        topic: "",
        exercises: [],
        methods: [],
        comment: "",
        option_files: [],
      },
      layout: {
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
      },
      fields: {
        topic: {
          validateStatus: "",
          help: "",
        },
        exercises: {
          validateStatus: "",
          help: "",
        },
        methods: {
          validateStatus: "",
          help: "",
        },
        comment: {
          validateStatus: "",
          help: "",
        },
        option_files: {
          validateStatus: "",
          help: "",
        },
      },
      rules: {
        topic: [
          {
            trigger: "change",
            required: true,
            message: "Пожалуйста, введите название темы",
          },
        ],
        exercises: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, выберите выполняемые упражнения",
          },
        ],
        methods: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, выберите формы проведения занятия",
          },
        ],
        comment: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, введите дополнительную информацию",
          },
        ],
        option_files: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, выберите файлы",
          },
        ],
      },

      loadingButton: false,
    };
  },
  computed: {
    ...mapGetters({
      allowedFetched: "skills/getAllowedFetched",
      allowedAreas: "skills/getAllowedAreas",
      exercisesOptions: "skills/exerciseOptions",
      formsFetched: "forms/getFetched",
      forms: "forms/getForms",
    }),

    methodsOptions() {
      let options = [];
      for (let form of this.forms) {
        let formNode = {
          id: 'form' + form.id,
          label: form.name,
          children: []
        };
        for (let method of form.methods) {
          let methodNode = {
            id: method.id,
            label: method.name,
          }
          formNode.children.push(methodNode);
        }
        options.push(formNode);
      }
      return options;
    },
  },
  methods: {
    ...mapActions({
      fetchAllowedAreas: "skills/fetchAllowedAreas",
      fetchForms: "forms/fetchForms",
    }),

    async fieldChanged(val, field_key) {
      this.fields[field_key].validateStatus = "";
      this.fields[field_key].help = "";
    },

    closeModal(result = false) {
      this.$emit("closeModal", result);
    },

    async handleOk() {
      if (!this.loadingButton) {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
            try {
              this.loadingButton = true;
              this.loading = true;

              const formData = new FormData();
              formData.append("activity_id", this.activity.id);

              formData.append("topic", this.form.topic);
              formData.append("exercises", JSON.stringify(this.form.exercises));
              formData.append("methods", JSON.stringify(this.form.methods));
              formData.append("comment", this.form.comment);

              let currFilesIds = [];
              this.form.option_files.forEach((file) => {
                if (file.status != "done") {
                  formData.append("files", file);
                } else {
                  currFilesIds.push(file.uid);
                }
              });
              formData.append("files_id", JSON.stringify(currFilesIds));

              let successCode = 0;
              let res = null;
              let successMessage = "";

              if (this.option) {
                successCode = 200;
                successMessage = "Параметры плана занятия сохранены";
                res = await patch(
                  this.$axios,
                  `/api/options/${this.option.id}/`,
                  formData
                );
              } else {
                successCode = 201;
                successMessage = "План занятия успешно добавлен";
                res = await post(this.$axios, `/api/options/`, formData);
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
              this.loading = false;
              this.loadingButton = false;
            }
          } else {
            return false;
          }
        });
      }
    },
    handleRemoveOptionFile(file) {
      const index = this.form.option_files.indexOf(file);
      const newFileList = this.form.option_files.slice();
      newFileList.splice(index, 1);
      this.form.option_files = newFileList;
    },
    beforeUploadOptionFile(file) {
      this.form.option_files = [...this.form.option_files, file];
      return false;
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
  async created() {
    let fetches = [];
    if (!this.allowedFetched) {
      fetches.push(this.fetchAllowedAreas());
    }
    if (!this.formsFetched) {
      fetches.push(this.fetchForms());
    }

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;

    if (this.option) {
      this.title = `${this.activity.name} | Изменение плана занятия`;
      this.form.topic = this.option.topic;

      this.form.exercises.splice(0);
      this.form.exercises = this.option.exercises.map((exercise) => {
        return exercise.id;
      });

      this.form.methods.splice(0);
      this.form.methods = this.option.methods.map((method) => {
        return method.id;
      });

      this.form.comment = this.option.comment;
      this.form.option_files.splice(0);
      for (let option_file of this.option.option_files) {
        this.form.option_files.push({
          uid: option_file.id,
          name: option_file.name,
          status: "done",
          url: option_file.file,
        });
      }
    } else {
      this.title = `${this.activity.name} | Добавление плана занятия`;
    }
    document.addEventListener("keydown", this.keydown);
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keydown);
  },
};
</script>

<style lang="sass">
.option-details
  &__body__form-files
    display: flex
    flex-direction: column
    max-height: 200px
    .ant-upload-list
      display: flex
      flex: 1
      flex-direction: row
      flex-wrap: wrap
      overflow-y: auto
      .ant-upload-list-item
        min-width: 200px
        margin-right: 8px

  .vue-treeselect--open.vue-treeselect--open-below .vue-treeselect__control
    border-bottom-left-radius: 5px
    border-bottom-right-radius: 5px
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2)
    border-color: #40a9ff

  .vue-treeselect__value-container
    line-height: 18px
  .vue-treeselect__multi-value-item-container
    line-height: 18px
  .vue-treeselect__multi-value-item
    border: 1px solid #e8e8e8
    background-color: #fafafa
  .vue-treeselect__multi-value-label
    font-size: 14px
    color: rgba(0, 0, 0, 0.65)
  .vue-treeselect__multi-value-remove
    color: rgba(0, 0, 0, 0.65)
  .vue-treeselect__value-remove
    color: rgba(0, 0, 0, 0.65)

  .vue-treeselect__menu
    margin-top: 2px
    border: none
    border-radius: 4px
    box-shadow: rgba(0, 0, 0, 0.15) 0px 2px 8px 0px

</style>
