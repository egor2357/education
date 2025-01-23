<template>
  <a-result status="404" title="404" sub-title="Запрашиваемой страницы не существует.">
    <template #extra>
      <a-button type="primary">
        <router-link to="/">
          На главную
        </router-link>
      </a-button>
    </template>
  </a-result>
</template>

<script>
  export default {
    name: "Page404"
  }
</script>

<style scoped>

</style>