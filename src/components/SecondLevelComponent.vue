<template>
  <div class="container">
    <p class="category-name">
      - {{ categoryName }} -
    </p>
    
    <div class="image-container">
      <img src="@/assets/comercio3.jpg" class="rectangular-image" alt="Rectángulo" />
      <img src="@/assets/contel.png" class="circular-image" alt="Círculo" />
    </div>

    <div class="merchant-information">
      <div class="principal-information"> 
        <h5>{{ merchantName }}</h5>
        <p>
          Cel. (453) 999 999, Tel. (453) 999 999
          <br>Calle, número, colonia, C.P 
          <br>Municipio
          <br>yael110@live.com.mx
        </p>
        <div class="categories mt-4">
          <ul class="row list-unstyled text-center circle-container">
            <li 
              v-for="webSite in webSites" 
              :key="webSite.id" 
              class="col-2 category-item" 
              @click="goToUrl(webSite.url)"
              style="cursor: pointer;"
            >
              <div class="circle">
                <span v-html="webSite.icon"></span>
              </div>
            </li> 
          </ul>
        </div>
      </div>

      <div class="secondary-information">
        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-book" viewBox="0 0 16 16">
          <path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783"/>
        </svg>
        <h5>Catálogo</h5>
        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-qr-code" viewBox="0 0 16 16">
          <path d="M2 2h2v2H2z"/>
          <path d="M6 0v6H0V0zM5 1H1v4h4zM4 12H2v2h2z"/>
          <path d="M6 10v6H0v-6zm-5 1v4h4v-4zm11-9h2v2h-2z"/>
          <path d="M10 0v6h6V0zm5 1v4h-4V1zM8 1V0h1v2H8v2H7V1zm0 5V4h1v2zM6 8V7h1V6h1v2h1V7h5v1h-4v1H7V8zm0 0v1H2V8H1v1H0V7h3v1zm10 1h-1V7h1zm-1 0h-1v2h2v-1h-1zm-4 0h2v1h-1v1h-1zm2 3v-1h-1v1h-1v1H9v1h3v-2zm0 0h3v1h-2v1h-1zm-4-1v1h1v-2H7v1z"/>
          <path d="M7 12h1v3h4v1H7zm9 2v2h-3v-1h2v-1z"/>
        </svg>
        <h5>Código QR</h5>
      </div>
    </div>

    <div class="services">
      <h4>Servicios/productos:</h4>
      <div class="rectangle">
        Lic. en Derecho egresada de la U.M.S.N.H.
        <br>Atención jurídica en materia civil, penal y familiar.
        <br>Asesoría para constitución de sociedades.
        <br>Horario:
        <br>Lunes a viernes de 10 a 2 pm y de 4 a 7 pm.
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { webSites } from '@/store/webSites';

defineProps({
  merchantName: String,
  categoryName: String,
})

const goToUrl = (url) => {
  window.open(url, '_blank');
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.category-name {
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 10px;
}

.image-container {
  display: flex;
  justify-content: center;
  position: relative;
  width: 450px; /* Ajusta según necesites */
  margin-top: 10px;
}

.rectangular-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
}

.circular-image {
  position: absolute;
  bottom: -40px;
  right: 20%; 
  transform: translateX(50%);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.merchant-information {
  display: flex;
  justify-content: space-between; /* Espacio entre los bloques */
  align-items: stretch; /* Asegura que ambos bloques tengan la misma altura */
  width: 100%;
  padding: 20px;
  margin-top: 20px;
}

.principal-information,
.secondary-information {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Distribuye el contenido en ambos bloques */
}

.principal-information {
  width: 48%; /* Controla el tamaño del bloque principal */
  text-align: center; /* Alineación del texto a la izquierda */
  align-items: center; /* Alineación del contenido al centro */
}

.secondary-information {
  width: 48%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.circle-container {
  display: flex;
  justify-content: space-between; /* Distribuye los círculos de manera uniforme */
  width: 100%;  /* Asegura que los círculos se distribuyan a lo largo del contenedor */
  margin-bottom: 10px;
}

.circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 50px; /* Asegura el tamaño mínimo */
  text-align: center; /* Centra el texto dentro de los círculos */
}

.secondary-information svg {
  margin-bottom: 10px;
}

.secondary-information h5 {
  margin-bottom: 15px;
}

/* Ajuste para mantener tamaño de círculos en móviles */
@media (max-width: 576px) {
  .circle {
    width: 50px;
    height: 50px;
  }
}

@media (max-width: 768px) {
  .merchant-information {
    flex-direction: column;
    align-items: center;
  }

  .principal-information,
  .secondary-information {
    width: 100%;
    margin-bottom: 20px;
  }

  .rectangular-image {
    width: 100%;
    height: auto;
  }
}


.services {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-top: 20px;
}

.rectangle {
  width: 450px;
  height: 150px;
  background-color: white;
  border: 2px solid black;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}


.services {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-top: 20px;
}

.rectangle {
  width: 450px;
  height: 150px;
  background-color: white;
  border: 2px solid black;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
</style>
