# 🧹 Checklist de Limpieza de Datos - Template

## Pre-Análisis Assessment

### 1. Exploración Inicial
- [ ] **Dimensiones del dataset:** Filas × Columnas
- [ ] **Tipos de datos:** Numérico, categórico, datetime, texto
- [ ] **Memoria utilizada:** Tamaño del dataset
- [ ] **Primera inspección visual:** .head(), .info(), .describe()

### 2. Análisis de Valores Faltantes
- [ ] **Missing values por columna:** .isnull().sum()
- [ ] **Patrón de missingness:** ¿Aleatorio o sistemático?
- [ ] **Impacto en análisis:** ¿Crítico para el objetivo?
- [ ] **Estrategia de imputación:** Drop, forward fill, mean, model-based

### 3. Detección de Outliers
- [ ] **Métodos estadísticos:** Z-score, IQR, Percentiles
- [ ] **Visualización:** Boxplots, histogramas, scatter plots
- [ ] **Validación de negocio:** ¿Outliers son válidos?
- [ ] **Tratamiento:** Remove, cap, transform, keep

### 4. Validación de Tipos de Datos
- [ ] **Fechas:** Formato consistente, timezone
- [ ] **Números:** Decimales vs enteros, unidades
- [ ] **Categóricos:** Levels, encoding, case sensitivity
- [ ] **Texto:** Encoding, caracteres especiales

### 5. Consistencia de Datos
- [ ] **Duplicados:** Registros exactos y fuzzy matches
- [ ] **Naming conventions:** Estandarización de nombres
- [ ] **Units consistency:** Mismas unidades de medida
- [ ] **Referential integrity:** Foreign keys válidos

## Proceso de Limpieza

### Código Base Python
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carga y exploración inicial
df = pd.read_csv('data.csv')
print(f"Dataset shape: {df.shape}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 2. Missing values analysis
missing_data = df.isnull().sum()
missing_percent = (missing_data / len(df)) * 100
missing_df = pd.DataFrame({
    'Column': missing_data.index,
    'Missing_Count': missing_data.values,
    'Missing_Percentage': missing_percent.values
}).sort_values('Missing_Percentage', ascending=False)

# 3. Outlier detection
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

# 4. Data type optimization
def optimize_dtypes(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            if df[col].nunique() / len(df) < 0.5:  # Likely categorical
                df[col] = df[col].astype('category')
        elif df[col].dtype == 'int64':
            if df[col].min() >= 0 and df[col].max() <= 255:
                df[col] = df[col].astype('uint8')
    return df
```

### Estrategias de Imputación
- **Numerical Missing Values:**
  - Mean/Median: Para distribuciones normales/skewed
  - Mode: Para categóricas
  - Forward/Backward fill: Para series temporales
  - Interpolation: Para datos temporales con tendencia
  - Model-based: KNN, regression imputation

- **Categorical Missing Values:**
  - Mode imputation
  - "Unknown" category
  - Model-based prediction

### Tratamiento de Outliers
```python
# Método de Winsorization
def winsorize(df, column, percentile=0.95):
    upper_limit = df[column].quantile(percentile)
    lower_limit = df[column].quantile(1 - percentile)
    df[column] = np.clip(df[column], lower_limit, upper_limit)
    return df

# Log transformation para skewed data
def log_transform(df, column):
    df[f'{column}_log'] = np.log1p(df[column])
    return df
```

## Quality Checks

### Data Quality Scorecard
- [ ] **Completeness:** % de valores no nulos
- [ ] **Validity:** % de valores en rangos esperados  
- [ ] **Consistency:** % de registros sin contradicciones
- [ ] **Accuracy:** % de valores correctos (si benchmark disponible)
- [ ] **Uniqueness:** % de registros únicos donde se espera

### Automated Quality Tests
```python
def data_quality_report(df):
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'missing_values_pct': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
        'duplicate_rows': df.duplicated().sum(),
        'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_columns': len(df.select_dtypes(include=['object', 'category']).columns)
    }
    return report
```

## Documentation Template

### Cleaning Log
```markdown
## Data Cleaning Report - [Dataset Name]

### Original Dataset
- **Rows:** 10,000
- **Columns:** 25
- **Size:** 15.2 MB

### Issues Identified
1. **Missing Values:** 15% en columna 'income'
2. **Outliers:** 50 valores extremos en 'age'
3. **Duplicates:** 25 registros duplicados
4. **Data Types:** 5 columnas mal tipificadas

### Actions Taken
1. **Imputación:** Income faltantes → Median por segmento
2. **Outliers:** Winsorization al 95% percentile
3. **Duplicates:** Eliminados basado en ID único
4. **Type Conversion:** object → category para variables con <10 levels

### Final Dataset
- **Rows:** 9,975 (-25 duplicados)
- **Columns:** 25
- **Size:** 12.8 MB
- **Quality Score:** 95%
```

---
*Template creado por: [Data Engineer]*