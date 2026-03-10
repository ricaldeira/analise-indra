<template>
  <div class="col-lg-4 col-md-6">
    <div class="card h-100 border-0 shadow-sm hover-card">
      <div class="card-body text-center">
        <div class="mb-3">
          <div
            class="icon-circle mx-auto"
            :class="iconBackgroundClass"
          >
            <i :class="`bi ${icon} fs-2`" :style="{ color: iconColor }"></i>
          </div>
        </div>
        <h5 class="card-title text-muted mb-2">{{ title }}</h5>
        <h3 class="card-value mb-2" :class="valueClass">{{ value }}</h3>
        <span
          v-if="showChange"
          class="badge rounded-pill"
          :class="changeBadgeClass"
        >
          <i :class="changeIconClass"></i>
          {{ change }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MetricCard',
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: String,
      required: true
    },
    change: {
      type: String,
      default: ''
    },
    changeType: {
      type: String,
      default: 'neutral',
      validator: (value) => ['positive', 'negative', 'neutral'].includes(value)
    },
    icon: {
      type: String,
      default: 'bi-graph-up'
    },
    theme: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'success', 'info', 'warning', 'danger'].includes(value)
    }
  },
  computed: {
    iconBackgroundClass() {
      return `bg-${this.theme} bg-opacity-10 text-${this.theme}`
    },
    iconColor() {
      const colors = {
        primary: '#0d6efd',
        success: '#198754',
        info: '#0dcaf0',
        warning: '#ffc107',
        danger: '#dc3545'
      }
      return colors[this.theme] || colors.primary
    },
    valueClass() {
      return this.changeType
    },
    showChange() {
      return this.change && this.change !== '0%' && this.change !== ''
    },
    changeBadgeClass() {
      const classes = {
        positive: 'bg-success',
        negative: 'bg-danger',
        neutral: 'bg-secondary'
      }
      return classes[this.changeType] || 'bg-secondary'
    },
    changeIconClass() {
      const icons = {
        positive: 'bi-arrow-up',
        negative: 'bi-arrow-down',
        neutral: 'bi-dash'
      }
      return `bi ${icons[this.changeType] || 'bi-dash'}`
    }
  }
}
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}

.icon-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-value.positive {
  color: #198754;
}

.card-value.negative {
  color: #dc3545;
}

.card-value.neutral {
  color: #6c757d;
}
</style>