<template>
  <router-view />
</template>

<script>
export default {
  name: "Jobs",
  created() {
    this.$store.commit("schedule/setSelectedDay", null)
  }
};
</script>

<style lang="sass"></style>
