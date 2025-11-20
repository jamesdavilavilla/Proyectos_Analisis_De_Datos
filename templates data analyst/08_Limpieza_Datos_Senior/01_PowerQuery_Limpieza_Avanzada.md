# Plantilla: Limpieza de Datos Senior — Power Query (M)

## Qué incluye
- Patrones avanzados y reutilizables en Power Query (M)
- Ejemplos prácticos y snippets listos para pegar
- Consejos de performance y debugging
- Checklist de validación final

---

## 1) Contrato breve (input/output)
- Input: una tabla con columnas heterogéneas (fechas como texto, números mezclados, strings ruidosos, nulos, duplicados)
- Output: tabla "limpia" lista para modelado: tipos correctos, claves consistentes, nulos imputados o marcados, outliers tratados, strings normalizados, índices y particionado si aplica

---

## 2) Patrones reutilizables (snippets)

### 2.1 Carga inicial y muestreo
```m
let
    Source = Csv.Document(File.Contents("C:\\datos\\mi_archivo.csv"),[Delimiter=",", Columns=0, Encoding=1252, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    // Muestra rápida para desarrollo: Table.FirstN(Promoted, 1000)
    Table0 = Promoted
in
    Table0
```

### 2.2 Normalizar nombres de columnas (snake_case)
```m
let
    NormalizeNames = (tbl as table) =>
    let
        cols = Table.ColumnNames(tbl),
        cols2 = List.Transform(cols, each Text.Lower(Text.Trim(_))),
        cols3 = List.Transform(cols2, each Text.Replace(Text.Replace(_, " ", "_"), "-", "_")),
        renamed = Table.RenameColumns(tbl, List.Zip({cols, cols3}), MissingField.Ignore)
    in
        renamed
in
    NormalizeNames
```

Uso: `Table1 = NormalizeNames(Table0)`

### 2.3 Forzar tipos con manejo de errores
```m
let
    SafeChangeType = (tbl as table, typeMap as list) =>
    let
        applyType = List.Accumulate(typeMap, tbl, (state, pair) =>
            let
                col = pair{0},
                t = pair{1},
                step = try Table.TransformColumnTypes(state, {{col, t}}) otherwise Table.TransformColumns(state, {{col, each try Value.ReplaceError(_, null) otherwise null}})
            in
                step
        )
    in
        applyType
in
    SafeChangeType
```

Ejemplo de `typeMap`: `{{"fecha","date"},{"importe","number"}}` (usar tipos M: type date, type number, type text, etc.)

### 2.4 Limpiar strings (trim, unicase, remover caracteres no imprimibles)
```m
let
    CleanText = (txt as nullable text) =>
    let
        t1 = if txt = null then null else Text.Trim(Text.Clean(txt)),
        t2 = if t1 = null then null else Text.Proper(Text.Normalize(t1, NormalizationForm.FormKD))
    in
        t2
in
    CleanText
```

Uso en tabla: `Table.TransformColumns(tbl, {{"columna_texto", CleanText, type text}})`

### 2.5 Detectar y eliminar duplicados por clave compuesta
```m
let
    RemoveDup = (tbl as table, key as list) => Table.Distinct(tbl, key)
in
    RemoveDup
```

### 2.6 Rellenar hacia abajo/arriba y reemplazar errores
```m
let
    FillAndReplace = (tbl as table, col as text) =>
    let
        filled = Table.FillDown(tbl, {col}),
        replaced = Table.ReplaceErrorValues(filled, {{col, null}})
    in
        replaced
in
    FillAndReplace
```

### 2.7 Imputación avanzada: mediana por grupo
```m
let
    ImputeMedianBy = (tbl as table, groupCols as list, targetCol as text) =>
    let
        grouped = Table.Group(tbl, groupCols, {"agg", each _ , type table}),
        filled = Table.TransformColumns(grouped, {"agg", (t)=>
            let
                med = List.Max(List.RemoveNulls(Table.Column(t, targetCol)))
            in
                Table.ReplaceValue(t, null, med, Replacer.ReplaceValue, {targetCol})
        }),
        ungroup = Table.Combine(Table.TransformRows(filled, each Record.Field(_, "agg")))
    in
        ungroup
in
    ImputeMedianBy
```
Nota: el ejemplo usa una estrategia simple; en datasets grandes calcular mediana debe hacerse con cuidado (usar List.Median en versiones que la soporten o calcular percentil).

