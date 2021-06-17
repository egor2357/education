<template>
  <div class="activities-list">
    <a-list
      :loading="loadingList"
      item-layout="horizontal"
      :data-source="data"
      class="types-list"
    >
      <a-list-item slot="renderItem" slot-scope="item" style="height: 75px">
        <a
          slot="actions"
          @click="$emit('onEditActivity', item)"
          >Изменить</a
        >
        <a slot="actions" @click="$emit('onDeleteActivity', item)">Удалить</a>
        <a-list-item-meta style="width: 50px">
          <div
            class="type-color"
            slot="avatar"
            :style="{ 'background-color': item.color }"
          ></div>
        </a-list-item-meta>
        <span class="type-label">{{ item.name }}</span>
      </a-list-item>
    </a-list>
  </div>
</template>

<script>
export default {
  name: "TypesList",
  props: {
    data: Array,
    loadingList: Boolean,
  },
  data() {
    return {

    };
  },
};
</script>

<style lang="sass">
.activities-list
  height: 100%
  overflow: auto
  display: flex
  justify-content: center
.types-list
  min-width: 900px
  .type-color
    width: 32px
    height: 32px
    -webkit-border-radius: 16px
    -moz-border-radius: 16px
    border-radius: 16px
  .type-label
    width: 100%
    font-size: 1.1rem
</style>
