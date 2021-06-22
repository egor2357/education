<template>
  <a-card>
    <div slot="title" style="text-align: center">
      <div><b>Обучение</b></div>
      Авторизация
    </div>
    <a-form-model :model="form" :rules="rules">
      <a-form-model-item key="username" prop="username">
        <a-input
          v-model="form.username"
          placeholder="Имя пользователя"
          @keyup.enter="login"
        >
          <a-icon
            slot="prefix"
            type="user"
            style="color: rgba(0, 0, 0, 0.25)"
          />
        </a-input>
      </a-form-model-item>
      <a-form-model-item key="password" prop="password">
        <a-input
          v-model="form.password"
          type="password"
          placeholder="Пароль"
          @keyup.enter="login"
        >
          <a-icon
            slot="prefix"
            type="lock"
            style="color: rgba(0, 0, 0, 0.25)"
          />
        </a-input>
      </a-form-model-item>
      <a-form-model-item style="text-align: center; margin-bottom: 0">
        <a-button type="primary" @click="login" :loading="loadingButton">
          Войти
        </a-button>
      </a-form-model-item>
    </a-form-model>
  </a-card>
</template>

<script>
import displayErrors from "@/middleware/displayErrors";
export default {
  name: "LoginForm",
  data() {
    return {
      form: {
        username: null,
        password: null,
      },
      rules: {
        username: [
          {
            required: true,
            trigger: "blur",
            message: "Пожалуйста, введите имя пользователя",
          },
        ],
        password: [
          {
            required: true,
            trigger: "blur",
            message: "Пожалуйста, введите пароль",
          },
        ],
      },
      fields: [
        {
          name: "username",
          label: "Имя пользователя",
          type: "text",
        },
        {
          name: "password",
          label: "Пароль",
          type: "password",
        },
      ],
      loadingButton: false,
    };
  },
  methods: {
    async login() {
      this.loadingButton = true;
      this.$store
        .dispatch("auth/login", this.form)
        .then((res) => {
          if (res.status === 200) {
            this.$message.success("Вход успешно выполнен");
            this.$router.push({ name: "JobWrapper" });
          } else if (res.status === 400) {
            this.$message.error("Проверьте введённые данные");
            displayErrors(this.$message, res.data, this.fields);
          } else {
            this.$message.error("Произошла ошибка");
          }
        })
        .catch(() => {
          this.$message.error("Произошла ошибка");
        })
        .finally(() => {
          this.loadingButton = false;
        });
    },
  },
};
</script>

<style scoped></style>
