# 📊 Fórmulas DAX Esenciales para Power BI

## 🎯 Introducción
Colección completa de fórmulas DAX organizadas por categoría para análisis de datos en Power BI.

---

## 📈 MEDIDAS DE VENTAS Y REVENUE

### Ventas Totales
```dax
Total Ventas = SUM(Ventas[Importe])
```

### Ventas Año Anterior (YoY)
```dax
Ventas Año Anterior = 
CALCULATE(
    [Total Ventas],
    SAMEPERIODLASTYEAR(Calendario[Fecha])
)
```

### Crecimiento YoY (%)
```dax
Crecimiento YoY % = 
DIVIDE(
    [Total Ventas] - [Ventas Año Anterior],
    [Ventas Año Anterior],
    0
)
```

### Ventas Acumuladas (YTD)
```dax
Ventas YTD = 
TOTALYTD(
    [Total Ventas],
    Calendario[Fecha]
)
```

### Ventas Mes Anterior
```dax
Ventas Mes Anterior = 
CALCULATE(
    [Total Ventas],
    DATEADD(Calendario[Fecha], -1, MONTH)
)
```

### Ventas Últimos 12 Meses (Rolling)
```dax
Ventas L12M = 
CALCULATE(
    [Total Ventas],
    DATESINPERIOD(
        Calendario[Fecha],
        LASTDATE(Calendario[Fecha]),
        -12,
        MONTH
    )
)
```

### Promedio Móvil 3 Meses
```dax
Promedio Móvil 3M = 
AVERAGEX(
    DATESINPERIOD(
        Calendario[Fecha],
        LASTDATE(Calendario[Fecha]),
        -3,
        MONTH
    ),
    [Total Ventas]
)
```

---

## 💰 MEDIDAS DE RENTABILIDAD

### Margen Bruto
```dax
Margen Bruto = [Total Ventas] - [Costo Total]
```

### Margen Bruto %
```dax
Margen Bruto % = 
DIVIDE(
    [Margen Bruto],
    [Total Ventas],
    0
)
```

### EBITDA
```dax
EBITDA = 
[Total Ventas] - 
[Costos Operativos] - 
[Gastos Administrativos] - 
[Gastos de Ventas]
```

### ROI (Retorno sobre Inversión)
```dax
ROI % = 
DIVIDE(
    [Margen Bruto] - [Inversión Marketing],
    [Inversión Marketing],
    0
)
```

---

## 👥 MEDIDAS DE CLIENTES

### Total Clientes
```dax
Total Clientes = DISTINCTCOUNT(Ventas[ClienteID])
```

### Clientes Nuevos
```dax
Clientes Nuevos = 
CALCULATE(
    DISTINCTCOUNT(Ventas[ClienteID]),
    FILTER(
        Clientes,
        Clientes[Fecha Primera Compra] >= MIN(Calendario[Fecha]) &&
        Clientes[Fecha Primera Compra] <= MAX(Calendario[Fecha])
    )
)
```

### Clientes Activos (Últimos 90 días)
```dax
Clientes Activos = 
CALCULATE(
    DISTINCTCOUNT(Ventas[ClienteID]),
    DATESINPERIOD(
        Calendario[Fecha],
        LASTDATE(Calendario[Fecha]),
        -90,
        DAY
    )
)
```

### Tasa de Retención
```dax
Tasa Retención % = 
VAR ClientesMesAnterior = 
    CALCULATE(
        DISTINCTCOUNT(Ventas[ClienteID]),
        DATEADD(Calendario[Fecha], -1, MONTH)
    )
VAR ClientesRepiten = 
    CALCULATE(
        DISTINCTCOUNT(Ventas[ClienteID]),
        FILTER(
            VALUES(Ventas[ClienteID]),
            CALCULATE(
                COUNTROWS(Ventas),
                DATEADD(Calendario[Fecha], -1, MONTH)
            ) > 0
        )
    )
RETURN
    DIVIDE(ClientesRepiten, ClientesMesAnterior, 0)
```

