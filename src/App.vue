<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
#app {
  font-family: 'myriad-pro', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin: 0;
  width: 100%;
  overflow-x: hidden; /* Asegura que nada sobresalga */
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden; /* Evita que haya scroll horizontal */
}


/* Corregir cualquier posible desbordamiento */
* {
  max-width: 100%; /* Evita que elementos sobrepasen el ancho */
  box-sizing: border-box; /* Asegura que el padding y border no aumenten el tamaño */
}

body {
  position: relative
}
</style>
