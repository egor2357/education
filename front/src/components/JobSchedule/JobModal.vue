<template>
  <a-modal
    okText="Сохранить"
    cancelText="Отмена"
    :visible="true"
    :title="title"
    @cancel="$emit('closeModal')"
    @ok="handleOk"
    @confirmLoading="loadingButton">
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">

      <a-form-model-item prop="date" label="Дата" key="date"
        validateStatus="" help="">
        <a-date-picker
          v-model="form.date"
          type="date"
          placeholder="Выберите дату"
          style="width: 100%;"
        />
      </a-form-model-item>

      <a-form-model-item prop="activity_id" label="Вид деятельности" key="activity_id"
        validateStatus="" help="">
        <a-select v-model="form.activity_id" @change="form.specialist_id=null">
          <a-select-option v-for="activity in activities" :key="activity.id">
            {{ activity.name }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item prop="specialist_id" label="Специалист" key="specialist_id"
        validateStatus="" help="">
        <a-select v-model="form.specialist_id">
          <a-select-option v-for="specialist in filteredSpecialists" :key="specialist.id">
            {{ specialist.__str__ }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item prop="start_time" label="Время" key="start_time"
        validateStatus="" help="">
        <a-input
          v-model="form.start_time"
          type="time"
        />
      </a-form-model-item>

    </a-form-model>

  </a-modal>
</template>

<script>
import consts from "@/const";
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
    async handleOk() {
      this.loadingButton = true;
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          // let dispatchName = "";
          // let successCode = 0;
          // let successMessage = "";

          // if (this.adding) {
          //   dispatchName = "schedule/addJob";
          //   successCode = 201;
          //   successMessage = "Занятие успешно добавлено";
          // } else if (!this.adding) {
          //   dispatchName = "schedule/editJob";
          //   successCode = 200;
          //   successMessage = "Занятие успешно изменено";
          // }
          // try {
          //   let res = await this.$store.dispatch(dispatchName, this.form);
          //   if (res.status === successCode) {
          //     this.$message.success(successMessage);
          //     this.$emit("closeModal");
          //   } else if (res.status === 400) {
          //     this.$message.error("Проверьте введённые данные");
          //     for (let key in res.data) {
          //       this.fields.forEach((field) => {
          //         if (field.name === key) {
          //           field.validateStatus = "error";
          //           field.help = res.data[key];
          //         }
          //       });
          //     }
          //   } else {
          //     this.$message.error("Произошла ошибка");
          //   }
          // } catch (e) {
          //   this.$message.error("Произошла ошибка");
          // } finally {
          //   this.loadingButton = false;
          // }
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
