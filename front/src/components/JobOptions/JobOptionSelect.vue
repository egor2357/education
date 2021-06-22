<template>
  <a-modal
    width="1000px"
    :visible="true"
    :title="'Выбор варианта проведения занятия'"
    :footer="null"
    @cancel="closeModal(null)"
    :body-style="{'max-height': '700px', 'overflow-y': 'auto'}">
    <div class="job-option-select__cards" v-if="options.length">
      <div class="job-option-select__card" v-for="option in options" :key="option.id">
        <job-option :option="option">
          <div class="job-option-header-actions">
            <div class="job-option-header-action"
              @click="closeModal(option.id)">
              Выбрать
            </div>
          </div>
        </job-option>
      </div>
    </div>
    <div v-else>
      <a-empty :image="simpleImage"/>
    </div>

  </a-modal>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import JobOption from "@/components/JobOptions/JobOption";
import { Empty } from 'ant-design-vue';

export default {
  name: "JobOptionSelect",
  components: {
    JobOption,
  },
  props: {
    options: {
      type: Array,
      default: ()=>{return [];}
    }
  },
  data() {
    return {
    };
  },
  computed: {
  },
  methods: {
    closeModal(optionId=null){
      this.$emit('closeModal', optionId);
    },
  },
  beforeCreate() {
    this.simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
  },
  async created() {
    let fetches = [];

    this.loading = true;
    await Promise.all(fetches);
    this.loading = false;
  },
};
</script>

<style lang="sass">
.job-option-select
  &__cards
    height: 100%
    overflow-y: auto

</style>
