"""
Script: Limpieza avanzada de datos (pandas)
- Funciones reutilizables para inspección, normalización, imputación, outliers, reducción de memoria y export
- Uso: python 02_Python_Limpieza_Avanzada.py --input datos.csv --output datos_clean.csv
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

# --------------------------------------------------
# Utilidades
# --------------------------------------------------

def load_csv(path, nrows=None, encoding='utf-8'):
    return pd.read_csv(path, nrows=nrows, encoding=encoding)


def profile_df(df):
    """Rápido perfil: tipos, nulos, unique, memory"""
    mem = df.memory_usage(deep=True).sum()
    profile = pd.DataFrame({
        'dtype': df.dtypes.astype(str),
        'n_nulls': df.isna().sum(),
        'pct_nulls': df.isna().mean(),
        'n_unique': df.nunique(dropna=True)
    })
    profile['memory_bytes'] = [df[col].memory_usage(deep=True) for col in df.columns]
    return profile, mem


def normalize_column_names(df):
    df = df.rename(columns=lambda c: str(c).strip().lower().replace(' ', '_').replace('-', '_'))
    return df


def parse_dates(df, cols):
    for c in cols:
        df[c] = pd.to_datetime(df[c], errors='coerce')
    return df


def clean_text_columns(df, cols):
    for c in cols:
        df[c] = df[c].astype('string')
        df[c] = df[c].str.strip()
        df[c] = df[c].str.replace('\u00A0', ' ', regex=False)
        df[c] = df[c].str.replace('[^\x00-\x7F]', '', regex=True)  # remover no-ascii
        df[c] = df[c].str.replace('\s+', ' ', regex=True)
        df[c] = df[c].str.title()
    return df


def downcast_numeric(df):
    for col in df.select_dtypes(include=['int','int64','float','float64']).columns:
        col_min = df[col].min()
        col_max = df[col].max()
        if pd.isna(col_min) or pd.isna(col_max):
            continue
        if pd.api.types.is_float_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], downcast='float')
        else:
            df[col] = pd.to_numeric(df[col], downcast='integer')
    return df


def reduce_memory(df):
    # Convert object/string columns with low cardinality to category
    for col in df.select_dtypes(include=['object','string']).columns:
        num_unique = df[col].nunique(dropna=True)
        num_total = len(df[col])
        if num_unique / num_total < 0.5:
            df[col] = df[col].astype('category')
    df = downcast_numeric(df)
    return df


def remove_duplicates(df, subset=None):
    return df.drop_duplicates(subset=subset)


def impute_median_by_group(df, group_cols, target_col):
    medians = df.groupby(group_cols)[target_col].median()
    df[target_col] = df.apply(lambda r: medians.get(tuple(r[g] for g in group_cols)) if pd.isna(r[target_col]) else r[target_col], axis=1)
    return df


def mark_outliers_iqr(df, col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    marker = f'is_outlier_{col}'
    df[marker] = df[col].apply(lambda v: False if pd.isna(v) else (v < lower or v > upper))
    return df


def impute_knn(df, cols, n_neighbors=5):
    imputer = KNNImputer(n_neighbors=n_neighbors)
    sub = df[cols]
    knn_res = imputer.fit_transform(sub)
    df[cols] = knn_res
    return df


def encode_top_categories(df, col, top_n=10, other_label='OTHER'):
    top = df[col].value_counts().nlargest(top_n).index
    df[col] = df[col].where(df[col].isin(top), other_label)
    return df


# --------------------------------------------------
# Pipeline principal
# --------------------------------------------------

def clean_pipeline(path_in, path_out, sample=None):
    df = load_csv(path_in, nrows=sample)

    df = normalize_column_names(df)

    # Ejemplo: detectar columnas de fecha/text automáticamente (heurística)
    # El usuario puede ajustar esto según su dataset
    # Heurística simple para columnas de fecha
    date_cols = [c for c in df.columns if 'date' in c or 'fecha' in c or 'dia' in c]
    df = parse_dates(df, date_cols)

    # Limpiar texto (aplicar a object/string cols)
    text_cols = df.select_dtypes(include=['object','string']).columns.tolist()
    df = clean_text_columns(df, text_cols)

    # Remover duplicados por todas las columnas clave si se detectan
    # Aquí no asumimos clave, dejamos al usuario pasar subset si hace falta
    df = remove_duplicates(df)

    # Marcar outliers en columnas numéricas clave (ejemplo: 'importe') si existe
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'importe' in num_cols:
        df = mark_outliers_iqr(df, 'importe')

    # Imputación por grupo ejemplo
    if 'producto' in df.columns and 'importe' in df.columns:
        df = impute_median_by_group(df, ['producto'], 'importe')

    # Reducción de memoria
    df = reduce_memory(df)

    # Guardar
    df.to_csv(path_out, index=False)
    return df


# --------------------------------------------------
# CLI
# --------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Limpieza avanzada de datos (pandas)')
    parser.add_argument('--input', '-i', required=True, help='Ruta al CSV de entrada')
    parser.add_argument('--output', '-o', required=True, help='Ruta de salida para CSV limpio')
    parser.add_argument('--sample', '-n', type=int, help='Cargar solo n filas para debug')
    args = parser.parse_args()

    df_clean = clean_pipeline(args.input, args.output, sample=args.sample)
    prof, mem = profile_df(df_clean)
    print('Perfil final:')
    print(prof)
    print(f'Total memory bytes: {mem}')
