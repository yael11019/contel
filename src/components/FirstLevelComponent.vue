<template>
    <div class="container">
        <p class="category-name">
            - {{ categoryName }} -
        </p>
        <div class="card mb-3" style="max-width: 700px;">
            <div class="row g-0 align-items-center">
                <div class="col-4 col-md-4">
                <img src="../assets/contelLogo.png" class="img-fluid rounded-start" alt="Logo">
                </div>
                <div class="col-8 col-md-8">
                <div class="card-body">
                    <h5 class="card-title">Nombre o razón social</h5>
                    <p class="card-text">
                    This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.
                    </p>
                    <p class="card-text"><small class="text-body-secondary">Last updated 3 mins ago</small></p>
                </div>
            </div>
        </div>
</div>

    </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  categoryName: String,
})
</script>

<style scoped>
    .category-name {
    color: red;
    margin-top: 10px;
  }
</style>