<template>
  <a-spin :spinning="loading">
    <div class="job-details">
      <div class="job-details__header">
        <div class="job-details__header-title">
          <div class="job-details__header-left-block">
            <a-button icon="left" @click="goBack">Назад</a-button>
          </div>
          <div class="job-details__header-center-block" v-if="job">
            <div class="job-details__header-title__activity">
              <div
                :style="{
                  'background-color': `${job.activity.color}10`,
                  border: `1px solid ${job.activity.color}99`,
                }"
              >
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
              <div class="job-details__header-title__specialist-label">
                Специалист:
              </div>
              <div class="job-details__header-title__specialist-name">
                {{ job.specialist ? job.specialist.__str__ : "Не назначен" }}
              </div>
            </div>
          </div>
          <div class="job-details__header-right-block"></div>
        </div>
      </div>

      <div class="job-details__content">
        <div class="job-details__tabs-holder">
          <a-tabs v-model="activeTab" class="job-details__tabs">
            <a-tab-pane key="1">
              <span slot="tab">
                <a-icon type="setting" />
                Параметры занятия
              </span>
            </a-tab-pane>
            <a-tab-pane key="2">
              <span slot="tab">
                <a-icon type="carry-out" />
                Отчет
              </span>
            </a-tab-pane>
          </a-tabs>
        </div>
        <div class="job-details__tab_content">
          <a-form-model
            v-if="activeTab == 1"
            :model="form"
            v-bind="layout"
            :rules="rules"
            ref="jobForm"
          >
            <a-form-model-item
              prop="topic"
              label="Тема занятия"
              key="topic"
              :validateStatus="fields['topic'].validateStatus"
              :help="fields['topic'].help"
            >
              <a-input v-model="form.topic" :disabled="isDisabled" />
            </a-form-model-item>

            <a-form-model-item
              prop="reports"
              label="Навыки"
              key="reports"
              :validateStatus="fields['reports'].validateStatus"
              :help="fields['reports'].help"
            >
              <a-tree-select
                :value="form.reports"
                @change="setReports"
                :dropdownStyle="{ 'max-height': '500px', 'overflow-y': 'auto' }"
                placeholder="Выберите навыки"
                allow-clear
                multiple
                :disabled="isDisabled"
              >
                <a-tree-select-node
                  v-for="area in areas"
                  :key="'area' + area.id"
                  :value="'area' + area.id"
                  :selectable="false"
                  :title="`${area.number}. ${area.name}`"
                >
                  <a-tree-select-node
                    v-for="direction in area.development_directions"
                    :key="'direction' + direction.id"
                    :value="'direction' + direction.id"
                    :selectable="false"
                    :title="`${area.number}.${direction.number}. ${direction.name}`"
                  >
                    <a-tree-select-node
                      v-for="skill in direction.skills"
                      :key="'skill' + skill.id"
                      :value="skill.id"
                      :title="`${area.number}.${direction.number}.${skill.number}. ${skill.name}`"
                      :isLeaf="true"
                    >
                    </a-tree-select-node>
                  </a-tree-select-node>
                </a-tree-select-node>
              </a-tree-select>
            </a-form-model-item>

            <a-form-model-item
              prop="form_id"
              label="Форма проведения занятия"
              key="form"
              :validateStatus="fields['form_id'].validateStatus"
              :help="fields['form_id'].help"
            >
              <a-select
                v-model="form.form_id"
                allow-clear
                @change="fieldChanged($event, 'form_id')"
                :disabled="isDisabled"
              >
                <a-select-option v-for="form in forms" :key="form.id">
                  {{ form.name }}
                </a-select-option>
              </a-select>
            </a-form-model-item>

            <a-form-model-item
              prop="method_id"
              label="Способ проведения занятия"
              key="method_id"
              :validateStatus="fields['method_id'].validateStatus"
              :help="fields['method_id'].help"
            >
              <a-select
                v-model="form.method_id"
                :disabled="!form.form_id || isDisabled"
                allow-clear
                @change="fieldChanged($event, 'method_id')"
              >
                <a-select-option v-for="method in methods" :key="method.id">
                  {{ method.name }}
                </a-select-option>
              </a-select>
            </a-form-model-item>

            <a-form-model-item
              prop="comment"
              label="Описание"
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
                :disabled="isDisabled"
              />
            </a-form-model-item>

            <a-form-model-item
              prop="job_files"
              label="Прикрепленные файлы"
              key="job_files"
              :validateStatus="fields['job_files'].validateStatus"
              :help="fields['job_files'].help"
            >
              <a-upload
                multiple
                list-type="picture"
                :file-list="form.job_files"
                :remove="handleRemoveJobFile"
                :before-upload="beforeUploadJobFile"
                class="job-details__body__form-files"
                :disabled="isDisabled"
              >
                <a-button :disabled="isDisabled">
                  <a-icon type="upload" /> Прикрепить файл
                </a-button>
              </a-upload>
            </a-form-model-item>

            <a-form-model-item
              class="job-details__body__form-ok"
              :wrapper-col="{ offset: 6 }"
            >
              <a-button
                icon="check"
                type="primary"
                @click="saveJob"
                :disabled="isDisabled"
                >Сохранить параметры занятия</a-button
              >
            </a-form-model-item>
          </a-form-model>
          <div v-if="activeTab == 2" class="job-details__wrapper">
            <div class="job-details__label" v-if="reportForm.marks.length">
              Уровень освоения
            </div>
            <div class="job-details__reports">
              <div
                class="job-details__report"
                v-for="report in reportForm.marks"
                :key="report.id"
              >
                <div class="job-details__report-name">
                  {{ report.skill.area_number }}.{{
                    report.skill.direction_number
                  }}. {{ report.skill.name }}
                </div>
                <div class="job-details__report-marks">
                  <div
                    class="job-details__report-mark"
                    v-for="i in 3"
                    :key="i"
                    :class="{ current: report.mark == i - 1 }"
                    :style="{ 'background-color': getColorByMark(i - 1) }"
                    @click="setReportMark(report, i - 1)"
                  ></div>
                </div>
              </div>
            </div>
            <a-input
              v-model="reportForm.report_comment"
              class="job-details__report_comment"
              allow-clear
              placeholder="Результат проведения занятия"
              :auto-size="{ minRows: 4, maxRows: 10 }"
              type="textarea"
              :disabled="isDisabled"
            />
            <a-button
              icon="check"
              type="primary"
              @click="saveReport"
              :disabled="isDisabled"
            >
              Сохранить отчет
            </a-button>
          </div>
        </div>
      </div>
    </div>
  </a-spin>