### Customer Lifetime Value (CLV)
```dax
CLV = 
DIVIDE(
    [Total Ventas],
    [Total Clientes],
    0
) * [Promedio Años Cliente]
```

### Ticket Promedio
```dax
Ticket Promedio = 
DIVIDE(
    [Total Ventas],
    COUNTROWS(Ventas),
    0
)
```

---

## 📊 MEDIDAS DE PRODUCTO

### Top N Productos por Ventas
```dax
Top 10 Productos = 
CALCULATE(
    [Total Ventas],
    TOPN(
        10,
        ALL(Productos[Nombre]),
        [Total Ventas],
        DESC
    )
)
```

### Análisis ABC (Clasificación)
```dax
Clasificación ABC = 
VAR TotalGeneral = [Total Ventas]
VAR VentasAcumuladas = 
    CALCULATE(
        [Total Ventas],
        FILTER(
            ALLSELECTED(Productos),
            [Total Ventas] >= EARLIER([Total Ventas])
        )
    )
VAR PorcentajeAcumulado = DIVIDE(VentasAcumuladas, TotalGeneral)
RETURN
    SWITCH(
        TRUE(),
        PorcentajeAcumulado <= 0.7, "A",
        PorcentajeAcumulado <= 0.9, "B",
        "C"
    )
```

### Rotación de Inventario
```dax
Rotación Inventario = 
DIVIDE(
    [Costo Total],
    [Inventario Promedio],
    0
)
```

### Stock Disponible
```dax
Stock Disponible = 
[Inventario Inicial] + 
[Compras] - 
[Ventas Unidades]
```

---

## ⏱️ INTELIGENCIA DE TIEMPO

### Mes a la Fecha (MTD)
```dax
Ventas MTD = 
TOTALMTD(
    [Total Ventas],
    Calendario[Fecha]
)
```

### Trimestre a la Fecha (QTD)
```dax
Ventas QTD = 
TOTALQTD(
    [Total Ventas],
    Calendario[Fecha]
)
```

### Comparación con Período Anterior
```dax
vs Período Anterior = 
VAR PeriodoActual = [Total Ventas]
VAR PeriodoAnterior = 
    CALCULATE(
        [Total Ventas],
        DATEADD(Calendario[Fecha], -1, MONTH)
    )
RETURN
    PeriodoActual - PeriodoAnterior
```

### Mismo Día Semana Anterior
```dax
Ventas Semana Anterior = 
CALCULATE(
    [Total Ventas],
    DATEADD(Calendario[Fecha], -7, DAY)
)
```

### Días Hábiles del Mes
```dax
Días Hábiles = 
CALCULATE(
    COUNTROWS(Calendario),
    Calendario[EsDiaHábil] = TRUE()
)
```

---

## 🎯 MEDIDAS DE PERFORMANCE

### % Cumplimiento de Meta
```dax
% Cumplimiento = 
DIVIDE(
    [Total Ventas],
    [Meta Ventas],
    0
)
```

### Semáforo de Performance
```dax
Estado Performance = 
SWITCH(
    TRUE(),
    [% Cumplimiento] >= 1, "🟢 Cumplido",
    [% Cumplimiento] >= 0.9, "🟡 En Progreso",
    "🔴 Bajo Meta"
)
```

### Varianza vs Budget
```dax
Varianza vs Budget = 
[Total Ventas] - [Budget]
```

### Varianza vs Budget %
```dax
Varianza % = 
DIVIDE(
    [Varianza vs Budget],
    [Budget],
    0
)
```

---

## 📌 RANKING Y CLASIFICACIONES

### Ranking de Vendedores
```dax
Ranking Vendedor = 
RANKX(
    ALL(Vendedores[Nombre]),
    [Total Ventas],
    ,
    DESC,
    DENSE
)
```

### Percentil de Ventas
```dax
Percentil 90 = 
PERCENTILEX.INC(
    ALL(Productos),
    [Total Ventas],
    0.9
)
```

