# 🏗️ Modelo de Datos para Power BI - Template

## Estructura del Modelo

### Star Schema Design
- **Fact Tables:** Contienen métricas y eventos
- **Dimension Tables:** Contienen atributos descriptivos
- **Bridge Tables:** Para relaciones many-to-many
- **Calendar Table:** Dimensión temporal estándar

### Best Practices
- Usar integer keys para relaciones
- Fact tables normalizadas
- Dimension tables denormalizadas
- Naming conventions consistentes

## Tables Recomendadas

### Fact Tables
- **Sales_Fact**
- **Budget_Fact**  
- **Inventory_Fact**
- **Customer_Activity_Fact**

### Dimension Tables
- **Dim_Date**
- **Dim_Customer**
- **Dim_Product**
- **Dim_Geography**
- **Dim_Employee**

### Calendar Table DAX
```dax
Calendar = 
ADDCOLUMNS(
    CALENDAR(DATE(2020,1,1), DATE(2025,12,31)),
    "Year", YEAR([Date]),
    "Quarter", "Q" & QUARTER([Date]),
    "Month", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMMM"),
    "Weekday", WEEKDAY([Date]),
    "WeekdayName", FORMAT([Date], "DDDD")
)
```

---