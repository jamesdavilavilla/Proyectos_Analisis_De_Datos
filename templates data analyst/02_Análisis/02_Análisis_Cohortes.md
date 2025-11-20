# 👥 Análisis de Cohortes - Template

## Información General
- **Objetivo:** Analizar comportamiento de grupos de usuarios/clientes a lo largo del tiempo
- **Audiencia:** Product, Marketing, Customer Success
- **Aplicaciones:** Retención, LTV, Product Adoption
- **Herramientas:** Python, SQL, Tableau

## Tipos de Cohortes

### 1. Cohortes Temporales
- **Por fecha de adquisición:** Mes/trimestre de registro
- **Por fecha de primera compra:** Cohortes de conversión
- **Por fecha de feature adoption:** Adopción de funcionalidades

### 2. Cohortes Comportamentales
- **Por canal de adquisición:** Organic, Paid, Referral
- **Por segmento demográfico:** Edad, ubicación, industria
- **Por nivel de engagement:** High, Medium, Low

### 3. Cohortes de Valor
- **Por valor inicial:** Ticket de primera compra
- **Por potencial:** Scoring de propensión
- **Por plan/producto:** Diferentes ofertas

## Metodología de Análisis

### Preparación de Datos
```sql
-- Estructura básica de datos de cohorte
SELECT 
    customer_id,
    acquisition_date,
    transaction_date,
    revenue,
    DATE_DIFF(transaction_date, acquisition_date, MONTH) as period_number
FROM customer_transactions
WHERE acquisition_date >= '2023-01-01'
```

### Cálculo de Métricas de Cohorte

#### Retención de Cohorte
```python
import pandas as pd
import numpy as np

def calculate_cohort_retention(df):
    # Crear tabla de cohorte
    cohort_data = df.groupby(['cohort_month', 'period_number'])['customer_id'].nunique().reset_index()
    cohort_table = cohort_data.pivot(index='cohort_month', 
                                   columns='period_number', 
                                   values='customer_id')
    
    # Calcular tamaños de cohorte inicial
    cohort_sizes = df.groupby('cohort_month')['customer_id'].nunique()
    
    # Calcular porcentajes de retención
    retention_table = cohort_table.divide(cohort_sizes, axis=0)
    
    return retention_table
```

#### Revenue por Cohorte
```python
def calculate_cohort_revenue(df):
    # Revenue acumulativo por cohorte
    revenue_cohort = df.groupby(['cohort_month', 'period_number'])['revenue'].sum().reset_index()
    revenue_table = revenue_cohort.pivot(index='cohort_month', 
                                       columns='period_number', 
                                       values='revenue')
    
    # Revenue promedio por usuario
    cohort_sizes = df.groupby('cohort_month')['customer_id'].nunique()
    arpu_table = revenue_table.divide(cohort_sizes, axis=0)
    
    return revenue_table, arpu_table
```

## Análisis de Retención

### Tabla de Retención Clásica
| Cohorte | Mes 0 | Mes 1 | Mes 2 | Mes 3 | Mes 6 | Mes 12 |
|---------|-------|-------|-------|-------|-------|--------|
| Ene 2023| 100%  | 65%   | 45%   | 35%   | 25%   | 20%    |
| Feb 2023| 100%  | 70%   | 48%   | 38%   | 28%   | 22%    |
| Mar 2023| 100%  | 68%   | 46%   | 36%   | 26%   | -      |

### Métricas Clave de Retención
- **Day 1 Retention:** % usuarios activos al día siguiente
- **Day 7 Retention:** % usuarios activos a la semana
- **Day 30 Retention:** % usuarios activos al mes
- **Long-term Retention:** % usuarios activos > 6 meses

### Benchmark de Retención por Industria
- **SaaS B2B:** D1: 60-70%, D7: 40-50%, D30: 25-35%
- **Mobile Apps:** D1: 20-25%, D7: 8-12%, D30: 3-5%
- **E-commerce:** D1: 15-20%, D7: 8-10%, D30: 4-6%

