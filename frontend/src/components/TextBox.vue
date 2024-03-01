<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
})
</script>

<template>
    <div>
        <p id="rcorners">{{ msg }}</p>
    </div>
</template>

<style scoped>
#rcorners {
    display: inline-block;
    vertical-align: middle;
    border-radius: 25px;
    background: #3B3B3B;
    padding: 20px;
    width: 200px;
    height: 150px;
    margin-left: 11px;
    margin-right: 11px;
}
</style>
