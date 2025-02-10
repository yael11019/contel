<template>
    <div class="modal fade" tabindex="-1" :class="{'show d-block': isVisible}" style="display: block;" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ name }}</h5>
            <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="categories mt-4">
                <ul class="row list-unstyled text-center">
                    <li 
                      v-for="category in subCategories" 
                      :key="category.id" 
                      class="col-4 col-md-3 category-item"
                      @click="pushToNextLevel(category)"  
                    >
                      <div class="circle">
                      </div>
                      <p class="category-name">{{ category }}</p>
                    </li>
                </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
  
  <script setup>
  import { defineProps, defineEmits, onMounted } from 'vue';
  import { useRouter } from "vue-router";

  const router = useRouter();
  
  onMounted(() => {
    console.log('ModalComponent mounted', props.isVisible);
    console.log('ModalComponent mounted', props.name);
    console.log( props.subCategories);
  });

  // Recibir el prop para controlar si el modal debe mostrarse
  const props = defineProps({
    isVisible: {
      type: Boolean,
      default: false
    },
    name: {
      type: String,
    },
    subCategories: {
      type: Array,
      default: () => []
    }
  });
  
  // Emitir evento para cerrar el modal
  const emit = defineEmits(['update:showModal']);

  const pushToNextLevel = (category) => {
    router.push(`/categorias/${category}`);
  };
  
  const closeModal = () => {
    emit('update:showModal', false); // Emitir el cambio al componente padre
  };
  </script>
  
  <style scoped>
  .modal.show {
    display: block;
    background-color: rgba(0, 0, 0, 0.5); /* Fondo oscuro */
  }

  .modal {
    z-index: 1050;
  }

/* Centrar el modal-header */
.modal-header {
  text-align: center;
  background-color: #c8c4e2;
  color: #d65748;
  display: flex;
  justify-content: center; /* Centra el contenido horizontalmente */
  align-items: center; /* Centra el contenido verticalmente */
  width: 100%;
  position: relative;
}

/* Estilo para la lista de categorías */
.categories .row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

/* Estilos para los círculos y la disposición */
.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

/* Estilo del círculo */
.circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.circle span {
  font-size: 20px;
  color: #333;
}

/* Asegurarse de que las categorías tengan un espacio adecuado */
.category-name {
  font-size: 14px;
  color: #333;
}

.modal-body {
    background-color: #e0def1;
    color: #d65748;
}

.category-name {
    color:#d65748;
}
  </style>
  
  
  
