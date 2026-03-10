<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header bg-light">
      <div class="d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">
          <i class="bi bi-table"></i> Projetos {{ categoryLabel }}
        </h5>
        <div class="d-flex gap-2">
          <input
            type="text"
            class="form-control form-control-sm"
            placeholder="Filtrar por margem..."
            v-model="filters.margin"
            style="width: 150px;"
          >
          <select
            class="form-select form-select-sm"
            v-model="filters.market"
            style="width: 120px;"
          >
            <option value="">Todos os mercados</option>
            <option value="Administraciones Públicas">AAPP</option>
            <option value="Sanidad">Sanidad</option>
          </select>
        </div>
      </div>
    </div>
    <div class="card-body">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
        Carregando projetos...
      </div>

      <!-- Table -->
      <div v-else-if="filteredProjects.length > 0" class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th @click="sortBy('codigo')" :class="getSortClass('codigo')">Código</th>
              <th @click="sortBy('descricao')" :class="getSortClass('descricao')">Descrição</th>
              <th @click="sortBy('mercado')" :class="getSortClass('mercado')">Mercado</th>
              <th @click="sortBy('regiao')" :class="getSortClass('regiao')">Região</th>
              <th @click="sortBy('tipo_solucao')" :class="getSortClass('tipo_solucao')">Tipo Solução</th>
              <th @click="sortBy('contratacion_ytd')" :class="getSortClass('contratacion_ytd')" class="text-end">Contratação YTD</th>
              <th @click="sortBy('ingresos_ytd')" :class="getSortClass('ingresos_ytd')" class="text-end">Receita YTD</th>
              <th @click="sortBy('margen_ytd')" :class="getSortClass('margen_ytd')" class="text-end">Margem YTD</th>
              <th @click="sortBy('margen_percentual_ytd')" :class="getSortClass('margen_percentual_ytd')" class="text-end">Margem %</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="project in paginatedProjects" :key="project.id || project.codigo">
              <td><code>{{ project.codigo }}</code></td>
              <td>{{ project.descricao }}</td>
              <td>
                <span class="badge" :class="getMarketBadgeClass(project.mercado)">
                  {{ project.mercado }}
                </span>
              </td>
              <td>{{ project.regiao || '-' }}</td>
              <td>{{ project.tipo_solucao || '-' }}</td>
              <td class="text-end">{{ formatCurrency(project.contratacion_ytd) }}</td>
              <td class="text-end">{{ formatCurrency(project.ingresos_ytd) }}</td>
              <td class="text-end">{{ formatCurrency(project.margen_ytd) }}</td>
              <td class="text-end">
                <span :class="getMarginClass(project.margen_percentual_ytd)">
                  {{ formatPercent(project.margen_percentual_ytd) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <nav v-if="totalPages > 1" class="mt-3">
          <ul class="pagination justify-content-center">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" href="#" @click.prevent="goToPage(currentPage - 1)">Anterior</a>
            </li>
            <li
              v-for="page in visiblePages"
              :key="page"
              class="page-item"
              :class="{ active: page === currentPage }"
            >
              <a class="page-link" href="#" @click.prevent="goToPage(page)">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" href="#" @click.prevent="goToPage(currentPage + 1)">Próximo</a>
            </li>
          </ul>
        </nav>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-4">
        <i class="bi bi-inbox fs-1 text-muted"></i>
        <p class="text-muted mt-2">Nenhum projeto encontrado</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'

export default {
  name: 'ProjectTable',
  props: {
    projects: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    category: {
      type: String,
      default: 'consolidado'
    }
  },
  setup(props) {
    const filters = ref({
      margin: '',
      market: ''
    })

    const sortConfig = ref({
      key: 'margen_percentual_ytd',
      direction: 'desc'
    })

    const currentPage = ref(1)
    const pageSize = ref(20)

    const categoryLabel = computed(() => {
      switch (props.category) {
        case 'aapp':
          return 'AAPP'
        case 'sanidad':
          return 'Sanidad'
        case 'consolidado':
        default:
          return 'Consolidados'
      }
    })

    const filteredProjects = computed(() => {
      let filtered = [...props.projects]

      // Apply margin filter
      if (filters.value.margin) {
        const marginFilter = parseFloat(filters.value.margin.replace(',', '.'))
        filtered = filtered.filter(project => {
          const margin = project.margen_percentual_ytd || 0
          return Math.abs(margin - marginFilter) < 0.01
        })
      }

      // Apply market filter
      if (filters.value.market) {
        filtered = filtered.filter(project =>
          project.mercado === filters.value.market
        )
      }

      return filtered
    })

    const sortedProjects = computed(() => {
      const sorted = [...filteredProjects.value].sort((a, b) => {
        const aValue = a[sortConfig.value.key] || 0
        const bValue = b[sortConfig.value.key] || 0

        let result = 0
        if (aValue < bValue) result = -1
        if (aValue > bValue) result = 1

        return sortConfig.value.direction === 'asc' ? result : -result
      })

      return sorted
    })

    const totalPages = computed(() => {
      return Math.ceil(sortedProjects.value.length / pageSize.value)
    })

    const visiblePages = computed(() => {
      const pages = []
      const start = Math.max(1, currentPage.value - 2)
      const end = Math.min(totalPages.value, currentPage.value + 2)

      for (let i = start; i <= end; i++) {
        pages.push(i)
      }

      return pages
    })

    const paginatedProjects = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return sortedProjects.value.slice(start, end)
    })

    const sortBy = (key) => {
      if (sortConfig.value.key === key) {
        sortConfig.value.direction = sortConfig.value.direction === 'asc' ? 'desc' : 'asc'
      } else {
        sortConfig.value.key = key
        sortConfig.value.direction = 'desc'
      }
    }

    const getSortClass = (key) => {
      if (sortConfig.value.key !== key) return ''
      return sortConfig.value.direction === 'asc' ? 'table-sort-asc' : 'table-sort-desc'
    }

    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
      }
    }

    const formatCurrency = (value) => {
      if (value === null || value === undefined) return 'R$ 0'
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value)
    }

    const formatPercent = (value) => {
      if (value === null || value === undefined) return '0%'
      return `${(value * 100).toFixed(1)}%`
    }

    const getMarketBadgeClass = (market) => {
      if (market?.includes('Administraciones Públicas')) {
        return 'bg-primary'
      } else if (market?.includes('Sanidad')) {
        return 'bg-success'
      }
      return 'bg-secondary'
    }

    const getMarginClass = (margin) => {
      if (margin === null || margin === undefined) return ''
      const marginPercent = margin * 100
      if (marginPercent >= 20) return 'text-success fw-bold'
      if (marginPercent >= 10) return 'text-warning'
      return 'text-danger'
    }

    // Reset to first page when filters change
    watch([() => filters.value.margin, () => filters.value.market], () => {
      currentPage.value = 1
    })

    // Reset to first page when category changes
    watch(() => props.category, () => {
      currentPage.value = 1
    })

    return {
      filters,
      categoryLabel,
      filteredProjects,
      sortedProjects,
      totalPages,
      visiblePages,
      paginatedProjects,
      currentPage,
      sortBy,
      getSortClass,
      goToPage,
      formatCurrency,
      formatPercent,
      getMarketBadgeClass,
      getMarginClass
    }
  }
}
</script>

<style scoped>
.table th {
  cursor: pointer;
  user-select: none;
  position: relative;
}

.table th:hover {
  background-color: rgba(13, 110, 253, 0.1);
}

.table-sort-asc::after {
  content: ' ▲';
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  color: #0d6efd;
}

.table-sort-desc::after {
  content: ' ▼';
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  color: #0d6efd;
}

.badge {
  font-size: 0.75em;
}

.pagination .page-link {
  color: #0d6efd;
}

.pagination .page-item.active .page-link {
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style>