### Top 20% (Pareto)
```dax
Es Top 20% = 
VAR RankingActual = [Ranking Vendedor]
VAR TotalVendedores = COUNTROWS(ALL(Vendedores))
RETURN
    IF(RankingActual <= TotalVendedores * 0.2, "Sí", "No")
```

---

## 🔄 MEDIDAS DINÁMICAS

### Medida Dinámica con Parámetro
```dax
Métrica Seleccionada = 
SWITCH(
    SELECTEDVALUE(Parámetro[Métrica]),
    "Ventas", [Total Ventas],
    "Margen", [Margen Bruto],
    "Unidades", [Total Unidades],
    "Clientes", [Total Clientes],
    BLANK()
)
```

### Título Dinámico
```dax
Título Dinámico = 
"Análisis de " & 
SELECTEDVALUE(Parámetro[Métrica]) & 
" - " & 
FORMAT(MAX(Calendario[Fecha]), "MMMM YYYY")
```

---

## 🔍 MEDIDAS DE ANÁLISIS AVANZADO

### Concentración de Ventas (Índice Herfindahl)
```dax
Índice Concentración = 
SUMX(
    VALUES(Productos[Nombre]),
    VAR VentasProducto = [Total Ventas]
    VAR VentasTotales = CALCULATE([Total Ventas], ALL(Productos))
    VAR Participación = DIVIDE(VentasProducto, VentasTotales, 0)
    RETURN Participación * Participación
)
```

### Coeficiente de Variación
```dax
CV Ventas = 
VAR Promedio = AVERAGE(Ventas[Importe])
VAR DesviacionEst = STDEV.P(Ventas[Importe])
RETURN
    DIVIDE(DesviacionEst, Promedio, 0)
```

### Z-Score (Detección de Outliers)
```dax
Z-Score = 
VAR VentaActual = [Total Ventas]
VAR Promedio = CALCULATE([Total Ventas], ALL(Calendario[Mes]))
VAR DesviacionEst = STDEVX.P(ALL(Calendario[Mes]), [Total Ventas])
RETURN
    DIVIDE(VentaActual - Promedio, DesviacionEst, 0)
```

### Tasa de Crecimiento Compuesto (CAGR)
```dax
CAGR = 
VAR ValorInicial = 
    CALCULATE(
        [Total Ventas],
        FIRSTDATE(ALL(Calendario[Fecha]))
    )
VAR ValorFinal = 
    CALCULATE(
        [Total Ventas],
        LASTDATE(ALL(Calendario[Fecha]))
    )
VAR Años = 
    DIVIDE(
        DATEDIFF(
            FIRSTDATE(ALL(Calendario[Fecha])),
            LASTDATE(ALL(Calendario[Fecha])),
            DAY
        ),
        365
    )
RETURN
    POWER(DIVIDE(ValorFinal, ValorInicial), DIVIDE(1, Años)) - 1
```

---

## 🎨 FORMATO CONDICIONAL

### Color Semáforo
```dax
Color Performance = 
VAR Cumplimiento = [% Cumplimiento]
RETURN
    SWITCH(
        TRUE(),
        Cumplimiento >= 1, "#00B050",      // Verde
        Cumplimiento >= 0.9, "#FFC000",    // Amarillo
        "#FF0000"                           // Rojo
    )
```

### Flecha de Tendencia
```dax
Tendencia = 
VAR Crecimiento = [Crecimiento YoY %]
RETURN
    SWITCH(
        TRUE(),
        Crecimiento > 0.05, "▲ Crecimiento",
        Crecimiento < -0.05, "▼ Decrecimiento",
        "◄► Estable"
    )
```

---

## 📋 TABLAS CALCULADAS

