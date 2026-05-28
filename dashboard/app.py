from pathlib import Path
import streamlit as st
import duckdb
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "warehouse.duckdb"

st.title("DB Dashboard")

@st.cache_data(ttl=300)
def load_delays():
    with duckdb.connect(str(DB_PATH), read_only=True) as conn:
        return conn.execute("SELECT * FROM delays").df()

col_title, col_btn = st.columns([5, 1])
with col_btn:
    if st.button("Aktualisieren"):
        st.cache_data.clear()
        st.rerun()

df_delays = load_delays()

st.dataframe(df_delays)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Anzahl Züge mit Verspätung", len(df_delays))
with col2:
    st.metric("Durchschnittliche Verspätung", round(df_delays["verspaetung_min"].mean()))
with col3:
    st.metric("Maximale Verspätung", df_delays["verspaetung_min"].max())

st.subheader("Durchschnittliche Verspätung pro Linie")
df_by_line = df_delays.groupby("linie")["verspaetung_min"].mean().reset_index()
st.bar_chart(df_by_line.set_index("linie"))

bins = [0, 1, 6, 16, 999]
labels = ["Pünktlich", "1-5 min", "6-15 min", "15+ min"]
df_delays["kategorie"] = pd.cut(df_delays["verspaetung_min"], bins=bins, labels=labels, right=False)
st.subheader("Verspätungsverteilung")
df_dist = df_delays["kategorie"].value_counts().reset_index()
st.bar_chart(df_dist.set_index("kategorie"))
