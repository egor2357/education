<template>
  <a-modal
    okText="Сохранить"
    cancelText="Отмена"
    :visible="true"
    :title="title"
    @cancel="closeModal(null)"
    @ok="handleOk"
    @confirmLoading="loadingButton">
    <a-form-model :model="form" v-bind="layout" :rules="rules" ref="form">

<!--       <a-form-model-item prop="date" label="Дата" key="date"
        :validateStatus="fields['date'].validateStatus" :help="fields['date'].help">
        <a-date-picker
          v-model="form.date"
          type="date"
          placeholder="Выберите дату"
          format="DD.MM.YYYY"
          style="width: 100%;"
          @change="fieldChanged($event, 'date')"
        />
      </a-form-model-item>
 -->
    </a-form-model>

  </a-modal>
</template>

<script>
import consts from "@/const";
import post from "@/middleware/post";
import put from "@/middleware/put";

export default {
  name: "JobOptionModal",
  props: {
    editableData: {
      type: Object,
      default: null,
    }
  },
  data() {
    return {
      form: {
      },
      title: "",
      layout: {
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
      },
      fields: {
        // 'date': {
        //   validateStatus: "",
        //   help: "",
        // },
      },
      rules: {
        // date: [
        //   {
        //     trigger: "change",
        //     required: true,
        //     message: "Пожалуйста, выберите дату",
        //   },
        // ],
      },

      loadingButton: false,
    };
  },
  computed: {

  },
  methods: {
    async fieldChanged(val, field_key) {
      this.fields[field_key].validateStatus = "";
      this.fields[field_key].help = "";
    },

    closeModal(jobDate=null){
      this.$emit('closeModal', jobDate);
    },

    async handleOk() {
      this.loadingButton = true;
      // this.$refs.form.validate(async (valid) => {
      //   if (valid) {
      //     try {
      //       let successCode = 0;
      //       let res = null;
      //       let successMessage = "";
      //       this.form.date = this.form.date.format("YYYY-MM-DD");
      //       if (this.form.id) {
      //         successCode = 200;
      //         successMessage = "Занятие успешно изменено";
      //         res = await put(this.$axios, `/api/jobs/${this.form.id}/`, this.form);
      //       } else {
      //         successCode = 201;
      //         successMessage = "Занятие успешно добавлено";
      //         res = await post(this.$axios, "/api/jobs/", this.form);
      //       }

      //       if (res.status === successCode) {
      //         this.$message.success(successMessage);
      //         this.closeModal(moment(this.form.date, "YYYY-MM-DD"));
      //       } else if (res.status === 400) {
      //         this.$message.error("Проверьте введённые данные");
      //         for (let key in res.data) {
      //           this.fields[key].validateStatus = "error";
      //           this.fields[key].help = res.data[key];
      //         }
      //       } else {
      //         this.$message.error("Произошла ошибка");
      //       }
      //     } catch (e) {
      //       this.$message.error("Произошла ошибка");
      //     } finally {
      //       this.form.date = moment(this.form.date, "YYYY-MM-DD");
      //       this.loadingButton = false;
      //     }
      //   } else {
      //     return false;
      //   }
      // });
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
      this.title = "Изменение плана занятия";
      // this.form.id = this.editableData.id
      // this.form.date = moment(this.editableData.date, "YYYY-MM-DD");
    } else {
      this.title = "Добавление плана занятия";
    }
    document.addEventListener("keydown", this.keydown);
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keydown);
  }
};
</script>

<style lang="sass"></style>
