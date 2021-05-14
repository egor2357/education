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
  Row,
  Col,
  Card,
  FormModel,
  Input,
  ConfigProvider
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
Vue.use(Row);
Vue.use(Col);
Vue.use(Card);
Vue.use(FormModel);
Vue.use(Input);
Vue.use(ConfigProvider);

Vue.prototype.$message = message;

export default Vue;
