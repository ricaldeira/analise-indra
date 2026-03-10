<template>
  <div>
    <!-- Dashboard Tabs -->
    <div class="card shadow-lg border-0">
      <div class="card-header bg-white border-bottom-0">
        <ul class="nav nav-tabs card-header-tabs" role="tablist">
          <li class="nav-item" role="presentation" v-for="tab in tabs" :key="tab.id">
            <button
              class="nav-link"
              :class="{ active: activeTab === tab.id }"
              :id="`${tab.id}-tab`"
              :data-bs-target="`#${tab.id}`"
              type="button"
              role="tab"
              @click="setActiveTab(tab.id)"
            >
              <i :class="`bi ${tab.icon}`"></i> {{ tab.name }}
            </button>
          </li>
        </ul>
      </div>
      <div class="card-body">
        <div class="tab-content">
          <!-- AAPP Tab -->
          <div
            class="tab-pane fade"
            :class="{ 'show active': activeTab === 'aapp' }"
            id="aapp"
            role="tabpanel"
          >
            <div class="row g-4">
              <MetricCard
                v-for="card in aappCards"
                :key="card.title"
                :title="card.title"
                :value="card.value"
                :change="card.change"
                :change-type="card.change_type"
                :icon="card.icon"
                theme="primary"
              />
            </div>
          </div>

          <!-- Sanidad Tab -->
          <div
            class="tab-pane fade"
            :class="{ 'show active': activeTab === 'sanidad' }"
            id="sanidad"
            role="tabpanel"
          >
            <div class="row g-4">
              <MetricCard
                v-for="card in sanidadCards"
                :key="card.title"
                :title="card.title"
                :value="card.value"
                :change="card.change"
                :change-type="card.change_type"
                :icon="card.icon"
                theme="success"
              />
            </div>
          </div>

          <!-- Consolidado Tab -->
          <div
            class="tab-pane fade"
            :class="{ 'show active': activeTab === 'consolidado' }"
            id="consolidado"
            role="tabpanel"
          >
            <div class="row g-4">
              <MetricCard
                v-for="card in consolidadoCards"
                :key="card.title"
                :title="card.title"
                :value="card.value"
                :change="card.change"
                :change-type="card.change_type"
                :icon="card.icon"
                theme="info"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MetricCard from './MetricCard.vue'
import { mapState, mapActions } from 'vuex'

export default {
  name: 'DashboardTabs',
  components: {
    MetricCard
  },
  data() {
    return {
      tabs: [
        { id: 'aapp', name: 'AAPP', icon: 'bi-building' },
        { id: 'sanidad', name: 'Sanidad', icon: 'bi-heart-pulse' },
        { id: 'consolidado', name: 'Consolidado', icon: 'bi-collection' }
      ]
    }
  },
  computed: {
    ...mapState({
      activeTab: 'currentCategory',
      aappData: 'aappData',
      sanidadData: 'sanidadData',
      consolidadoData: 'consolidadoData'
    }),
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
  methods: {
    ...mapActions(['setCurrentCategory']),
    setActiveTab(tabId) {
      this.setCurrentCategory(tabId)
      this.$emit('tab-changed', tabId)
    }
  }
}
</script>

<style scoped>
.nav-tabs .nav-link {
  border: none;
  border-radius: 0;
  color: #6c757d;
}

.nav-tabs .nav-link:hover {
  background-color: rgba(13, 110, 253, 0.1);
  color: #0d6efd;
}

.nav-tabs .nav-link.active {
  background-color: #0d6efd;
  color: white;
  border-color: #0d6efd;
}
</style>