# 📊 Análisis ABC - Template

## Información General
- **Objetivo:** Clasificar elementos por importancia (80/20 rule)
- **Aplicaciones:** Inventory, Customers, Products, Suppliers
- **Herramientas:** Excel, Python, SQL

## Metodología ABC

### Clasificación Estándar
- **Clase A:** 80% del valor (top 20% items)
- **Clase B:** 15% del valor (siguiente 30% items)  
- **Clase C:** 5% del valor (restante 50% items)

### Cálculo
```python
def abc_analysis(df, value_column, item_column):
    # Calcular valor acumulado
    df_sorted = df.sort_values(value_column, ascending=False)
    df_sorted['cumulative_value'] = df_sorted[value_column].cumsum()
    df_sorted['cumulative_percentage'] = df_sorted['cumulative_value'] / df_sorted[value_column].sum()
    
    # Clasificar
    df_sorted['ABC_Class'] = pd.cut(df_sorted['cumulative_percentage'], 
                                   bins=[0, 0.8, 0.95, 1], 
                                   labels=['A', 'B', 'C'])
    return df_sorted
```

## Aplicaciones por Área

### Inventory Management
- **Clase A:** Control estricto, stock safety alto
- **Clase B:** Control moderado, revisión periódica
- **Clase C:** Control básico, bulk ordering

### Customer Analysis
- **VIP Customers (A):** Account management dedicado
- **Regular Customers (B):** Programas de loyalty
- **Occasional Customers (C):** Marketing automation

### Product Portfolio
- **Star Products (A):** Máxima promoción y soporte
- **Standard Products (B):** Mantenimiento regular
- **Tail Products (C):** Evaluación de discontinuación

---
*Template creado por: [Business Analyst]*