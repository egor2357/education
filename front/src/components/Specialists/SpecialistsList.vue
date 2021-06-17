<template>
  <div class="users-container">
    <template v-if="!displayTabs">
      <div class="top-bar">
        <div class="top-bar__side-block left">
          <a-radio-group v-model="staffSelected">
            <a-radio-button :value="false"> Специалисты </a-radio-button>
            <a-radio-button :value="true"> Администраторы </a-radio-button>
          </a-radio-group>
        </div>
        <div class="title">Пользователи</div>
        <div class="top-bar__side-block right">
          <a-button
            icon="plus"
            type="secondary"
            @click="
              displayModal = true;
              modalAdding = true;
            "
          >
          Добавить
        </a-button>
        </div>
      </div>
      <div class="specialists-container">
        <a-list
          :loading="loading"
          item-layout="horizontal"
          class="specialists-container__list"
        >
          <template v-for="item in specialists">
            <a-list-item
              v-if="item.user && item.user.is_staff === staffSelected"
              :key="item.id"
            >
              <div slot="actions">
                <a
                  @click="
                    displayModal = true;
                    modalEditableData = item;
                    modalAdding = false;
                  "
                  >Изменить</a
                >
                <a-divider type="vertical" />
                <a @click="displayDelete(item)">Удалить</a>
                <br />
                <a v-if="!staffSelected" @click="displayActivitySkill(item.id)">
                  Виды деятельности / навыки
                </a>
              </div>

              <a-list-item-meta style="width: 50px">
                <template slot="title">
                  <span class="specialist-label">{{
                    item.surname
                      ? formatSpecialistFull(item)
                      : item.user.username
                  }}</span>
                </template>
                <template slot="description" v-if="!staffSelected">
                  <div class="activities">
                    <template v-for="activity in item.activities">
                      <div
                        class="activity-block"
                        :key="activity.activity.id"
                        :style="{
                          'background-color': `${activity.activity.color}4d`,
                          border: `1px solid ${activity.activity.color}99`,
                        }"
                        v-if="activity.is_main"
                      >
                        <span class="activity-label">{{
                          activity.activity.name
                        }}</span>
                      </div>
                    </template>
                  </div>
                  <template v-if="item.hasAdditionalActivity">
                    <a-divider orientation="left">
                      Дополнительные виды деятельности
                    </a-divider>
                    <div class="activities">
                      <template v-for="activity in item.activities">
                        <div
                          class="activity-block"
                          :key="activity.activity.id"
                          :style="{
                            'background-color': `${activity.activity.color}4d`,
                            border: `1px solid ${activity.activity.color}99`,
                          }"
                          v-if="!activity.is_main"
                        >
                          <span class="activity-label">{{
                            activity.activity.name
                          }}</span>
                        </div>
                      </template>
                    </div>
                  </template>
                </template>
              </a-list-item-meta>
            </a-list-item>
          </template>
        </a-list>
      </div>
    </template>
    <ModalSpecialist
      v-if="displayModal"
      :adding="modalAdding"
      :editableData="modalEditableData"
      @close="displayModal = false"
      :staffSelected="staffSelected"
      @closeSuccess="
        displayModal = false;
        fetchSpecialists();
      "
    />
    <ActivitySkillTabs
      :currentUser="currentUser"
      v-if="displayTabs"
      @goBack="closeTabs"
    />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import ModalSpecialist from "@/components/Specialists/ModalSpecialist";
import ActivitySkillTabs from "@/components/Specialists/ActivitySkillTabs";
import common from "@/mixins/common";
export default {
  name: "SpecialistsList",
  components: {
    ModalSpecialist,
    ActivitySkillTabs,
  },
  mixins: [common],
  data() {
    return {
      loading: false,
      displayModal: false,
      modalAdding: false,
      modalEditableData: {},
      staffSelected: false,
      displayTabs: false,
      currentUser: {},
    };
  },
  async created() {
    this.loading = true;
    await this.fetchSpecialists();
    this.loading = false;
  },
  methods: {
    ...mapActions({
      fetchSpecialists: "specialists/fetchSpecialists",
    }),
    displayDelete(item) {
      let that = this;
      this.$confirm({
        title: `Вы действительно хотите удалить специалиста ${
          item.surname
            ? this.formatSpecialistFull(item)
            : item.user.username
        }?`,
        content: ``,
        okType: "danger",
        onOk() {
          that.deleteRecord(item.id);
        },
      });
    },
    async deleteRecord(id) {
      this.loading = true;
      try {
        let res = await this.$store.dispatch(
          "specialists/deleteSpecialist",
          id
        );
        if (res.status === 204) {
          this.$message.success("Специалист успешно удалён");
          this.fetchSpecialists();
        } else {
          this.$message.error("Произошла ошибка");
        }
      } catch (e) {
        this.$message.error("Произошла ошибка");
      } finally {
        this.loading = false;
      }
    },
    displayActivitySkill(userId) {
      this.currentUser = this.specialists.find(user => user.id == userId) || {};
      this.displayTabs = true;
    },
    async closeTabs() {
      this.displayTabs = false;
    },
  },
  computed: {
    ...mapGetters({
      specialists: "specialists/getSpecialists",
      specialistsFetched: "specialists/getFetched"
    }),
  },
};
</script>

<style lang="sass">
.users-container
  display: flex
  height: 100%
  flex-direction: column

  .top-bar
    display: flex
    margin-bottom: 10px
    line-height: 32px

  .top-bar__side-block
    flex: 1

    &.right
      text-align: right
.title
  text-align: center
  font-size: 1rem

.specialists-container
  flex: 1
  overflow: auto
  display: flex
  justify-content: center

  .specialists-container__list
    min-width: 900px
  .specialist-label
    font-size: 1.1rem
  .ant-list-item-meta-description
    .ant-divider
      margin: 0
    .activities
      display: flex
      flex-wrap: wrap
      .activity-block
        margin: 5px
        padding: 3px
        -webkit-border-radius: 4px
        -moz-border-radius: 4px
        border-radius: 4px
        .activity-label
          margin: 5px
          color: #111111
</style>