</template>

<script>
import moment from "moment";
import getColorByMark from "@/mixins/getColorByMark";
import { mapActions, mapGetters } from "vuex";
import patch from "@/middleware/patch";

export default {
  name: "JobDetails",
  mixins: [getColorByMark],
  props: {},
  data() {
    return {
      loading: true,
      activeTab: "1",

      job: null,
      form: {
        topic: "",
        reports: [],
        form_id: null,
        method_id: null,
        comment: "",
        job_files: [],
      },

      reportForm: {
        marks: [],
        report_comment: "",
      },

      layout: {
        labelCol: { span: 6 },
        wrapperCol: { span: 14 },
      },

      fields: {
        topic: {
          validateStatus: "",
          help: "",
        },
        reports: {
          validateStatus: "",
          help: "",
        },
        form_id: {
          validateStatus: "",
          help: "",
        },
        method_id: {
          validateStatus: "",
          help: "",
        },
        comment: {
          validateStatus: "",
          help: "",
        },
        job_files: {
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
      userInfo: "auth/getUserInfo",
    }),

    methods() {
      for (let form of this.forms) {
        if (form.id == this.form.form_id) {
          return form.methods.slice();
        }
      }
      return [];
    },

    isDisabled() {
      return (
        !this.userInfo.staff ||
        (!this.userInfo.staff &&
          this.job &&
          this.userInfo.id !== this.job.specialist.id)
      );
    },
  },
  methods: {
    ...mapActions({
      fetchAreas: "skills/fetchAreas",
      fetchForms: "forms/fetchForms",
    }),

    fieldChanged(value, key) {
      if (key == "form_id") {
        this.form.method_id = null;
      }
      this.fields[key].validateStatus = "";
      this.fields[key].help = "";
    },

    setReports(values, labels) {
      this.form.reports.splice(0);
      for (let value of values) {
        this.form.reports.push(value);
      }
      this.fieldChanged(values, "reports");
    },

    goBack() {
      this.$router.go(-1);
    },
    setJobFormData(job) {
      this.form.topic = job.topic;
      this.form.reports.splice(0);
      this.form.reports = job.reports.map((report) => {
        return report.skill_id;
      });
      this.form.form_id = job.method ? job.method.form_id : null;
      this.form.method_id = job.method ? job.method.id : null;
      this.form.comment = job.comment;
      this.form.job_files.splice(0);
      for (let job_file of job.job_files) {
        this.form.job_files.push({
          uid: job_file.id,
          name: job_file.name,
          status: "done",
          url: job_file.file,
        });
      }

      this.reportForm.marks = job.reports.slice();
      this.reportForm.report_comment = job.report_comment;
    },
    async fetchJob() {
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
    async saveJob() {
      this.$refs.jobForm.validate(async (valid) => {
        if (valid) {
          try {
            this.loading = true;

            const formData = new FormData();
            formData.append("topic", this.form.topic);
            formData.append("reports", this.form.reports);
            formData.append(
              "method_id",
              this.form.method_id ? this.form.method_id : ""
            );
            formData.append("comment", this.form.comment);

            let allFilesIds = [];
            this.form.job_files.forEach((file) => {
              allFilesIds.push(file.uid);
              if (file.status != "done") {
                formData.append(file.uid, file);
              }
            });
            formData.append("files", allFilesIds);

            let res = await patch(
              this.$axios,
              `/api/jobs/${this.$route.params.id}/`,
              formData
            );
            if (res.status === 200) {
              this.$message.success("Параметры занятия сохранены");
              await this.fetchJob();
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

    setReportMark(report, mark) {
      if (report.mark == mark) {
        report.mark = null;
      } else {
        report.mark = mark;
      }
    },
    async saveReport() {
      this.loading = true;
      try {
        let res = await patch(
          this.$axios,
          `/api/jobs/${this.$route.params.id}/`,
          this.reportForm
        );
        if (res.status === 200) {
          this.$message.success("Отчет сохранен");
          await this.fetchJob();
        } else if (res.status === 400) {
          this.$message.error("Проверьте введённые данные");
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.loading = false;
      }
    },

    handleRemoveJobFile(file) {
      const index = this.form.job_files.indexOf(file);
      const newFileList = this.form.job_files.slice();
      newFileList.splice(index, 1);
      this.form.job_files = newFileList;
    },
    beforeUploadJobFile(file) {
      this.form.job_files = [...this.form.job_files, file];
      return false;
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

    fetches.push(this.fetchJob());

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
  },
  beforeDestroy() {},
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
      flex: 1
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


  &__wrapper
    display: flex
    flex-direction: column
    padding: 0 20%
    align-items: flex-end
  &__label
    font-size: 18px
    font-weight: bold
    margin-bottom: 16px
  &__reports
    display: flex
    width: 100%
    flex-direction: column
    margin-bottom: 10px
    max-height: 400px
    overflow-y: auto

  &__report
    display: flex
    flex-direction: row
    align-items: center
    justify-content: space-between
    margin-bottom: 10px
    padding-bottom: 10px
    border-bottom: 1px solid #e8e8e8
    &-name
      padding-left: 10px
      font-size: 18px
    &-marks
      display: flex
      flex-direction: row
    &-mark
      height: 40px
      width: 40px
      border-radius: 20px
      background: #ccc
      box-shadow: 0 1px 3px 1px #dedede
      margin-right: 10px
      cursor: pointer
      opacity: 0.2
      transition: 0.2s ease-out
      &:hover
        opacity: 1
      &.current
        opacity: 1

  &__report_comment
    margin-bottom: 24px

.job-details__header-left-block
  flex: 1

.job-details__header-center-block
  display: flex
  justify-content: center
  align-items: center
  font-size: 1rem

.job-details__header-right-block
  flex: 1

.job-details__content
  display: flex
  flex-direction: column
  flex: 1
  overflow: hidden

.job-details__tabs-holder
  display: flex
  justify-content: center

.job-details__tab_content
  flex: 1
  overflow: auto
</style>
