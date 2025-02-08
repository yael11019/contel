<template>
    <div class="menu-wrapper">
      <!-- Fondo oscuro detrás del menú -->
      <div class="backdrop"></div>
  
      <transition name="slide">
        <div class="menu">
          <!-- Botón de cierre (X) -->
           <image>
            <img src="@/assets/contelLogo.png" alt="icon" class="btn-icon">
           </image>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="currentColor"
            class="bi bi-x-circle-fill close"
            viewBox="0 0 16 16"
            @click="emit('closeMenu')"
          >
            <path
              d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"
            />
          </svg>
  
          <!-- Opciones del menú como list-group -->
          <ul class="list-group">
            <li class="list-group-item">Inicio</li>
            <li class="list-group-item">Servicios</li>
            <li class="list-group-item">Nosotros</li>
            <li class="list-group-item">Contacto</li>
          </ul>
        </div>
      </transition>
    </div>
  </template>
  
    <script setup>
    import { defineEmits } from 'vue';
    
    const emit = defineEmits(['closeMenu']);

    </script>

  <style scoped>
  .close {
    display: block;
    margin-left: auto; /* Lo alinea a la derecha */
    cursor: pointer;
  }
  
  /* Estilos de la lista para que los cuadros salgan más abajo */
  .list-group {
    margin-top: 20px; /* Ajusta la distancia desde el icono de cierre */
  }
  
  /* Menú lateral */
  .menu {
    position: fixed;
    top: 0;
    left: 0;
    width: 50%;
    height: 100vh;
    background-color: white;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
    z-index: 10002;
    padding: 20px;
  }
  </style>
  