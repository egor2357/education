<template>
  <a-row type="flex" justify="center" align="middle" style="background-color: #f0f2f5; height: 100vh;">
    <a-col :xs="{span: 24}" :sm="{span: 22}" :md="{span: 16}" :lg="{span: 12}" :xl="{span: 10}" :xxl="{span: 7}">
      <LoginForm class="login-form"/>
    </a-col>
  </a-row>
</template>

<script>
  import LoginForm from '@/components/LoginForm'
  export default {
    name: "Login",
    components: {
      LoginForm
    },
  }
</script>

<style lang="sass">
</style>