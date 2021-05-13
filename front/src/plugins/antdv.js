import Vue from "vue";
import {
  message,
  Table,
  Layout,
  Menu,
  Breadcrumb,
  Icon,
  Divider,
  Button,
  Modal,
} from "ant-design-vue";
import "ant-design-vue/dist/antd.css";

Vue.use(Table);
Vue.use(Layout);
Vue.use(Menu);
Vue.use(Breadcrumb);
Vue.use(Icon);
Vue.use(Divider);
Vue.use(Button);
Vue.use(Modal);

Vue.prototype.$message = message;

export default Vue;
