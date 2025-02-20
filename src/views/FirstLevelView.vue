<template>
  <div class="app">
    <HeaderComponent @toggleMenu="toggleMenu" class="header" />
    
    <MenuComponent 
      v-if="isMenuOpen" class="menu" 
      @closeMenu="toggleMenu"
    />
    
    <div class="content">
      <FirstLevelComponent :categoryName="categoryName" />
      <p v-if="isMenuOpen">Funciona</p>
    </div>
    
    <FooterComponent :source="'Home'" class="footer" />
  </div>
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
});

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
  console.log("Estado del menú:", isMenuOpen.value);
};
</script>

<style scoped>
/* 📌 Layout base */
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 📌 Header siempre arriba */
.header {
  position: sticky;
  top: 0;
  width: 100%;
  z-index: 1000;
}

/* 📌 Footer siempre abajo */
.footer {
  position: sticky;
  bottom: 0;
  width: 100%;
  background: white;
  z-index: 1000;
}

/* 📌 Contenido con scroll */
.content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
  box-sizing: border-box;
}
</style>