### Tabla de Calendario
```dax
Calendario = 
ADDCOLUMNS(
    CALENDAR(DATE(2020,1,1), DATE(2025,12,31)),
    "Año", YEAR([Date]),
    "Mes", MONTH([Date]),
    "Mes Nombre", FORMAT([Date], "MMMM"),
    "Trimestre", "Q" & QUARTER([Date]),
    "Día Semana", WEEKDAY([Date]),
    "Día Nombre", FORMAT([Date], "DDDD"),
    "Es Fin Semana", WEEKDAY([Date]) IN {1, 7},
    "Semana Año", WEEKNUM([Date]),
    "Año-Mes", FORMAT([Date], "YYYY-MM")
)
```

### Tabla de Parámetros
```dax
Parámetro Métrica = 
DATATABLE(
    "Orden", INTEGER,
    "Métrica", STRING,
    {
        {1, "Ventas"},
        {2, "Margen"},
        {3, "Unidades"},
        {4, "Clientes"}
    }
)
```

---

## 🔗 COLUMNAS CALCULADAS

### Edad de Cliente
```dax
Edad Cliente = 
DATEDIFF(
    Clientes[Fecha Nacimiento],
    TODAY(),
    YEAR
)
```

### Segmento RFM
```dax
Segmento RFM = 
VAR R = [Score Recencia]
VAR F = [Score Frecuencia]
VAR M = [Score Monetario]
RETURN
    SWITCH(
        TRUE(),
        R >= 4 && F >= 4 && M >= 4, "Champions",
        R >= 3 && F >= 3 && M >= 3, "Loyal",
        R >= 4 && F <= 2, "Promising",
        R <= 2 && F >= 4, "At Risk",
        R <= 2 && F <= 2, "Hibernating",
        "Other"
    )
```

### Categoría de Producto Consolidada
```dax
Categoría Principal = 
SWITCH(
    Productos[Categoría],
    "Electrónica", "Tecnología",
    "Computadoras", "Tecnología",
    "Celulares", "Tecnología",
    "Ropa", "Moda",
    "Calzado", "Moda",
    "Accesorios", "Moda",
    "Otros"
)
```

---

## 🚀 TIPS DE OPTIMIZACIÓN

### ✅ Mejores Prácticas

1. **Usar variables (VAR)** para cálculos repetidos
2. **DIVIDE en lugar de /** para evitar errores de división por cero
3. **ALL vs ALLSELECTED** - entender el contexto
4. **CALCULATE** para modificar contexto de filtro
5. **Evitar columnas calculadas** si se puede hacer con medidas
6. **Usar SELECTEDVALUE** en lugar de VALUES cuando esperas un solo valor

### ⚠️ Evitar

❌ **Columnas calculadas innecesarias** (usar medidas)
❌ **Funciones volátiles** como NOW(), TODAY() en columnas
❌ **Iteradores sin necesidad** (SUMX cuando SUM es suficiente)
❌ **Relaciones bidireccionales** sin justificación
❌ **ALL sin filtros** en tablas grandes

---

## 📚 PATRONES COMUNES

### Pattern: Previous Period
```dax
[Medida] Período Anterior = 
CALCULATE(
    [Medida],
    DATEADD(Calendario[Fecha], -1, [Período])
)
```

### Pattern: Dynamic TopN
```dax
TopN Dinámico = 
CALCULATE(
    [Total Ventas],
    TOPN(
        [Parámetro N],
        ALL([Dimensión]),
        [Total Ventas],
        DESC
    )
)
```

### Pattern: Running Total
```dax
Total Acumulado = 
CALCULATE(
    [Total Ventas],
    FILTER(
        ALL(Calendario[Fecha]),
        Calendario[Fecha] <= MAX(Calendario[Fecha])
    )
)
```

---

## 🎓 RECURSOS ADICIONALES

- **DAX Guide**: dax.guide
- **SQLBI**: sqlbi.com/articles
- **Microsoft Learn**: learn.microsoft.com/dax
- **DAX Formatter**: daxformatter.com

---

**Creado**: Noviembre 2025  
**Versión**: 1.0  
**Autor**: Data Analyst Portfolio

---

> 💡 **Tip**: Guarda este documento como referencia rápida. Todas estas fórmulas son funcionales y están listas para copiar y adaptar a tus necesidades específicas.
