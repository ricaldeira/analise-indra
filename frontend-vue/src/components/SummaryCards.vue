<template>
  <div class="row mb-4">
    <!-- Category Tabs -->
    <div class="col-12 mb-3">
      <nav>
        <div class="nav nav-tabs" id="dashboardTabs" role="tablist">
          <button
            class="nav-link"
            :class="{ active: currentCategory === 'consolidado' }"
            @click="setCategory('consolidado')"
            type="button"
          >
            Consolidado
          </button>
          <button
            class="nav-link"
            :class="{ active: currentCategory === 'aapp' }"
            @click="setCategory('aapp')"
            type="button"
          >
            AAPP
          </button>
          <button
            class="nav-link"
            :class="{ active: currentCategory === 'sanidad' }"
            @click="setCategory('sanidad')"
            type="button"
          >
            Sanidad
          </button>
        </div>
      </nav>
    </div>

    <!-- Cards -->
    <div class="col-12">
      <div class="row">
        <div
          v-for="(card, index) in currentCards"
          :key="index"
          class="col-md-3 mb-3"
        >
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="mb-2">
                <i :class="getIconClass(card.icon)" class="fs-2 text-primary"></i>
              </div>
              <h5 class="card-title text-muted mb-2">{{ card.title }}</h5>
              <h3 class="card-value mb-1" :class="getChangeClass(card.change_type)">
                {{ card.value }}
              </h3>
              <small
                class="text-muted"
                :class="getChangeClass(card.change_type)"
              >
                {{ card.change }}
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'SummaryCards',
  props: {
    aappData: {
      type: Array,
      default: () => []
    },
    sanidadData: {
      type: Array,
      default: () => []
    },
    consolidadoData: {
      type: Array,
      default: () => []
    },
    currentCategory: {
      type: String,
      default: 'consolidado'
    }
  },
  emits: ['category-changed'],
  setup(props, { emit }) {
    const currentCards = computed(() => {
      switch (props.currentCategory) {
        case 'aapp':
          return props.aappData
        case 'sanidad':
          return props.sanidadData
        case 'consolidado':
        default:
          return props.consolidadoData
      }
    })

    const setCategory = (category) => {
      emit('category-changed', category)
    }

    const getIconClass = (icon) => {
      return `bi ${icon}`
    }

    const getChangeClass = (changeType) => {
      switch (changeType) {
        case 'positive':
          return 'text-success'
        case 'negative':
          return 'text-danger'
        default:
          return 'text-muted'
      }
    }

    return {
      currentCards,
      setCategory,
      getIconClass,
      getChangeClass
    }
  }
}
</script>

<style scoped>
.nav-tabs .nav-link {
  border: none;
  border-bottom: 2px solid transparent;
  background: none;
  color: #6c757d;
  font-weight: 500;
}

.nav-tabs .nav-link.active {
  border-bottom-color: #0d6efd;
  color: #0d6efd;
  background: none;
}

.nav-tabs .nav-link:hover {
  border-bottom-color: #0d6efd;
  color: #0d6efd;
}

.card {
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.card-value.positive {
  color: #198754 !important;
}

.card-value.negative {
  color: #dc3545 !important;
}
</style>