### 2.8 Detectar outliers (IQR) y marcar
```m
let
    MarkOutliersIQR = (tbl as table, col as text) =>
    let
        values = List.Sort(List.RemoveNulls(Table.Column(tbl, col))),
        q1 = List.Percentile(values, 0.25),
        q3 = List.Percentile(values, 0.75),
        iqr = q3 - q1,
        lower = q1 - 1.5 * iqr,
        upper = q3 + 1.5 * iqr,
        added = Table.AddColumn(tbl, "is_outlier_" & col, each let v = Record.Field(_, col) in if v = null then false else (v < lower or v > upper))
    in
        added
in
    MarkOutliersIQR
```

### 2.9 Fuzzy merge (coincidencia aproximada) para uniones por nombres
```m
// En Power Query UI: Home -> Merge Queries -> usar "Fuzzy matching" y configurar threshold
// Snippet (aplicar desde GUI es más sencillo); parámetros comunes: Threshold=0.8, IgnoreCase=true, TransformationTable=null
```

### 2.10 Performance: usar Table.Buffer con precaución
- Usar `Table.Buffer` cuando reutilizas una tabla muchas veces en una consulta compleja para evitar recalculaciones.
- Evitar `Table.Buffer` en tablas enormes si no hay memoria suficiente.

Ejemplo:
```m
let
    buffered = Table.Buffer(FilteredTable),
    result = Table.AddColumn(buffered, "calc", each ...)
in
    result
```

---

## 3) Flujo completo recomendado (esqueleto)
1. Cargar fuente (CSV/Excel/DB)
2. Promover headers y normalizar nombres (`NormalizeNames`)
3. Eliminar columnas sin valor/ID de sistema
4. Aplicar limpieza de texto (`CleanText`) a columnas string
5. Forzar tipos con `SafeChangeType`
6. Detectar y separar filas con errores (`Table.RemoveRowsWithErrors` o marcarlas)
7. Imputar nulos por regla (grupo/mediana/moda)
8. Detectar outliers y marcarlos (no borrarlos automáticamente)
9. Eliminar duplicados por clave principal
10. Agregar columnas calculadas útiles (Año, Mes, Periodo)
11. Validación final: conteos, nulos por columna, tipado

---

## 4) Checklist de validación final
- [ ] Columnas con tipos correctos
- [ ] No hay duplicados en la clave primaria
- [ ] % de nulos por columna documentado
- [ ] Outliers marcados y justificación
- [ ] Strings normalizados (sin blancos, con casing coherente)
- [ ] Fechas en formato date
- [ ] Performance: tamaño final y memoria estimada

---

## 5) Debugging y logging
- Para debug rápido, use `Table.FirstN(tbl, 50)` en pasos intermedios.
- Use comentarios y pasos intermedios nombrados (ej. `Step_RemoveDup`) para poder retroceder.

---

## 6) Ejemplo práctico completo (mini consulta)
```m
let
    Source = Csv.Document(File.Contents("C:\\datos\\ventas_sample.csv"),[Delimiter=",", Encoding=1252, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Norm = NormalizeNames(Promoted),
    Trimmed = Table.TransformColumns(Norm, List.Transform(Table.ColumnNames(Norm), each {_, (x)=> if x = null then null else Text.Trim(Text.Clean(Text.From(x))), type text})),
    Types = SafeChangeType(Trimmed, {{"fecha","date"},{"importe","number"},{"cliente_id","text"}}),
    NoDup = RemoveDup(Types, {"cliente_id","fecha","producto"}),
    Imputed = ImputeMedianBy(NoDup, {"producto"}, "importe"),
    Outliers = MarkOutliersIQR(Imputed, "importe"),
    Final = Outliers
in
    Final
```

---

## 7) Notas finales y buenas prácticas
- Mantener pasos pequeños y con nombres. Evita una sola consulta monolítica.
- Documentar transformaciones clave en el editor de consultas (comentarios y descripciones).
- Versionar queries críticas (guardar M en repositorio de control de versiones).

---

**Archivo**: `01_PowerQuery_Limpieza_Avanzada.md` — creado en Nov 2025
