# Limpieza de Datos Senior — Plantillas

Contenido:
- `01_PowerQuery_Limpieza_Avanzada.md`: pasos y snippets M (Power Query)
- `02_Python_Limpieza_Avanzada.py`: script con pipeline en pandas
- `requirements.txt`: dependencias para el script Python

Uso rápido (Python):

1. Crear un entorno virtual (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
```

2. Ejecutar el script sobre un CSV de ejemplo:

```powershell
python 02_Python_Limpieza_Avanzada.py --input datos/raw/ventas.csv --output datos/clean/ventas_clean.csv
```

Notas:
- Ajusta los nombres de columnas en el script si tu dataset usa nombres distintos (ej. 'importe', 'producto').
- El archivo `01_PowerQuery_Limpieza_Avanzada.md` contiene snippets listos para pegar en Power Query y patrones de validación.

Siguientes pasos sugeridos:
- Agregar tests unitarios para funciones Python (pytest)
- Añadir transformaciones específicas del negocio (ej. reglas de cartera, jerarquías de producto)
- Implementar un notebook de demostración con un dataset toy
