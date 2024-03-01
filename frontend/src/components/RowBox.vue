<script setup>
import TextBox from './TextBox.vue'
defineProps({
  n_blocks: {
    type: Number,
    default: 0,
    required: false
  }
})
</script>

<template>
  <div class="row">
    <TextBox msg="This is a test"/>
    <TextBox msg="This is a test"/>
    <TextBox msg="This is a test"/>
    <TextBox msg="This is a test"/>
  </div>
</template>

<style scoped>
.row {
    display: flex;
    background: #181818;
    padding: 20px;
    width: 100%;
    height: 160px;
    margin-top: 11px;
    margin-bottom: 11px;
    margin-left: 0px;
    margin-right: 0px;
}
</style>
