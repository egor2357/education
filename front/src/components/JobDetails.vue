<template>
  <a-spin :spinning="loading">
    <div class="job-details">
      <div class="job-details__header">

        <div class="job-details__header-title" v-if="job">
          <div class="job-details__header-title__activity">
            <div :style="{
              'background-color': `${job.activity.color}10`,
              border: `1px solid ${job.activity.color}99`,
            }">
              {{ job.activity.name }}
            </div>
          </div>
          <div class="job-details__header-title__date">
            <div class="job-details__header-title__date-day">
              {{ jobDateMoment.format("D MMMM") }}
            </div>
            <div class="job-details__header-title__date-weekday">
              {{ jobDateMoment.format("dddd") }}
            </div>
          </div>
          <div class="job-details__header-title__specialist">
            <div class="job-details__header-title__specialist-label">Специалист:</div>
            <div class="job-details__header-title__specialist-name">{{ job.specialist.__str__ }}</div>
          </div>
        </div>

        <div class="job-details__header__options">
          <div class="job-details__header__options__back">
            <a-button icon="left" @click="goBack">Назад</a-button>
          </div>
          <a-radio-group v-model="isJobWindow">
            <a-radio-button :value="true">Параметры занятия</a-radio-button>
            <a-radio-button :value="false">Отчет</a-radio-button>
          </a-radio-group>
        </div>

      </div>

      <div class="job-details__body" v-if="job">

        <a-form-model :model="form" v-bind="layout" :rules="rules" ref="jobForm">

          <a-form-model-item prop="topic" label="Тема занятия" key="topic"
            :validateStatus="fields['topic'].validateStatus" :help="fields['topic'].help">
            <a-input v-model="form.topic" />
          </a-form-model-item>

          <a-form-model-item prop="reports" label="Навыки" key="reports"
            :validateStatus="fields['reports'].validateStatus" :help="fields['reports'].help">
            <a-tree-select
              :value="form.reports"
              @change="setReports"
              placeholder="Выберите навыки"
              allow-clear multiple>
              <a-tree-select-node v-for="area in areas"
                :key="'area'+area.id"
                :value="'area'+area.id"
                :selectable="false"
                :title="area.name">
                <a-tree-select-node v-for="direction in area.development_directions"
                  :key="'direction'+direction.id"
                  :value="'direction'+direction.id"
                  :selectable="false"
                  :title="direction.name">
                  <a-tree-select-node v-for="skill in direction.skills"
                    :key="'skill'+skill.id"
                    :value="skill.id"
                    :title="skill.name"
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

          <a-form-model-item prop="method_id" label="Метод проведения занятия" key="method_id"
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
              type="textarea"/>
          </a-form-model-item>

          <a-form-model-item prop="job_files" label="Прикрепленные файлы" key="job_files"
            :validateStatus="fields['job_files'].validateStatus" :help="fields['job_files'].help">
            <a-upload
              multiple
              list-type="picture"
              :default-file-list="form.job_files"
              class="job-details__body__form-files"
            >
              <a-button> <a-icon type="upload" /> Прикрепить файл </a-button>
            </a-upload>
          </a-form-model-item>

          <a-form-model-item class="job-details__body__form-ok"
            :wrapper-col="{offset: 6}">
            <a-button icon="check" type="primary" @click="saveJob">Сохранить параметры занятия</a-button>
          </a-form-model-item>
        </a-form-model>


      </div>
    </div>
  </a-spin>
</template>

<script>
import moment from "moment";
import getColorByMark from "@/mixins/getColorByMark"
import { mapActions, mapGetters } from "vuex";

export default {
  name: "JobDetails",
  mixins: [getColorByMark],
  props: {
  },
  data() {
    return {
      loading: true,

      job: null,
      form: {
        topic: '',
        reports: [],
        form_id: null,
        method_id: null,
        comment: '',
        job_files: [],
      },

      isJobWindow: true,
      layout: {
        labelCol: { span: 6 },
        wrapperCol: { span: 14 },
      },

      fields: {
        'topic': {
          validateStatus: "",
          help: "",
        },
        'reports': {
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
        'job_files': {
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
        reports: [
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
            message: "Пожалуйста, выберите метод проведения занятия",
          },
        ],
        comment: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, введите дополнительную информацию",
          },
        ],
        job_files: [
          {
            trigger: "change",
            required: false,
            message: "Пожалуйста, выберите файлы",
          },
        ],
      },
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

    fieldChanged(value, key){
      console.log(value);
      if (key == "form_id") {
        this.form.method_id = null;
      }
      this.fields[key].validateStatus = "";
      this.fields[key].help = "";
    },

    setReports(values, labels){
      this.form.reports.splice(0);
      for (let value of values) {
        this.form.reports.push(value);
      }
    },

    goBack(){
      this.$router.go(-1);
    },
    setJobFormData(job) {
      this.form.topic = job.topic
      this.form.reports = job.reports.map((report)=>{
        return report.skill_id;
      });
      this.form.form_id = job.method ? job.method.form_id : null;
      this.form.method_id = job.method ? this.job.method.id : null;
      this.form.comment = job.comment;
      this.form.job_files = job.job_files.map((job_file)=>{
        return {
          uid: job_file.id,
          name: 'yyy.png',
          status: 'done',
          url: job_file.file,
        };
      });
    },
    async fetchJob(){
      try {
        this.loading = true;
        let jobId = this.$route.params.id;
        let res = await this.$axios.get(`/api/jobs/${jobId}`);
        if (res.status === 200) {
          this.job = res.data;
          this.jobDateMoment = moment(this.job.date, "YYYY-MM-DD");
          this.setJobFormData(this.job);
        } else {
          this.$message.error("Произошла ошибка при загрузке занятия");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка при загрузке занятия");
      } finally {
        this.loading = false;
      }
    },
    async saveJob(){

    },
  },
  async created() {
    let fetches = []

    if (!this.areasFetched) {
      fetches.push(this.fetchAreas());
    }
    if (!this.formsFetched) {
      fetches.push(this.fetchForms());
    }

    fetches.push(this.fetchJob());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
  },
  beforeDestroy() {

  }
};
</script>

<style lang="sass">
.job-details
  display: flex
  flex-direction: column
  overflow: hidden
  height: 100%
  &__header
    display: flex
    flex-direction: column
    &-title
      display: flex
      flex-direction: row
      justify-content: center
      align-items: center
      flex: 1
      text-align: center
      font-size: 1rem
      margin-bottom: 10px
      &__activity
        display: flex
        margin-right: 20px
        max-width: 400px
        div
          padding: 2px 4px
          text-align: center
          border-radius: 4px
      &__date
        display: flex
        flex-direction: column
        align-items: center
        margin-right: 20px
        &-day
          color: rgba(0, 0, 0, 0.85)
          font-size: 20px
          line-height: 22px
          &:first-letter
            font-weight: bold
        &-weekday
          font-size: 18px
          line-height: 20px
      &__specialist
        display: flex
        flex-direction: row
        &-label
          margin-right: 10px
        &-name
          color: rgba(0, 0, 0, 0.85)


    &__options
      display: flex
      flex-direction: row
      align-items: center
      justify-content: space-between
      margin-bottom: 10px
      &__back
        display: flex
        flex-direction: row
        justify-content: flex-start

  &__body

.job-details__body__form-files
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