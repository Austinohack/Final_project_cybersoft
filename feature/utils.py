
import pandas as pd
import glob
import os
import streamlit as st

key = "products"


# def check_session():
#     if key not in st.session_state:
#         st.session_state[key] = top_products

#     print(f"State with {key} is ready.")


# def vnd(x: int | float) -> str:
#     return f"{x:,}".replace(",", ".") + " VND"


# def filter_products(items: list[dict], q: str) -> list[dict]:
#     if not q:
#         return items
#     q = q.strip().lower()
#     return [it for it in items if q in it["Tên sản phẩm"].lower()]


# def fmt_table(items: list[dict]) -> list[dict]:
#     rows = []
#     for it in items:
#         rows.append({
#             "Tên sản phẩm": it["Tên sản phẩm"],
#             "Số lượng bán": f'{it["Số lượng bán"]:,}'.replace(",", "."),
#             "Danh mục": it["Danh mục"],
#             "Giá bán (VND)": f'{it["Giá bán (VND)"]:,}'.replace(",", "."),
#             "Tình trạng": it["Tình trạng"],
#         })
#     return rows

def load_movies_data(path: str) -> pd.DataFrame:
    """
    Load movie data from a file or a folder.

    Parameters
    ----------
    path : str
        - CSV file path  (e.g. data/clean/movies_clean.csv)
        - Folder path    (e.g. data/financial)

    Returns
    -------
    pd.DataFrame
        Concatenated dataframe
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")

    # -------- Case 1: single CSV --------
    if os.path.isfile(path):
        if not path.endswith(".csv"):
            raise ValueError("Only CSV files are supported")
        return pd.read_csv(path)

    # -------- Case 2: folder with CSVs --------
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in folder: {path}")

    dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        df["_source"] = os.path.basename(file)  # optional, for debugging / insight
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
