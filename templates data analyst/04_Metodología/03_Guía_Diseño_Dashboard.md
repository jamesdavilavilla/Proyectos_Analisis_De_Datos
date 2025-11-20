# 🎨 Guía de Diseño de Dashboard - Template

## Principios de Diseño

### 1. Hierarchy Visual
- **Title:** Más prominente, propósito claro
- **KPIs:** Tamaño grande, fácil lectura
- **Charts:** Ordenados por importancia
- **Filters:** Visibles pero no dominantes

### 2. Color Strategy
- **Corporate Colors:** Mantener brand consistency
- **Semantic Colors:** Red (malo), Green (bueno), Yellow (warning)
- **Accessibility:** Considerar daltonismo
- **Contrast:** Texto legible en todos los backgrounds

### 3. Layout Principles
- **F-Pattern:** Usuarios leen de izquierda a derecha, arriba a abajo
- **Whitespace:** Permite respirar al contenido
- **Alignment:** Todo alineado en grids
- **Consistency:** Mismo estilo en todos los elementos

## Chart Selection Guide

### Comparisons
- **Bar Charts:** Comparar categorías
- **Column Charts:** Tendencias temporales cortas
- **Horizontal Bars:** Cuando labels son largos

### Relationships
- **Scatter Plots:** Correlación entre variables
- **Bubble Charts:** 3 dimensiones
- **Correlation Matrix:** Multiple correlations

### Distributions
- **Histograms:** Distribución de frecuencias
- **Box Plots:** Outliers y quartiles
- **Violin Plots:** Distribución + density

### Parts-to-Whole
- **Pie Charts:** Solo para 2-5 categorías
- **Donut Charts:** Con metric en el centro
- **Treemap:** Jerarquías y proporciones

## Performance Optimization
- Usar aggregated data cuando posible
- Limitar número de visuals por página
- Optimizar DAX calculations
- Implementar incremental refresh

---