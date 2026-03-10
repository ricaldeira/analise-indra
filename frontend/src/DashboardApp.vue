<template>
  <div id="dashboard-vue-app">
    <!-- Summary Cards -->
    <div class="row mt-4">
      <div class="col-12">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-light">
            <h5 class="card-title mb-0">
              <i class="bi bi-info-circle"></i> Resumo Geral
            </h5>
          </div>
          <div class="card-body">
            <div class="row text-center">
              <div class="col-md-3">
                <div class="p-3">
                  <h4 class="text-primary mb-1">{{ aappCards[0]?.value || '0' }}</h4>
                  <p class="text-muted mb-0">{{ aappCards[0]?.title || 'Projetos AAPP' }}</p>
                </div>
              </div>
              <div class="col-md-3">
                <div class="p-3">
                  <h4 class="text-success mb-1">{{ sanidadCards[0]?.value || '0' }}</h4>
                  <p class="text-muted mb-0">{{ sanidadCards[0]?.title || 'Projetos Sanidad' }}</p>
                </div>
              </div>
              <div class="col-md-3">
                <div class="p-3">
                  <h4 class="text-info mb-1">{{ consolidadoCards[0]?.value || '0' }}</h4>
                  <p class="text-muted mb-0">{{ consolidadoCards[0]?.title || 'Total Projetos' }}</p>
                </div>
              </div>
              <div class="col-md-3">
                <div class="p-3">
                  <h4 class="text-warning mb-1">{{ consolidadoCards[1]?.value || '0' }}</h4>
                  <p class="text-muted mb-0">{{ consolidadoCards[1]?.title || 'Receita Total' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <DashboardTabs
      :aapp-data="aappData"
      :sanidad-data="sanidadData"
      :consolidado-data="consolidadoData"
      @tab-changed="onTabChanged"
    />

    <!-- Projects Table -->
    <div class="row mt-4">
      <div class="col-12">
        <ProjectTable
          :projects="currentProjects"
          :key="currentCategory"
        />
      </div>
    </div>
  </div>
</template>

<script>
import DashboardTabs from './components/DashboardTabs.vue'
import ProjectTable from './components/ProjectTable.vue'
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: 'DashboardApp',
  components: {
    DashboardTabs,
    ProjectTable
  },
  computed: {
    ...mapState(['aappData', 'sanidadData', 'consolidadoData']),
    ...mapGetters(['currentProjects']),
    aappCards() {
      return this.aappData.cards || []
    },
    sanidadCards() {
      return this.sanidadData.cards || []
    },
    consolidadoCards() {
      return this.consolidadoData.cards || []
    }
  },
  mounted() {
    console.log('🚀 Dashboard Vue.js inicializado com sucesso!')
    this.loadDataFromDjango()
  },
  methods: {
    ...mapActions(['setCurrentCategory', 'loadDataFromDjango']),
    onTabChanged(tabId) {
      this.setCurrentCategory(tabId)
    }
  }
}
</script>

<style scoped>
#dashboard-vue-app {
  min-height: 50px;
}
</style>