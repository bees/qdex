<template>
  <div>
    <p>
      {{ $t('messages.welcome') }}
    </p>
    <p>
      <router-link to="/hello/bourgeon">{{ $t('buttons.hello') }}</router-link>
    </p>
  </div>
</template>

<script>
export default {}
</script>

<style>
</style>
