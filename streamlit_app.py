import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Conexión con Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

st.title("🥤 Customize Your Smoothie!")

st.write("Choose the fruits you want in your custom Smoothie!")

# Nombre de la orden
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Obtener frutas y su valor de búsqueda
my_dataframe = (
    session
    .table("smoothies.public.fruit_options")
    .select(
        col("FRUIT_NAME"),
        col("SEARCH_ON")
    )
)

# Convertir Snowpark DataFrame a Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Multiselect: mostramos solamente FRUIT_NAME
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

        # Obtener SEARCH_ON correspondiente al FRUIT_NAME
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        st.write(
            "The search value for ",
            fruit_chosen,
            " is ",
            search_on,
            "."
        )

        # Mostrar información nutricional
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # La API ahora utiliza SEARCH_ON
        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    # Crear la orden
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders
            (name_on_order, ingredients)
        VALUES
            (?, ?)
    """

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        if name_on_order:
            session.sql(
                my_insert_stmt,
                params=[name_on_order, ingredients_string]
            ).collect()

            st.success(
                f"Your Smoothie is ordered, {name_on_order}!",
                icon="✅"
            )

        else:
            st.warning("Please enter a name for your Smoothie.")
