# 🔗 Análisis de Correlación - Template

## Información General
- **Objetivo:** Identificar relaciones entre variables
- **Tipos:** Pearson, Spearman, Kendall
- **Aplicaciones:** Feature selection, Causality, Multicollinearity

## Tipos de Correlación

### Correlación de Pearson
- **Uso:** Variables numéricas, relación lineal
- **Rango:** -1 a +1
- **Interpretación:**
  - 0.7-1.0: Fuerte correlación
  - 0.3-0.7: Moderada correlación  
  - 0.0-0.3: Débil correlación

### Correlación de Spearman
- **Uso:** Variables ordinales, relaciones no lineales
- **Ventaja:** No asume distribución normal

### Matriz de Correlación
```python
import pandas as pd
import seaborn as sns

# Calcular matriz de correlación
corr_matrix = df.corr()

# Visualizar heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.show()
```

## Interpretación y Alertas
- **Multicolinealidad:** Correlaciones > 0.8 entre predictores
- **Correlación ≠ Causación:** Siempre validar causalidad
- **Variables latentes:** Correlaciones pueden ser indirectas

---
*Template creado por: [Data Scientist]*