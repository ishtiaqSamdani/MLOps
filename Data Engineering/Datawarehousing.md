
### **6. Data Warehousing & Dimensional Modeling**

A **Data Warehouse** is a centralized storage system specifically optimized for analytics and reporting (OLAP). Unlike standard databases (OLTP) that handle day-to-day transactions, a Data Warehouse is designed to answer complex business questions like *"What was the total revenue for Product X in the last 5 years?"*

To make this analysis efficient, we cannot just dump data into the warehouse randomly; we must organize it using a technique called **Dimensional Modeling**.

---

### **A. Dimensional Modeling: Facts and Dimensions**
Dimensional modeling organizes data into two specific types of tables: **Facts** and **Dimensions**. This structure makes it easy for analysts to slice and dice data.

#### **1. Fact Table**
* **Definition:** The central table in your model that contains the quantitative (numerical) data or metrics about a business process.
* **Characteristics:** These numbers can be counted, summed, or averaged. The table usually consists of foreign keys pointing to dimension tables and the actual measurements.
* **Real-World Example (E-commerce Order):**
    * `Sales_Amount` ($20.00)
    * `Quantity_Sold` (1 unit)
    * `Discount_Amount` ($2.00)
    * `Tax_Amount` ($1.50)

#### **2. Dimension Table**
* **Definition:** These tables contain descriptive attributes (context) related to the measurements in the fact table. They answer the "Who, What, Where, and When."
* **Characteristics:** These are usually text fields used for filtering and grouping in reports.
* **Real-World Example:**
    * **Customer Dimension:** `Customer Name`, `City`, `Age`, `Email`.
    * **Product Dimension:** `Product Name`, `Category`, `Color`, `Brand`.
    * **Date Dimension:** `Month`, `Quarter`, `Year`, `Holiday_Flag`.

> **The Relationship:** If a user buys a phone case, the **Fact Table** records that 1 item was sold for $20. The **Dimension Tables** tell us *who* bought it (John), *what* it was (Phone Case), and *when* (Monday).



---

### **B. Schema Types: Star vs. Snowflake**
How do we connect these Fact and Dimension tables? There are two primary architecture patterns.

#### **1. Star Schema**
* **Definition:** The simplest design where a single central **Fact Table** is directly connected to multiple **Dimension Tables**. Visually, it looks like a star.
* **Key Feature:** Dimension tables are **denormalized**. This means all information about a product (Category, Brand, Description) is stored in a single `Product` table.
* **Pros:** Very fast for queries (fewer joins required).
* **Cons:** Uses more storage space due to duplicate data (e.g., the text "Electronics" is repeated for every electronic product).

#### **2. Snowflake Schema**
* **Definition:** An extension of the Star Schema where the dimension tables are **normalized** (broken down into sub-dimensions).
* **Example:** Instead of one big `Product` table, you might have a `Product` table connected to a `Category` table, which is connected to a `Brand` table.
* **Pros:** Saves storage space (less data redundancy).
* **Cons:** Slower performance because queries require many complex joins to get simple information.

> **Masterclass Verdict:** In the modern cloud era (storage is cheap), **Star Schema** is preferred because it is faster and simpler for analysts to understand.



[Image of Star Schema vs Snowflake Schema diagram]


---

### **C. Slowly Changing Dimensions (SCD)**
Data in dimension tables changes over time (e.g., a customer moves from New York to London). We need a strategy to handle these changes so our historical reports remain accurate. These strategies are called **SCDs**.

#### **SCD Type 1: Overwrite (No History)**
* **Action:** You simply delete the old value and type in the new value.
* **Example:** John moves from *New York* to *London*. We change his record to *London*.
* **Result:** If we run a report for "Sales in New York last year," John's sales will now wrongly appear under "London" because the history is lost.
* **Use Case:** Correcting spelling errors (e.g., changing "Nwe York" to "New York").

#### **SCD Type 2: Add New Row (Full History)**
* **Action:** You keep the old row as it is, mark it as "inactive," and create a brand new row for the new data with a new `Start_Date`.
* **Example:**
    * *Row 1:* John | New York | Active: False | End Date: 2023
    * *Row 2:* John | London | Active: True | Start Date: 2024
* **Result:** We can accurately report that John bought items in New York in 2023 and London in 2024.
* **Use Case:** Most common method for tracking customer or product changes.



#### **SCD Type 3: Add New Column (Limited History)**
* **Action:** You add a specific column to the existing row to hold the previous value.
* **Example:** The table has columns: `Current_City` and `Previous_City`.
* **Result:** You can only see the *current* and the *immediate last* value. If John moves a third time, the oldest history is lost.
* **Use Case:** When you only ever need to compare "This Year" vs "Last Year."

