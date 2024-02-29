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
    border-radius: 25px;
    background: #3B3B3B;
    padding: 20px;
    width: 200px;
    height: 150px;
    margin-top: 25px;
    margin-bottom: 25px;
    margin-left: 20px;
    margin-right: 20px;
}
</style>
