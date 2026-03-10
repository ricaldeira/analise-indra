<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header bg-light d-flex justify-content-between align-items-center">
      <h5 class="card-title mb-0">
        <i class="bi bi-table"></i> Detalhamento de Projetos
        <span class="badge bg-primary ms-2">{{ filteredProjects.length }}</span>
      </h5>
      <div class="d-flex gap-2">
        <input
          type="text"
          v-model="margemFilter"
          class="form-control form-control-sm"
          placeholder="Filtrar margem % (ex: >10, <20, 15)"
          style="width: 200px;"
          @input="applyFilters"
        >
        <select
          v-model="marketFilter"
          class="form-select form-select-sm"
          style="width: 120px;"
          @change="applyFilters"
        >
          <option value="">Todos Mercados</option>
          <option value="Administraciones Públicas">AAPP</option>
          <option value="Sanidad">Sanidad</option>
        </select>
        <button class="btn btn-sm btn-outline-secondary" @click="clearFilters">
          <i class="bi bi-x-circle"></i> Limpar
        </button>
      </div>
    </div>
    <div class="card-body p-0">
      <!-- Summary Cards for Filtered Data -->
      <div class="row g-3 mb-3 px-3">
        <div class="col-md-3">
          <div class="card bg-primary bg-opacity-10 border-primary border-opacity-25 h-100 shadow-sm">
            <div class="card-body text-center py-3">
              <div class="d-flex align-items-center justify-content-center mb-2">
                <i class="bi bi-currency-dollar text-primary me-2 fs-4"></i>
                <div>
                  <h6 class="card-title mb-1 text-primary fw-bold">Total Contratação</h6>
                  <h4 class="mb-0 text-primary fw-bold">{{ formatCurrency(totals.totalContratacao) }}</h4>
                </div>
              </div>
              <hr class="my-2 opacity-25">
              <div class="d-flex align-items-center justify-content-center">
                <small class="text-muted me-1">POA:</small>
                <span class="fw-semibold text-primary">{{ formatCurrency(totals.totalContratacaoPoa) }}</span>
              </div>
              <div class="d-flex align-items-center justify-content-center">
                <span class="fw-semibold text-primary">({{ formatPercentage(totals.totalVarContratacaoPoa) }})</span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-success bg-opacity-10 border-success border-opacity-25 h-100 shadow-sm">
            <div class="card-body text-center py-3">
              <div class="d-flex align-items-center justify-content-center mb-2">
                <i class="bi bi-graph-up-arrow text-success me-2 fs-4"></i>
                <div>
                  <h6 class="card-title mb-1 text-success fw-bold">Total Ingresso</h6>
                  <h4 class="mb-0 text-success fw-bold">{{ formatCurrency(totals.totalIngresso) }}</h4>
                </div>
              </div>
              <hr class="my-2 opacity-25">
              <div class="d-flex align-items-center justify-content-center">
                <small class="text-muted me-1">POA:</small>
                <span class="fw-semibold text-success">{{ formatCurrency(totals.totalIngressoPoa) }}</span>
              </div>
              <div class="d-flex align-items-center justify-content-center">
                <span class="fw-semibold text-success">({{ formatPercentage(totals.totalVarIngressoPoa) }})</span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-info bg-opacity-10 border-info border-opacity-25 h-100 shadow-sm">
            <div class="card-body text-center py-3">
              <div class="d-flex align-items-center justify-content-center mb-2">
                <i class="bi bi-bar-chart-line text-info me-2 fs-4"></i>
                <div>
                  <h6 class="card-title mb-1 text-info fw-bold">Total Margem</h6>
                  <h4 class="mb-0 text-info fw-bold">{{ formatCurrency(totals.totalMargem) }}</h4>
                </div>
              </div>
              <hr class="my-2 opacity-25">
              <div class="d-flex align-items-center justify-content-center">
                <small class="text-muted me-1">POA:</small>
                <span class="fw-semibold text-info">{{ formatCurrency(totals.totalMargemPoa) }}</span>
              </div>
              <div class="d-flex align-items-center justify-content-center">
                <span class="fw-semibold text-info">({{ formatPercentage(totals.totalVarMargemPoa) }})</span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-secondary bg-opacity-10 border-secondary border-opacity-25 h-100 shadow-sm">
            <div class="card-body text-center py-3">
              <div class="d-flex align-items-center justify-content-center mb-2">
                <i class="bi bi-percent text-secondary me-2 fs-4"></i>
                <div>
                  <h6 class="card-title mb-1 text-secondary fw-bold">Margem %</h6>
                  <h4 class="mb-0 text-secondary fw-bold">{{ formatPercentage(totals.totalMargemPercentual) }}</h4>
                </div>
              </div>
              <hr class="my-2 opacity-25">
              <div class="d-flex align-items-center justify-content-center">
                <small class="text-muted me-1">POA:</small>
                <span class="fw-semibold text-secondary">{{ formatPercentage(totals.totalMargemPercentualPoa) }}</span>
              </div>
              <div class="d-flex align-items-center justify-content-center">
                <span class="fw-semibold text-secondary">({{ formatPercentage(totals.totalVarMargemPercentualPoa, true) }})</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th scope="col" class="border-0 fw-bold text-center align-middle" @click="sortBy('mercado')" :class="sortClass('mercado')">Mercado</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" @click="sortBy('codigo')" :class="sortClass('codigo')">Código</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" @click="sortBy('descricao')" :class="sortClass('descricao')">Descrição</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" @click="sortBy('regiao')" :class="sortClass('regiao')">Região</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" @click="sortBy('tipo_solucao')" :class="sortClass('tipo_solucao')">Tipo<br>Solução</th>
              <!-- YTD headers -->
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(25, 135, 84, 0.1);" @click="sortBy('contratacion_ytd')" :class="sortClass('contratacion_ytd')">Contr.<br>YTD</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(25, 135, 84, 0.1);" @click="sortBy('ingresos_ytd')" :class="sortClass('ingresos_ytd')">Ingr.<br>YTD</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(25, 135, 84, 0.1);" @click="sortBy('margen_ytd')" :class="sortClass('margen_ytd')">Margem<br>YTD</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(25, 135, 84, 0.1);" @click="sortBy('margen_percentual')" :class="sortClass('margen_percentual')">%</th>
              <!-- POA headers -->
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(13, 110, 253, 0.1);" @click="sortBy('contratacion_poa')" :class="sortClass('contratacion_poa')">Contr.<br>POA</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(13, 110, 253, 0.1);" @click="sortBy('ingresos_poa')" :class="sortClass('ingresos_poa')">Ingr.<br>POA</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(13, 110, 253, 0.1);" @click="sortBy('margen_poa')" :class="sortClass('margen_poa')">Margem<br>POA</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(13, 110, 253, 0.1);" @click="sortBy('margen_percentual_poa')" :class="sortClass('margen_percentual_poa')">Margem %<br>POA</th>
              <!-- Comparison headers -->
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(255, 193, 7, 0.1);" @click="sortBy('contratacion_vs_poa')" :class="sortClass('contratacion_vs_poa')">Δ<br>Contr.</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(255, 193, 7, 0.1);" @click="sortBy('ingresos_vs_poa')" :class="sortClass('ingresos_vs_poa')">Δ<br>Ingr.</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(255, 193, 7, 0.1);" @click="sortBy('margen_vs_poa')" :class="sortClass('margen_vs_poa')">Δ<br>Margem</th>
              <th scope="col" class="border-0 fw-bold text-center align-middle" style="background-color: rgba(255, 193, 7, 0.1);" @click="sortBy('margen_percentual_vs_poa')" :class="sortClass('margen_percentual_vs_poa')">Δ<br>Margem%</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="projeto in sortedProjects" :key="projeto.id">
              <td class="text-center align-middle">
                <span class="badge bg-secondary">{{ projeto.mercado }}</span>
              </td>
              <td class="text-center align-middle">
                <code class="text-primary">{{ projeto.codigo }}</code>
              </td>
              <td class="text-center align-middle text-truncate" style="max-width: 150px;" :title="projeto.descricao">
                {{ projeto.descricao }}
              </td>
              <td class="text-center align-middle">{{ projeto.regiao || '-' }}</td>
              <td class="text-center align-middle">{{ projeto.tipo_solucao || '-' }}</td>
              <!-- YTD (Realizado) -->
              <td class="text-center fw-bold align-middle" style="background-color: rgba(25, 135, 84, 0.05);">
                {{ projeto.contratacion_ytd_formatted }}
              </td>
              <td class="text-center fw-bold text-success align-middle" style="background-color: rgba(25, 135, 84, 0.05);">
                {{ projeto.ingresos_ytd_formatted }}
              </td>
              <td class="text-center fw-bold align-middle" style="background-color: rgba(25, 135, 84, 0.05);" :class="{ 'text-success': projeto.margen_ytd >= 0, 'text-danger': projeto.margen_ytd < 0 }">
                {{ projeto.margen_ytd_formatted }}
              </td>
              <td class="text-center align-middle">
                <span class="badge"
                      :class="getMargemBadgeClass(projeto.margen_percentual)">
                  {{ projeto.margen_percentual.toFixed(1) }}%
                </span>
              </td>
              <!-- POA (Planejado) -->
              <td class="text-center fw-bold text-primary align-middle" style="background-color: rgba(13, 110, 253, 0.05);">
                {{ projeto.contratacion_poa_formatted }}
              </td>
              <td class="text-center fw-bold text-primary align-middle" style="background-color: rgba(13, 110, 253, 0.05);">
                {{ projeto.ingresos_poa_formatted }}
              </td>
              <td class="text-center fw-bold text-primary align-middle" style="background-color: rgba(13, 110, 253, 0.05);">
                {{ projeto.margen_poa_formatted }}
              </td>
              <td class="text-center fw-bold text-primary align-middle" style="background-color: rgba(13, 110, 253, 0.05);">
                {{ projeto.margen_percentual_poa_formatted }}%
              </td>
              <!-- Comparações -->
              <td class="text-center fw-bold align-middle" style="background-color: rgba(255, 193, 7, 0.05);" :class="{ 'text-success': projeto.contratacion_vs_poa >= 0, 'text-danger': projeto.contratacion_vs_poa < 0 }">
                {{ projeto.contratacion_vs_poa_formatted }}
              </td>
              <td class="text-center fw-bold align-middle" style="background-color: rgba(255, 193, 7, 0.05);" :class="{ 'text-success': projeto.ingresos_vs_poa >= 0, 'text-danger': projeto.ingresos_vs_poa < 0 }">
                {{ projeto.ingresos_vs_poa_formatted }}
              </td>
              <td class="text-center fw-bold align-middle" style="background-color: rgba(255, 193, 7, 0.05);" :class="{ 'text-success': projeto.margen_vs_poa >= 0, 'text-danger': projeto.margen_vs_poa < 0 }">
                {{ projeto.margen_vs_poa_formatted }}
              </td>
              <td class="text-center fw-bold align-middle" style="background-color: rgba(255, 193, 7, 0.05);" :class="{ 'text-success': projeto.margen_percentual_vs_poa >= 0, 'text-danger': projeto.margen_percentual_vs_poa < 0 }">
                {{ projeto.margen_percentual_vs_poa_formatted }}%
              </td>
            </tr>
            <tr v-if="filteredProjects.length === 0">
              <td colspan="19" class="text-center text-muted py-4">
                <i class="bi bi-info-circle me-2"></i>
                Nenhum projeto encontrado.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: 'ProjectTable',
  computed: {
    ...mapState({
      margemFilter: state => state.projectTable.margemFilter,
      marketFilter: state => state.projectTable.marketFilter,
      sortColumn: state => state.projectTable.sortColumn,
      sortDirection: state => state.projectTable.sortDirection
    }),
    ...mapGetters(['currentProjects']),
    filteredProjects() {
      let filtered = [...this.currentProjects]

      // Aplicar filtro de margem
      if (this.projectTableStore.margemFilter.trim()) {
        const filterValue = parseFloat(this.projectTableStore.margemFilter.replace(/^[><=]+/, ''))
        const operator = this.projectTableStore.margemFilter.replace(/[\d.-]/g, '')

        filtered = filtered.filter(projeto => {
          const margemValue = projeto.margen_percentual

          switch (operator) {
            case '>=':
              return margemValue >= filterValue
            case '<=':
              return margemValue <= filterValue
            case '>':
              return margemValue > filterValue
            case '<':
              return margemValue < filterValue
            default:
              // Filtro exato
              return Math.abs(margemValue - filterValue) < 0.1
          }
        })
      }

      // Aplicar filtro de mercado
      if (this.projectTableStore.marketFilter) {
        filtered = filtered.filter(projeto => projeto.mercado === this.projectTableStore.marketFilter)
      }

      return filtered
    },
    sortedProjects() {
      if (!this.projectTableStore.sortColumn) {
        return this.filteredProjects
      }

      return [...this.filteredProjects].sort((a, b) => {
        let aValue = a[this.projectTableStore.sortColumn]
        let bValue = b[this.projectTableStore.sortColumn]

        // Tratamento especial para valores numéricos
        if (['contratacion_ytd', 'ingresos_ytd', 'margen_ytd', 'margen_percentual',
             'contratacion_poa', 'ingresos_poa', 'margen_poa', 'margen_percentual_poa',
             'contratacion_vs_poa', 'ingresos_vs_poa', 'margen_vs_poa', 'margen_percentual_vs_poa'].includes(this.projectTableStore.sortColumn)) {
          aValue = parseFloat(aValue) || 0
          bValue = parseFloat(bValue) || 0
        } else {
          // Para strings, usar comparação local
          aValue = String(aValue || '').toLowerCase()
          bValue = String(bValue || '').toLowerCase()
        }

        if (aValue < bValue) return this.projectTableStore.sortDirection === 'asc' ? -1 : 1
        if (aValue > bValue) return this.projectTableStore.sortDirection === 'asc' ? 1 : -1
        return 0
      })
    },
    totals() {
      const projects = this.sortedProjects

      // Totais realizados
      let totalContratacao = 0
      let totalIngresso = 0
      let totalMargem = 0

      // Totais POA
      let totalContratacaoPoa = 0
      let totalIngressoPoa = 0
      let totalMargemPoa = 0

      projects.forEach(projeto => {
        totalContratacao += projeto.contratacion_ytd || 0
        totalIngresso += projeto.ingresos_ytd || 0
        totalMargem += projeto.margen_ytd || 0

        totalContratacaoPoa += projeto.contratacion_poa || 0
        totalIngressoPoa += projeto.ingresos_poa || 0
        totalMargemPoa += projeto.margen_poa || 0
      })

      const totalMargemPercentual = totalIngresso > 0 ? (totalMargem / totalIngresso) * 100 : 0
      const totalMargemPercentualPoa = totalIngressoPoa > 0 ? (totalMargemPoa / totalIngressoPoa) * 100 : 0

      // Variações
      const totalVarContratacaoPoa = totalContratacaoPoa > 0 ? (totalContratacao / totalContratacaoPoa) - 1 : 0
      const totalVarIngressoPoa = totalIngressoPoa > 0 ? (totalIngresso / totalIngressoPoa) - 1 : 0
      const totalVarMargemPoa = totalMargemPoa > 0 ? (totalMargem / totalMargemPoa) - 1 : 0
      const totalVarMargemPercentualPoa = totalMargemPercentual - totalMargemPercentualPoa

      return {
        totalContratacao,
        totalIngresso,
        totalMargem,
        totalMargemPercentual,
        totalContratacaoPoa,
        totalIngressoPoa,
        totalMargemPoa,
        totalMargemPercentualPoa,
        totalVarContratacaoPoa,
        totalVarIngressoPoa,
        totalVarMargemPoa,
        totalVarMargemPercentualPoa
      }
    }
  },
  methods: {
    ...mapActions({
      setMargemFilter: 'projectTable/setMargemFilter',
      setMarketFilter: 'projectTable/setMarketFilter',
      setSorting: 'projectTable/setSorting',
      clearFilters: 'projectTable/clearFilters'
    }),
    applyFilters() {
      // Os filtros são aplicados automaticamente via computed properties
      console.log('🔍 Filtros aplicados:', {
        margem: this.margemFilter,
        mercado: this.marketFilter,
        projetosVisiveis: this.filteredProjects.length
      })
    },
    clearFilters() {
      this.clearFilters()
    },
    sortBy(column) {
      this.setSorting({ column })
    },
    sortClass(column) {
      if (this.sortColumn !== column) return ''
      return this.sortDirection === 'asc' ? 'table-sorted-asc' : 'table-sorted-desc'
    },
    getMargemBadgeClass(margemPercentual) {
      if (margemPercentual >= 20) return 'bg-success'
      if (margemPercentual >= 10) return 'bg-warning'
      if (margemPercentual >= 0) return 'bg-secondary'
      return 'bg-danger'
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value)
    },
    formatPercentage(value, isPoints = false) {
      const formatted = value.toFixed(2)
      return isPoints ? `${formatted}p.p` : `${formatted}%`
    }
  }
}
</script>

<style scoped>
.table th {
  position: relative;
  user-select: none;
  cursor: pointer;
}

.table th:hover {
  background-color: rgba(0, 123, 255, 0.1);
}

.table th.table-sorted-asc::after {
  content: ' ▲';
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  color: #198754;
  font-size: 12px;
}

.table th.table-sorted-desc::after {
  content: ' ▼';
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  color: #198754;
  font-size: 12px;
}
</style>