# 🎛️ Análisis de Sensibilidad - Template

## Información General
- **Objetivo:** Evaluar impacto de cambios en variables clave
- **Métodos:** Scenario analysis, Monte Carlo, Tornado diagrams
- **Aplicaciones:** Financial modeling, Risk assessment, Decision making

## Metodología

### Análisis de Escenarios
- **Base Case:** Escenario más probable
- **Best Case:** Escenario optimista  
- **Worst Case:** Escenario pesimista
- **Custom Scenarios:** Situaciones específicas

### Variables de Entrada
- Volumen de ventas
- Precios
- Costos variables
- Costos fijos
- Tasas de conversión
- Market share

### One-Way Sensitivity
```python
def sensitivity_analysis(base_value, variable_range, formula):
    results = []
    for var in variable_range:
        output = formula(var)
        results.append({
            'input': var,
            'output': output,
            'change_%': (output - base_value) / base_value * 100
        })
    return pd.DataFrame(results)
```

### Tornado Diagram
- Ranking de variables por impacto
- Visualización de sensibilidades
- Identificación de drivers clave

---