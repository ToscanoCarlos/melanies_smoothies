import streamlit as st
from snowflake.snowpark.functions import col

# Conexión con Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Título
st.title("🥤 Customize Your Smoothie!")

st.write("Choose the fruits you want in your custom Smoothie!")

# Nombre de la orden
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Obtener frutas desde Snowflake
my_dataframe = (
    session
    .table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
)

# Seleccionar ingredientes
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # INSERT: ahora guarda NAME_ON_ORDER e INGREDIENTS
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

            # Success message incluyendo NAME_ON_ORDER
            st.success(
                f"Your Smoothie is ordered, {name_on_order}!",
                icon="✅"
            )

        else:
            st.warning("Please enter a name for your Smoothie.")
