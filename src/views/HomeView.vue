<template>
  <div id="app">
    <HeaderComponent @toggleMenu="toggleMenu" />
    <MenuComponent 
      v-if="isMenuOpen" 
      class="menu" 
      @closeMenu="toggleMenu"
    />
    
    <!-- Contenedor principal -->
    <main class="content">
      <HomeComponent />
    </main>

    <FooterComponent :source="'Home'" />
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import HeaderComponent from '@/components/HeaderComponent.vue';
import MenuComponent from '@/components/MenuComponent.vue';
import HomeComponent from '@/components/HomeComponent.vue';
import FooterComponent from '@/components/FooterComponent.vue';

defineProps({
  categoryName: String,
});

const isMenuOpen = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};
</script>

<style>
/* 📌 Elimina los espacios blancos en los lados */
html, body, #app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden; /* Evita scroll horizontal */
}

/* 📌 Configuración del layout principal */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  max-width: 100%;
}

/* 📌 Permitir que el contenido crezca y evitar que choque con el footer */
.content {
  flex-grow: 1;
  width: 100%; /* Asegura que ocupe todo el ancho */
  overflow-y: auto; /* Solo el contenido tiene scroll */
  padding-top: 10px; /* Ajusta según la altura del Header */
  padding-bottom: 10px; /* Ajusta según la altura del Footer */
  box-sizing: border-box; /* Evita problemas de tamaño */
}

/* 📌 Asegurar que el Footer esté siempre al final */
footer {
  width: 100%;
  flex-shrink: 0;
  position: relative;
  z-index: 10;
  background: #fff; /* Asegura que no se sobreponga contenido */
}
</style>
