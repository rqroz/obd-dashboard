<template>
  <embed :src="endpoint" width="100%" height="800" />
</template>

<script>
export default {
  data: () => ({
    endpoint: '/dash/',
  }),
};
</script>
