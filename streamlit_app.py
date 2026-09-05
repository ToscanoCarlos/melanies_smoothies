if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

        # Título para cada fruta
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # Consultar API
        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + fruit_chosen
        )

        # Mostrar información nutricional
        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    # INSERT de la orden
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
