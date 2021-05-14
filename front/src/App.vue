<template>
  <a-config-provider :locale="ru_RU">
    <div id="app">
      <Layout v-if="isAuth" />
      <Login v-else-if="isAuth === false" />
    </div>
  </a-config-provider>
</template>

<script>
import Layout from "@/components/Layout";
import Login from "@/views/Login";
import { mapGetters } from "vuex";
import ru_RU from 'ant-design-vue/lib/locale-provider/ru_RU';
import moment from 'moment';
import 'moment/locale/ru';

moment.locale('ru');
export default {
  name: "App",
  components: {
    Layout,
    Login,
  },
  data() {
    return {
      ru_RU
    }
  },
  created() {
    document.title = "Обучение";
  },
  computed: {
    ...mapGetters({
      isAuth: "auth/getIsAuth",
    }),
  },
};
</script>

<style lang="sass"></style>
