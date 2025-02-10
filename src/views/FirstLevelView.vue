<template>
    <HeaderComponent @toggleMenu="toggleMenu" />
    <MenuComponent 
      v-if="isMenuOpen" class="menu" 
      @closeMenu="toggleMenu"
    />
    <FirstLevelComponent 
      :categoryName="categoryName" 
    />
    <p v-if="isMenuOpen"> Funciona</p>
    <FooterComponent :source="'Home'" />
  </template>
  
  <script setup>
  import { ref, defineProps } from 'vue';
  import HeaderComponent from '@/components/HeaderComponent.vue';
  import MenuComponent from '@/components/MenuComponent.vue';
  import FooterComponent from '@/components/FooterComponent.vue';
  import FirstLevelComponent from '@/components/FirstLevelComponent.vue';

  const isMenuOpen = ref(false);

  defineProps({
    categoryName: String,
  })
  
  const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value;
    console.log("Estado del menú:", isMenuOpen.value); // Verifica si cambia correctamente
  };
  </script>
  
  
  
  
  <style scoped>
  body, html {
    height: 100%;
    margin: 0;
    display: flex;
    flex-direction: column;
  }
  
  main {
    flex-grow: 1; /* Empuja el footer hacia abajo */
  }
  
  footer {
    margin-top: auto;
    width: 100%;
    max-width: 100%;
  }
  
  .home {
    position: static; /* Cambia de relative a static si sigue dando problemas */
  }
  
  .menu {
    z-index: 9999;
  }

  .category-name {
    color: red;
    margin-top: 10px;
  }
  </style>