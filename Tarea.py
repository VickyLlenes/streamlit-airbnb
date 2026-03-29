import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("Airbnb analisis")
df = pd.read_csv("airbnb.csv")
st.subheader("Victoria Llenes")
#st.write(df.head())
#st.write(df.columns)

df["price"] = pd.to_numeric(df["price"])
df["minimum_nights"] = pd.to_numeric(df["minimum_nights"])
df["number_of_reviews"] = pd.to_numeric(df["number_of_reviews"])
df["reviews_per_month"] = pd.to_numeric(df["reviews_per_month"])
df["availability_365"] = pd.to_numeric(df["availability_365"])

df = df.dropna(subset=["neighbourhood", "room_type", "price", "minimum_nights"])

st.sidebar.header("Filtros")

room = st.sidebar.multiselect(
    "Tipo de cuarto",
    df["room_type"].dropna().unique(),
    placeholder="Selecciona un cuarto"
)

barrio = st.sidebar.selectbox(
    "Tipo de barrio",
    ["Selecciona tipo"] + list(df["neighbourhood_group"].dropna().unique())
)

df_filtrado = df.copy()

if barrio != "Selecciona tipo":
    df_filtrado = df_filtrado[df_filtrado["neighbourhood_group"] == barrio]

if room:
    df_filtrado = df_filtrado[df_filtrado["room_type"].isin(room)]

tab1, tab2, tab3 = st.tabs(["Overview", "Analysis", "Simulator"])


with tab1:
    #st.subheader("Datos filtrados")
    #st.dataframe(df_filtrado)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Precio promedio por barrio")
        precio_barrio = df_filtrado.groupby("neighbourhood")["price"].mean().sort_values(ascending=False).head(10)
        st.bar_chart(precio_barrio)

    with col2:
        st.subheader("Cantidad de alojamientos por barrio")
        anuncios_barrio = df_filtrado["neighbourhood"].value_counts().head(10)
        st.bar_chart(anuncios_barrio)
    
with tab2:
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average availability by neighbourhood")

        availability_barrio = (
            df_filtrado.groupby("neighbourhood")["availability_365"]
            .mean()
            .round(0)
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(availability_barrio)
        
    with col2:
        st.subheader("Reviews vs Precio")
        st.scatter_chart(df_filtrado[["number_of_reviews", "price"]])

with tab3:
    st.subheader("Price recommendation simulator")

    sim_neighbourhood = st.selectbox(
        "Choose neighbourhood",
        sorted(df["neighbourhood"].dropna().unique())
    )

    sim_room_type = st.selectbox(
        "Choose room type",
        sorted(df["room_type"].dropna().unique())
    )

    sim_min_nights = st.slider(
        "Minimum nights",
        int(df["minimum_nights"].min()),
        int(df["minimum_nights"].max()),
        3
    )

    similares = df[
        (df["neighbourhood"] == sim_neighbourhood) &
        (df["room_type"] == sim_room_type)
    ].copy()

    if not similares.empty:
        similares["diff_nights"] = (similares["minimum_nights"] - sim_min_nights).abs()
        similares = similares.sort_values("diff_nights").head(20)

        p25 = similares["price"].quantile(0.25)
        p50 = similares["price"].median()
        p75 = similares["price"].quantile(0.75)

        st.write(f"Recommended price range: {p25:.0f} - {p75:.0f}")
        st.write(f"Suggested central price: {p50:.0f}")

        st.dataframe(
            similares[["name", "neighbourhood", "room_type", "minimum_nights", "price"]]
        )
    else:
        st.warning("No similar apartments found.")