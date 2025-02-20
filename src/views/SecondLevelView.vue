<template>
  <div class="app">
    <HeaderComponent @toggleMenu="toggleMenu" />
    <MenuComponent 
      v-if="isMenuOpen" class="menu" 
      @closeMenu="toggleMenu"
    />
    <div class="content">
      <SecondLevelComponent 
        :merchantName="merchantName" 
        :categoryName="categoryName"
      />
    </div>
    <FooterComponent :source="'Home'" class="footer" />
  </div>
  </template>
  
  <script setup>
  import { ref, defineProps } from 'vue';
  import HeaderComponent from '@/components/HeaderComponent.vue';
  import MenuComponent from '@/components/MenuComponent.vue';
  import FooterComponent from '@/components/FooterComponent.vue';
import SecondLevelComponent from '@/components/SecondLevelComponent.vue';

  const isMenuOpen = ref(false);

  defineProps({
    merchantName: String,
    categoryName: String,
  })
  
  const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value;
    console.log("Estado del menú:", isMenuOpen.value); // Verifica si cambia correctamente
  };
  </script>
  
  
  
  
  <style scoped>
 .app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  position: sticky;
  top: 0;
  width: 100%;
  z-index: 1000;
}
  
.footer {
  position: sticky;
  bottom: 0;
  width: 100%;
  background: white;
  z-index: 1000;
}
  
.content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
  box-sizing: border-box;
}

  .category-name {
    color: red;
    margin-top: 10px;
  }
  </style>