# Local Food Wastage Management System

### Project Type  
EDA | SQL | Streamlit | Food Management | Social Good  

### Contribution  
Individual Project  

---

## 📖 Project Summary
Food wastage is a critical global issue, with tons of edible food discarded daily while many communities face food insecurity.  
This project aims to solve this problem by building a **Local Food Wastage Management System** that connects **food providers** (restaurants, grocery stores, supermarkets) with **receivers** (NGOs, individuals).  

Key highlights:
- Food providers list surplus food items.  
- Receivers can claim available food.  
- **PostgreSQL database** manages providers, receivers, food listings, and claims.  
- **Streamlit app** provides CRUD operations, filtering, and analysis.  
- **13 SQL-powered queries** generate insights into wastage, demand, and provider trends.  

---

## 🚀 Problem Statement
Food wastage reduction through redistribution:  
- Store provider, receiver, food, and claim data in SQL.  
- Enable filtering and contact options via a user-friendly interface.  
- Provide analytical insights into claims, contributions, and wastage trends.  

---

## 📂 Datasets
- `providers_data.csv` → details of food providers  
- `receivers_data.csv` → details of receivers  
- `food_listings_data.csv` → surplus food listings  
- `claims_data.csv` → food claims history  

SQL dump: `food_waste_db.sql`

---

## 🛠️ Approach

1. **Database Setup**  
   - Designed schema with 4 key tables: `Providers`, `Receivers`, `Food_Listings`, and `Claims`.  
   - Loaded cleaned CSV data into PostgreSQL.  

2. **CRUD Operations**  
   - Add, update, and delete records for providers, receivers, food, and claims.  

3. **SQL Analysis (15 Queries)**  
   - Providers & Receivers: count by city, top contributors, contact details.  
   - Food Listings: availability, city trends, most common food types.  
   - Claims & Distribution: completed vs pending claims, average quantity per receiver, top meal types.  

4. **Streamlit Application**  
   - Multi-page interface with:  
     - **CRUD Page** → manage records  
     - **Reports & Insights Page** → run queries, view results + charts  
     - **Contact Page** → connect with providers and receivers  

---

## 📊 Results & Insights

✅ Fully functional **Streamlit app**  
✅ Interactive filtering (city, provider, food type)  
✅ Direct contact with food providers/receivers  
✅ CRUD (Create, Read, Update, Delete) functionality  
✅ 15 SQL queries with both tabular and chart-based insights  

Examples:  
- **Most claimed meal type** → Lunch items dominated overall claims.  
- **City with highest demand** → Metro cities had maximum claim activity.  
- **Provider trends** → Restaurants contributed the largest food quantity.  
- **Claims status analysis** → 65% completed, 25% pending, 10% cancelled.  

---

## 📌 Example Queries
1. How many food providers and receivers are there in each city?  
2. Which provider has donated the most food?  
3. Which receivers have claimed the most food?  
4. What percentage of food claims are completed vs pending vs cancelled?  
5. Which city has the highest number of food listings?  

(All 13 queries are implemented in the app.)

---

## 📈 Screenshots
*(Add screenshots of your Streamlit app pages here – CRUD page, Insights page, charts, etc.)*

---

## ⚙️ Tech Stack
- **Python** (Pandas, SQLAlchemy)  
- **PostgreSQL**  
- **Streamlit**  
- **Matplotlib / Seaborn**  

---

## 🧪 Evaluation Metrics
- ✅ Completeness of SQL schema  
- ✅ Accuracy of queries  
- ✅ Functionality of CRUD operations  
- ✅ Quality of data insights & visualizations  
- ✅ User-friendly Streamlit interface  

---
## 📂 Repository Structure  

- ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) `app.py` — Streamlit app code  
- ![Postgres](https://img.shields.io/badge/-PostgreSQL-336791?logo=postgresql&logoColor=white) `food_waste_db.sql` — PostgreSQL dump file  
- ![CSV](https://img.shields.io/badge/-CSV-FFD43B?logo=file&logoColor=black) `providers_data.csv` — Providers dataset  
- ![CSV](https://img.shields.io/badge/-CSV-FFD43B?logo=file&logoColor=black) `receivers_data.csv` — Receivers dataset  
- ![CSV](https://img.shields.io/badge/-CSV-FFD43B?logo=file&logoColor=black) `food_listings_data.csv` — Food listings dataset  
- ![CSV](https://img.shields.io/badge/-CSV-FFD43B?logo=file&logoColor=black) `claims_data.csv` — Claims dataset  
- ![Dependencies](https://img.shields.io/badge/-Requirements.txt-blue?logo=dependabot&logoColor=white) `requirements.txt` — Python dependencies  
- ![Docs](https://img.shields.io/badge/-Docs-8CA1AF?logo=readthedocs&logoColor=white) `README.md` — Project documentation  


---

## 📌 How to Run
```bash
# Clone repo
git clone https://github.com/<sayan-ghosh10>/food-management-project.git
cd food-management-project

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app/app.py
________________________________________
✍️ Developed with ❤️ by Sayan Ghosh
