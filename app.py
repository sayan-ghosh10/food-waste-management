import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# DB connection
engine = create_engine("postgresql+psycopg2://postgres:sayanghosh@localhost/food_waste_db")

st.set_page_config(page_title="Local Food Wastage Management", layout="wide")

# Tabs
tab1, tab2, tab3 = st.tabs(["🍲 Food Listings", "🛠 Manage Listings (CRUD)", "📊 Reports & Insights"])

# -----------------------------
# TAB 1: Food Listings
# -----------------------------
with tab1:
    st.header("Available Food Listings")

    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        city = st.selectbox("City", ["All"] + list(pd.read_sql("SELECT DISTINCT city FROM providers;", engine)['city']))
    with col2:
        provider_type = st.selectbox("Provider Type", ["All"] + list(pd.read_sql("SELECT DISTINCT type FROM providers;", engine)['type']))
    with col3:
        food_type = st.selectbox("Food Type", ["All"] + list(pd.read_sql("SELECT DISTINCT food_type FROM food_listings;", engine)['food_type']))
    with col4:
        meal_type = st.selectbox("Meal Type", ["All"] + list(pd.read_sql("SELECT DISTINCT meal_type FROM food_listings;", engine)['meal_type']))

    query = """
    SELECT f.food_id, f.food_name, f.quantity, f.expiry_date, f.food_type, f.meal_type, 
           p.name AS provider, p.city, p.contact
    FROM food_listings f
    JOIN providers p ON f.provider_id = p.provider_id
    WHERE 1=1
    """
    if city != "All": query += f" AND p.city = '{city}'"
    if provider_type != "All": query += f" AND p.type = '{provider_type}'"
    if food_type != "All": query += f" AND f.food_type = '{food_type}'"
    if meal_type != "All": query += f" AND f.meal_type = '{meal_type}'"

    df = pd.read_sql(query, engine)
    st.dataframe(df)

# -----------------------------
# TAB 2: Manage Listings (CRUD)
# -----------------------------
with tab2:
    st.header("Manage Food Listings")

    crud_choice = st.radio("Choose Operation", ["Add", "Update", "Delete"])

    # CREATE
    if crud_choice == "Add":
        with st.form("add_form"):
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1)
            expiry = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider ID", min_value=1)
            food_type_in = st.text_input("Food Type")
            meal_type_in = st.text_input("Meal Type")
            submitted = st.form_submit_button("Add")
            if submitted:
                with engine.begin() as conn:
                    conn.execute(text("""
                        INSERT INTO food_listings 
                        (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
                        VALUES (:food_name, :quantity, :expiry_date, :provider_id, 
                                (SELECT type FROM providers WHERE provider_id=:provider_id),
                                (SELECT city FROM providers WHERE provider_id=:provider_id),
                                :food_type, :meal_type)
                    """), {
                        "food_name": food_name, "quantity": quantity, "expiry_date": expiry,
                        "provider_id": provider_id, "food_type": food_type_in, "meal_type": meal_type_in
                    })
                st.success("✅ Food listing added successfully!")

    # UPDATE
    elif crud_choice == "Update":
        listings = pd.read_sql("SELECT food_id, food_name FROM food_listings;", engine)
        selected_id = st.selectbox("Select Food ID", listings['food_id'])

        new_name = st.text_input("New Food Name")
        new_qty = st.number_input("New Quantity", min_value=1)
        new_expiry = st.date_input("New Expiry Date")
        new_meal = st.text_input("New Meal Type")

        update_btn = st.button("Update")
        if update_btn:
            with engine.begin() as conn:
                conn.execute(text("""
                    UPDATE food_listings 
                    SET food_name=:n, quantity=:q, expiry_date=:e, meal_type=:m
                    WHERE food_id=:id
                """), {"n": new_name, "q": new_qty, "e": new_expiry, "m": new_meal, "id": selected_id})
            st.success("✅ Listing updated!")

    # DELETE
    elif crud_choice == "Delete":
        listings = pd.read_sql("SELECT food_id, food_name FROM food_listings;", engine)
        selected_id = st.selectbox("Select Food ID to Delete", listings['food_id'])
        delete_btn = st.button("Delete")
        if delete_btn:
            with engine.begin() as conn:
                conn.execute(text("DELETE FROM food_listings WHERE food_id=:id"), {"id": selected_id})
            st.success("🗑 Listing deleted!")

