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
  ConfigProvider,
  Dropdown,
  Popconfirm,
  Result,
  InputNumber,
  Tabs,
  List,
  Avatar
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
Vue.use(Dropdown);
Vue.use(Popconfirm);
Vue.use(Result);
Vue.use(InputNumber);
Vue.use(Tabs);
Vue.use(List);
Vue.use(Avatar);

Vue.prototype.$message = message;
Vue.prototype.$confirm = Modal.confirm;

export default Vue;
