<template>
  <a-modal
    okText="Сохранить"
    cancelText="Отмена"
    width="900px"
    :visible="true"
    :title="title"
    @cancel="closeModal(false)"
    @ok="handleOk"
    @confirmLoading="loadingButton">
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">
      <a-form-model-item prop="topic" label="Тема занятия" key="topic"
        :validateStatus="fields['topic'].validateStatus" :help="fields['topic'].help">
        <a-input v-model="form.topic" />
      </a-form-model-item>

      <a-form-model-item prop="skills" label="Навыки" key="skills"
        :validateStatus="fields['skills'].validateStatus" :help="fields['skills'].help">
        <a-tree-select
          :value="form.skills"
          @change="setSkills"
          :dropdownStyle="{'max-height': '500px', 'overflow-y': 'auto'}"
          placeholder="Выберите навыки"
          allow-clear multiple>
          <a-tree-select-node v-for="area in areas"
            :key="'area'+area.id"
            :value="'area'+area.id"
            :selectable="false"
            :title="`${area.number}. ${area.name}`">
            <a-tree-select-node v-for="direction in area.development_directions"
              :key="'direction'+direction.id"
              :value="'direction'+direction.id"
              :selectable="false"
              :title="`${area.number}.${direction.number}. ${direction.name}`">
              <a-tree-select-node v-for="skill in direction.skills"
                :key="'skill'+skill.id"
                :value="skill.id"
                :title="`${area.number}.${direction.number}.${skill.number}. ${skill.name}`"
                :isLeaf="true">
              </a-tree-select-node>
            </a-tree-select-node>
          </a-tree-select-node>
        </a-tree-select>
      </a-form-model-item>

      <a-form-model-item prop="form_id" label="Форма проведения занятия" key="form"
        :validateStatus="fields['form_id'].validateStatus" :help="fields['form_id'].help">
        <a-select v-model="form.form_id"
          allow-clear
          @change="fieldChanged($event, 'form_id')">
          <a-select-option v-for="form in forms" :key="form.id">
            {{ form.name }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item prop="method_id" label="Способ проведения занятия" key="method_id"
        :validateStatus="fields['method_id'].validateStatus" :help="fields['method_id'].help">
        <a-select v-model="form.method_id"
          :disabled="!form.form_id"
          allow-clear
          @change="fieldChanged($event, 'method_id')">
          <a-select-option v-for="method in methods" :key="method.id">
            {{ method.name }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item prop="comment" label="Дополнительная информация по занятию" key="comment"
        :validateStatus="fields['comment'].validateStatus" :help="fields['comment'].help">
        <a-input v-model="form.comment"
          allow-clear
          :auto-size="{minRows: 4, maxRows: 6}"
          @change="fieldChanged($event, 'comment')"
          type="textarea"/>
      </a-form-model-item>

      <a-form-model-item prop="option_files" label="Прикрепленные файлы" key="option_files"
        :validateStatus="fields['option_files'].validateStatus" :help="fields['option_files'].help">
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

  </a-modal>
</template>

<script>
import consts from "@/const";
import { mapActions, mapGetters } from "vuex";
import post from "@/middleware/post";
import put from "@/middleware/put";
import patch from "@/middleware/patch";

export default {
  name: "JobOptionModal",
  props: {
    activity: {
      type: Object,
      default: null,
    },
    option: {
      type: Object,
      default: null,
    }
  },
  data() {
    return {
      title: "",
      form: {
        topic: '',
        skills: [],
        form_id: null,
        method_id: null,
        comment: '',
        option_files: [],
      },
      layout: {
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
      },
      fields: {
        'topic': {
          validateStatus: "",
          help: "",
        },
        'skills': {
          validateStatus: "",
          help: "",
        },
        'form_id': {
          validateStatus: "",
          help: "",
        },
        'method_id': {
          validateStatus: "",
          help: "",
        },
        'comment': {
          validateStatus: "",
          help: "",
        },
        'option_files': {
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
        skills: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, выберите затрагиваемые навыки",
          },
        ],
        form_id: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, выберите форму проведения занятия",
          },
        ],
        method_id: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, выберите способ проведения занятия",
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
      areasFetched: "skills/getFetched",
      areas: "skills/getAreas",
      formsFetched: "forms/getFetched",
      forms: "forms/getForms",
    }),
    methods(){
      for (let form of this.forms) {
        if (form.id == this.form.form_id) {
          return form.methods.slice();
        }
      }
      return [];
    },
  },
  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas",
      fetchForms: "forms/fetchForms",
    }),

    async fieldChanged(val, field_key) {
      if (field_key == "form_id") {
        this.form.method_id = null;
      }

      this.fields[field_key].validateStatus = "";
      this.fields[field_key].help = "";
    },

    closeModal(result=false){
      this.$emit('closeModal', result);
    },

    async handleOk() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          try {
            this.loading = true;

            const formData = new FormData();
            formData.append('activity_id', this.activity.id);

            formData.append('topic', this.form.topic);
            formData.append('skills', this.form.skills);
            formData.append('method_id', this.form.method_id ? this.form.method_id : '');
            formData.append('comment', this.form.comment);

            let allFilesIds = [];
            this.form.option_files.forEach((file) => {
              allFilesIds.push(file.uid);
              if (file.status != "done") {
                formData.append(file.uid, file);
              }
            });
            formData.append('files', allFilesIds);

            let successCode = 0;
            let res = null;
            let successMessage = "";

            if (this.option) {
              successCode = 200;
              successMessage = "Параметры плана занятия сохранены";
              res = await patch(this.$axios, `/api/options/${this.option.id}/`, formData);
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
          }
        } else {
          return false;
        }
      });
    },
    setSkills(values, labels){
      this.form.skills.splice(0);
      for (let value of values) {
        this.form.skills.push(value);
      }
      this.fieldChanged(values, 'skills');
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
        this.$refs.form !== undefined
      ) {
        this.handleOk();
      }
    },
  },
  async created() {
    let fetches = [];
    if (!this.areasFetched) {
      fetches.push(this.fetchAreas());
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
      this.form.skills.splice(0);
      this.form.skills = this.option.skills.map((skill)=>{
        return skill.id;
      });
      this.form.form_id = this.option.method ? this.option.method.form_id : null;
      this.form.method_id = this.option.method ? this.option.method.id : null;
      this.form.comment = this.option.comment;
      this.form.option_files.splice(0);
      for (let option_file of this.option.option_files) {
        this.form.option_files.push({
          uid: option_file.id,
          name: option_file.name,
          status: 'done',
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
  }
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

</style>
