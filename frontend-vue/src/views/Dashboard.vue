<template>
  <div class="dashboard">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h2 class="mb-1">
              <i class="bi bi-bar-chart-line"></i> Dashboard Analítico
            </h2>
            <p class="text-muted mb-0">Visão geral dos projetos e indicadores</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Carregando...</span>
      </div>
      <p class="mt-3">Carregando dados do dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-danger" role="alert">
      <i class="bi bi-exclamation-triangle"></i>
      Erro ao carregar dados: {{ error }}
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Summary Cards -->
      <SummaryCards
        :aapp-data="dashboardData.aapp?.cards || []"
        :sanidad-data="dashboardData.sanidad?.cards || []"
        :consolidado-data="dashboardData.consolidado?.cards || []"
        :current-category="currentCategory"
        @category-changed="setCurrentCategory"
      />

      <!-- Project Table -->
      <ProjectTable
        :projects="currentProjects"
        :loading="loadingProjects"
        :category="currentCategory"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { dashboardAPI } from '../services/api.js'
import SummaryCards from '../components/SummaryCards.vue'
import ProjectTable from '../components/ProjectTable.vue'

export default {
  name: 'Dashboard',
  components: {
    SummaryCards,
    ProjectTable
  },
  setup() {
    const loading = ref(true)
    const loadingProjects = ref(false)
    const error = ref(null)
    const dashboardData = ref({})
    const currentCategory = ref('consolidado')

    const currentProjects = computed(() => {
      return dashboardData.value[currentCategory.value]?.projetos || []
    })

    const loadDashboardData = async () => {
      try {
        loading.value = true
        error.value = null

        const response = await dashboardAPI.getAllData()
        dashboardData.value = response.data

        console.log('✅ Dashboard data loaded:', dashboardData.value)
      } catch (err) {
        console.error('❌ Error loading dashboard data:', err)
        error.value = err.message || 'Erro ao carregar dados'
      } finally {
        loading.value = false
      }
    }

    const setCurrentCategory = (category) => {
      currentCategory.value = category
      console.log('📊 Category changed to:', category)
    }

    onMounted(() => {
      loadDashboardData()
    })

    return {
      loading,
      loadingProjects,
      error,
      dashboardData,
      currentCategory,
      currentProjects,
      setCurrentCategory
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
}
</style>