## Análisis de Revenue Cohorte

### Customer Lifetime Value (CLV)
```python
def calculate_clv_by_cohort(df, periods=12):
    # CLV acumulativo por período
    clv_data = []
    for period in range(periods + 1):
        period_clv = df[df['period_number'] <= period].groupby('cohort_month')['revenue'].sum()
        clv_data.append(period_clv)
    
    clv_df = pd.DataFrame(clv_data).T
    clv_df.columns = [f'CLV_Month_{i}' for i in range(periods + 1)]
    
    return clv_df
```

### Métricas de Monetización
- **Time to First Purchase:** Días hasta primera compra
- **Purchase Frequency:** Compras por usuario por período
- **Average Order Value:** Valor promedio por transacción
- **Revenue per User:** Revenue total / usuarios únicos

## Visualizaciones de Cohorte

### Heatmap de Retención
```python
import seaborn as sns
import matplotlib.pyplot as plt

def plot_cohort_heatmap(retention_table):
    plt.figure(figsize=(12, 8))
    sns.heatmap(retention_table, 
                annot=True, 
                fmt='.1%',
                cmap='YlOrRd',
                linewidths=0.5)
    plt.title('Cohort Retention Rates')
    plt.xlabel('Period Number')
    plt.ylabel('Cohort Month')
    plt.show()
```

### Gráfico de Líneas de Retención
```python
def plot_retention_lines(retention_table):
    plt.figure(figsize=(12, 6))
    for cohort in retention_table.index:
        plt.plot(retention_table.columns, 
                retention_table.loc[cohort], 
                marker='o', 
                label=cohort)
    
    plt.title('Cohort Retention Curves')
    plt.xlabel('Months Since Acquisition')
    plt.ylabel('Retention Rate')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()
```

## Análisis Avanzado de Cohortes

### Cohortes Multidimensionales
```python
# Cohorte por canal y mes
cohort_multi = df.groupby(['cohort_month', 'acquisition_channel', 'period_number'])['customer_id'].nunique()

# Comparar performance por canal
channel_performance = cohort_multi.groupby(['acquisition_channel', 'period_number']).mean()
```

### Análisis de Supervivencia
```python
from lifelines import KaplanMeierFitter

def survival_analysis(df):
    kmf = KaplanMeierFitter()
    
    # Preparar datos para análisis de supervivencia
    durations = df.groupby('customer_id')['period_number'].max()
    event_observed = durations < df['period_number'].max()  # Churn observado
    
    kmf.fit(durations, event_observed)
    
    return kmf
```

## Insights y Recomendaciones

### Patrones Típicos
1. **Healthy Cohort:** Retención gradual y estable
2. **Leaky Bucket:** Caída pronunciada en primeros períodos
3. **Recovering Cohort:** Mejora en retención en períodos recientes
4. **Seasonal Impact:** Variación por época del año

### Acciones por Tipo de Cohorte
- **Baja retención inicial:** Mejorar onboarding
- **Caída en mes 2-3:** Revisar product-market fit
- **Diferencias por canal:** Optimizar targeting
- **Variación estacional:** Ajustar estrategias temporales

### Framework de Decisión
1. **Identificar cohortes problemáticas**
2. **Analizar causas de churn**
3. **Implementar intervenciones específicas**
4. **Medir impacto en cohortes futuras**

## Template de Reporte

### Executive Summary
- **Retención promedio:** XX% a 30 días, XX% a 90 días
- **Mejor cohorte:** [Mes] con XX% retención
- **Tendencia:** [Mejorando/Estable/Deteriorando]
- **Acción requerida:** [Prioridad principal]

### Recomendaciones
- [ ] **Onboarding:** Mejorar primeros 7 días
- [ ] **Engagement:** Implementar programa de activación
- [ ] **Segmentación:** Personalizar experiencia por cohorte
- [ ] **Win-back:** Campaña para cohortes de baja retención

---
*Template creado por: [Senior Analytics Specialist]*  
*Última actualización: [Fecha]*  
*Versión: 1.0*