# -----------------------------
# TAB 3: Reports & Insights
# -----------------------------
with tab3:
    st.header("Reports & Insights")

    subtab1, subtab2, subtab3, subtab4 = st.tabs([
        "🏙 Providers & Receivers", 
        "🥗 Food Listings & Availability", 
        "📦 Claims & Distribution", 
        "📈 Analysis & Insights"
    ])

    # -------------------- Providers & Receivers --------------------
    with subtab1:
        #----------------- Question 1 -------------------------------
        st.subheader("1. How many food providers and receivers are there in each city?")
        st.markdown("#### Answer: ")
        st.markdown("##### ***Food Providers in each city:*** ")
        sql_providers = """
        SELECT city, COUNT(*) AS providers
        FROM providers
        GROUP BY city
        ORDER BY providers DESC;
        """
        st.code(sql_providers, language="sql")
        if st.button("▶ Run Query 1a"):
            df = pd.read_sql(sql_providers, engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("city"))
        st.markdown("##### ***Food Receivers in each city:*** ")
        sql_receivers = """
            SELECT city, COUNT(*) AS receivers
            FROM receivers
            GROUP BY city
            ORDER BY receivers DESC;
            """
        st.code(sql_receivers, language="sql")
        if st.button("▶ Run Query 1b"):
            df = pd.read_sql(sql_receivers, engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("city"))
        #----------------- Question 2 -------------------------------
        st.subheader("2. Which type of food provider (restaurant, grocery store, etc.) contributes the most food?")
        st.markdown("#### Answer: ")
        st.markdown("##### ***Provider Type Contributions***")
        q2 = """
        SELECT provider_type, SUM(quantity) AS total_quantity
        FROM food_listings GROUP BY provider_type ORDER BY total_quantity DESC;
        """
        st.code(q2, language="sql")
        if st.button("▶ Run Query 2"):
            df = pd.read_sql(q2, engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("provider_type"))
        
        #----------------- Question 3 -------------------------------
        st.subheader("3. What is the contact information of food providers in a specific city?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Contact Info of Providers per City***")
        q3="""
        SELECT name, type, city, contact FROM providers;
        """
        st.code(q3, language="sql")
        if st.button("▶ Run Query 3"):
            df = pd.read_sql(q3, engine)
            st.dataframe(df)

        #----------------- Question 4 -------------------------------
        st.subheader("4. Which receivers have claimed the most food?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Top Receivers by Food Claimed:***")
        q4 = """
            SELECT r.name, COALESCE(SUM(f.quantity),0) AS total_qty_claimed
            FROM claims c
            JOIN receivers r ON r.receiver_id=c.receiver_id
            JOIN food_listings f ON f.food_id=c.food_id
            GROUP BY r.name ORDER BY total_qty_claimed DESC;
        """
        st.code(q4, language="sql")
        if st.button("▶ Run Query 4:"):
            df=pd.read_sql(q4, engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("name"))

    # -------------------- Food Listings --------------------
    with subtab2:
        #----------------- Question 5 -----------------------
        st.subheader("5. What is the total quantity of food available from all providers?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Total Quantity of Food Available***")
        q5="""
        SELECT SUM(quantity) AS total_available_quantity 
        FROM food_listings;
        """
        st.code(q5, language="sql")
        if st.button("▶ Run Query 5:"):
            df = pd.read_sql(q5, engine)
            st.dataframe(df)

        #----------------- Question 6 -----------------------
        st.subheader("6. Which city has the highest number of food listings?")
        st.markdown("#### Answer:")
        st.markdown("##### ***City with Highest Number of Food Listings***")
        q6="""
            SELECT location AS city, COUNT(*) AS listings
            FROM food_listings GROUP BY location ORDER BY listings DESC;
        """
        st.code(q6,language="sql")
        if st.button("▶ Run Query 6:"):
            df = pd.read_sql(q6, engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("city"))
        #----------------- Question 7 -----------------------
        st.subheader("7. What are the most commonly available food types?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Most Commonly Available Food Types***")
        q7 = """
        SELECT food_type, COUNT(*) AS listings 
        FROM food_listings 
        GROUP BY food_type;
        """
        st.code(q7,language="sql")
        if st.button("▶ Run Query 7:"):
            df=pd.read_sql(q7,engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("food_type"))

    # -------------------- Claims & Distribution --------------------
    with subtab3:
        #----------------- Question 8 -----------------------
        st.subheader("8.How many food claims have been made for each food item?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Claims per Food Item***")
        q8 ="""
            SELECT f.food_name, COUNT(c.claim_id) AS claims_count
            FROM food_listings f
            LEFT JOIN claims c ON f.food_id=c.food_id
            GROUP BY f.food_name ORDER BY claims_count DESC;
        """
        st.code(q8,language="sql")
        if st.button("▶ Run Query 8:"):
            df=pd.read_sql(q8,engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("food_name"))
        #----------------- Question 9 -----------------------
        st.subheader("9. Which provider has had the highest number of successful food claims?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Provider with Highest Completed Claims***")
        q9 ="""
            SELECT p.name, COUNT(*) AS completed_claims
            FROM claims c
            JOIN food_listings f ON f.food_id=c.food_id
            JOIN providers p ON p.provider_id=f.provider_id
            WHERE LOWER(c.status)='completed'
            GROUP BY p.name ORDER BY completed_claims DESC;
        """
        st.code(q9,language="sql")
        if st.button("▶ Run Query 9:"):
            df=pd.read_sql(q9,engine)
            st.dataframe(df)
        #----------------- Question 10  ----------------------
        st.subheader("10. What percentage of food claims are completed vs. pending vs. canceled?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Claims by Status***")
        q10 ="""
        SELECT status, COUNT(*) AS cnt 
        FROM claims GROUP BY status;
        """
        st.code(q10,language="sql")
        if st.button("▶ Run Query 10:"):
            df=pd.read_sql(q10,engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("status"))

    # -------------------- Analysis & Insights --------------------
    with subtab4:
        #----------------- Question 11 -----------------------
        st.subheader("11. What is the average quantity of food claimed per receiver?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Avg Quantity Claimed per Receiver***")
        q11 ="""
            SELECT r.name, ROUND(AVG(f.quantity)::numeric,2) AS avg_qty
            FROM claims c
            JOIN receivers r ON r.receiver_id=c.receiver_id
            JOIN food_listings f ON f.food_id=c.food_id
            GROUP BY r.name ORDER BY avg_qty DESC;
        """
        st.code(q11,language="sql")
        if st.button("▶ Run Query 11:"):
            df=pd.read_sql(q11,engine)
            st.dataframe(df)
        #----------------- Question 12 -----------------------
        st.subheader("12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Most Claimed Meal Types***")
        q12 ="""
            SELECT f.meal_type, COUNT(*) AS claim_count
            FROM claims c
            JOIN food_listings f ON f.food_id=c.food_id
            GROUP BY f.meal_type ORDER BY claim_count DESC;
        """
        st.code(q12,language="sql")
        if st.button("▶ Run Query 12:"):
            df=pd.read_sql(q12,engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("meal_type"))
        #----------------- Question 13 -----------------------
        st.subheader("13. What is the total quantity of food donated by each provider?")
        st.markdown("#### Answer:")
        st.markdown("##### ***Total Quantity Donated by Each Provider***")
        q13 ="""
            SELECT p.name, COALESCE(SUM(f.quantity),0) AS total_donated
            FROM providers p
            LEFT JOIN food_listings f ON f.provider_id=p.provider_id
            GROUP BY p.name ORDER BY total_donated DESC;
        """
        st.code(q13,language="sql")
        if st.button("▶ Run Query 13:"):
            df=pd.read_sql(q13,engine)
            st.dataframe(df)
            st.bar_chart(df.set_index("name"))