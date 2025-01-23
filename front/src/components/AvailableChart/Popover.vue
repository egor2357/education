<template>
  <a-popover title="Виды деятельности" placement="right">
    <template slot="content">
      <div class="activities-popover">
        <template v-for="activity in data.specialist.activities">
          <div
            class="activity-block-popover"
            :key="activity.activity.id"
            :style="{
              'background-color': `${activity.activity.color}4d`,
              border: `1px solid ${activity.activity.color}99`,
            }"
            v-if="activity.is_main"
          >
            <span class="activity-label">{{ activity.activity.name }}</span>
          </div>
        </template>
      </div>
      <template v-if="data.specialist.hasAdditionalActivity">
        <a-divider orientation="center" class="activities-divider">
          Дополнительные виды деятельности
        </a-divider>
        <div class="activities-popover">
          <template v-for="activity in data.specialist.activities">
            <div
              class="activity-block-popover"
              :key="activity.activity.id"
              :style="{
                'background-color': `${activity.activity.color}4d`,
                border: `1px solid ${activity.activity.color}99`,
              }"
              v-if="!activity.is_main"
            >
              <span class="activity-label-popover">{{
                activity.activity.name
              }}</span>
            </div>
          </template>
        </div>
      </template>
    </template>
    <span> {{ data.name }} </span>
  </a-popover>
</template>

<script>
export default {
  name: "Popover",
  props: {
    data: Object,
  },
};
</script>

<style lang="sass">
.activities-popover
  display: flex
  flex-wrap: wrap
  max-width: 300px
  .activity-block-popover
    margin: 3px
    padding: 3px
    -webkit-border-radius: 4px
    -moz-border-radius: 4px
    border-radius: 4px
    .activity-label-popover
      margin: 5px
      color: #111111
.ant-divider
  &.activities-divider
    font-size: 0.8rem
    margin: 0
    max-width: 330px
    &::before
      position: unset
</style>
