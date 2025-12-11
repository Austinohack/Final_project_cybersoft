import streamlit as st
from constants import top_products
key = "products"


def check_session():
    if key not in st.session_state:
        st.session_state[key] = top_products

    print(f"State with {key} is ready.")


def vnd(x: int | float) -> str:
    return f"{x:,}".replace(",", ".") + " VND"


def filter_products(items: list[dict], q: str) -> list[dict]:
    if not q:
        return items
    q = q.strip().lower()
    return [it for it in items if q in it["Tên sản phẩm"].lower()]


def fmt_table(items: list[dict]) -> list[dict]:
    rows = []
    for it in items:
        rows.append({
            "Tên sản phẩm": it["Tên sản phẩm"],
            "Số lượng bán": f'{it["Số lượng bán"]:,}'.replace(",", "."),
            "Danh mục": it["Danh mục"],
            "Giá bán (VND)": f'{it["Giá bán (VND)"]:,}'.replace(",", "."),
            "Tình trạng": it["Tình trạng"],
        })
    return rows
