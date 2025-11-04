Here is the document in Markdown format.

````markdown
# Kata Solution: n8n Text-to-SQL Generation Agent

This document details the design, prompts, and analysis of a multi-stage system built in n8n to convert generic, natural language questions into executable MySQL queries. The system uses a chain of Large Language Model (LLM) calls to refine, generate, and, most importantly, validate the SQL before execution.

## 1. Prompt Engineering: Design and Rationale

The system is built on a "chain" of three distinct LLM prompts, each with a specific task.

### Prompt 1: The "Refinement Agent"

**Goal:** To convert a generic, ambiguous question (e.g., "How are sales?") into a specific, answerable question and identify the correct database.

**Prompt:**
```prompt
You are an expert data analyst assistant. Your task is to take a generic, ambiguous user question and refine it into a specific, detailed question that is answerable by a single database. You must also identify which database to query from the provided data catalog.

**Data Catalog:**

[
  {
    "database_name": "sales_db",
    "description": "Handles all customer transactions, product information, and orders.",
    "tables": ["customers", "products", "orders", "order_items"]
  },
  {
    "database_name": "hr_db",
    "description": "Contains employee information, departments, salaries, and hire dates.",
    "tables": ["employees", "departments"]
  }
]

**Your Task:**

1.  Analyze the user's generic question.
2.  Compare the question's intent against the "Data Catalog".
3.  Identify the single most relevant database.
4.  Formulate a "refined_question" that adds necessary business context. Make reasonable assumptions (e.g., "recent" means "last 30 days," "top" means "top 5").
5.  Your output *must* be a single, valid JSON object with two keys: "refined_question" and "database_name".

**Examples:**

User Question: "How are sales?"
Your Output:
{
  "refined_question": "What is the total sales revenue per product category for the last 30 days?",
  "database_name": "sales_db"
}

User Question: "Who are the new people?"
Your Output:
{
  "refined_question": "List all employees hired in the last 60 days, along with their department names.",
  "database_name": "hr_db"
}

---
**Current Request:**

User Question: "{{ $json.generic_question }}"
Your Output:
````

**Rationale:**

  * **Role-Playing:** Primes the LLM for high-quality, contextual understanding.
  * **Data Catalog (Context):** This is the most crucial part, acting as the "ground truth."
  * **Few-Shot Examples:** Demonstrates the exact JSON structure and logic of refinement.
  * **Strict JSON Output:** Paired with the n8n node's JSON setting for reliability.

-----

### Prompt 2: The "SQL Generation Agent"

**Goal:** To take the `refined_question` and the full database `schema` and generate a single, syntactically correct MySQL query.

**Prompt (Final Iteration):**

```prompt
You are an expert SQL database engineer. Your task is to write a single, accurate, and efficient SQL query to answer the given user question.

You will be given the database schema and the question.

**Example:**

Database Schema: hr_db
CREATE TABLE employees (employee_id INT, name VARCHAR);

User Question: "Show all employees"

JSON Output:
{
  "sql_query": "SELECT * FROM employees;"
}

---
**Current Request:**

**Database Schema: {{ $json[0].message.content.database_name }}**

{{ $json[0].schema }}

**User Question:**
"{{ $json[0].message.content.refined_question }}"

**Instructions:**

1.  Analyze the question and the provided schema.
2.  Write a single SQL query (assuming **MySQL** dialect).
3.  Your output must be *only* a single, valid JSON object with a single key named "sql_query", following the format in the example.

**JSON Output:**
```

**Rationale & Iterations:**

  * **Initial Challenge:** A "zero-shot" prompt (no examples) in text mode confused the LLM, causing garbled output.
  * **Iteration 1 (JSON Mode):** Solved garbled text but led to inconsistent JSON keys (e.g., `query` vs. `sql_query`).
  * **Iteration 2 (Few-Shot):** Adding a clear `Example` block forced the LLM to *consistently* use the `sql_query` key.

-----

### Prompt 3: The "SQL Validation Agent"

**Goal:** To check the LLM-generated SQL query against the schema for *both* semantic (e.g., non-existent tables) and syntactic errors.

**Prompt:**

```prompt
You are an expert SQL database validator. Your task is to check if a SQL query is syntactically valid AND semantically correct against a given schema.

Check for:
1.  Valid SQL syntax (SELECT, FROM, WHERE, etc.).
2.  Non-existent table names.
3.  Non-existent column names *within* their respective tables.

Respond *only* with a JSON object.

If the query is valid, use this format:
{"is_valid": true, "error_message": null}

If the query is invalid, provide a DETAILED, user-friendly `error_message` as shown in the example.

**Example of a good detailed error:**

Schema:
CREATE TABLE customers (customer_id INT, customer_name VARCHAR(255), region VARCHAR(100));

SQL Query:
SELECT name, region FROM users;

JSON Output:
{
  "is_valid": false,
  "error_message": "The query is invalid for two reasons: 1. It references a table named 'users', but this table does not exist in the schema. The correct table name is 'customers'. 2. It tries to select a column named 'name', but the 'customers' table does not have this column. The correct column name is 'customer_name'."
}

---
**Current Request:**

**Schema:**
{{ $json[0].schema }}

**SQL Query:**
{{ $json[0].generated_sql }}

**JSON Output:**
```

**Rationale:**

  * **Safety & Reliability:** A "meta-check" (an LLM checking another's work) is a necessary guardrail.
  * **Detailed Errors:** Providing a strong example of a detailed error trains the validator to provide user-friendly feedback.

## 2\. Examples of the System in Action

### Example 1: The "Happy Path" (Successful Query)

1.  **Generic Question:** `"who are new people?"`
2.  **Stage 1 (Refinement) Output:**
    ```json
    {
      "refined_question": "List all employees hired in the last 60 days, along with their department names.",
      "database_name": "hr_db"
    }
    ```
3.  **Stage 2 (SQL Generation) Output:**
    ```json
    {
      "sql_query": "SELECT e.first_name, e.last_name, d.department_name, e.hire_date FROM employees e JOIN departments d ON e.department_id = d.department_id WHERE e.hire_date >= CURDATE() - INTERVAL 60 DAY;"
    }
    ```
4.  **Stage 3 (Validation) Output:**
    ```json
    {
      "is_valid": true,
      "error_message": null
    }
    ```
5.  **Final Action:** `SUCCESS: Query is valid and safe. Action: Route to MySQL-HRDB credential for execution.`

### Example 2: The "Failure Path" (Invalid Query)

1.  **Generic Question:** `"Show all employee job titles"`
2.  **Stage 1 (Refinement) Output:**
    ```json
    {
      "refined_question": "List all employees and their job titles",
      "database_name": "hr_db"
    }
    ```
3.  **Stage 2 (SQL Generation) Output:** (The LLM "hallucinates" the `job_title` column)
    ```json
    {
      "sql_query": "SELECT first_name, last_name, job_title FROM employees;"
    }
    ```
4.  **Stage 3 (Validation) Output:**
    ```json
    {
      "is_valid": false,
      "error_message": "The query is invalid because it tries to select a column named 'job_title' from the 'employees' table, but this column does not exist."
    }
    ```
5.  **Final Action:** `FAILURE: Query is invalid. Action: Route to Error node. Workflow stopped.`

## 3\. Analysis of Effectiveness and Challenges

### Effectiveness

  * **Modularity:** Breaking the problem into three distinct LLM calls (Refine, Generate, Validate) was highly effective. Each node has one job, making the prompt simple and the output more reliable.
  * **Robustness:** The final system is very secure. The `Validation` step catches semantic errors (like bad column names), and an `IF` node guardrail blocks non-`SELECT` queries.
  * **Chained Context:** The n8n workflow was a perfect tool for this, allowing us to "chain" context. The `schema` was added only when needed, and the `refined_question` was passed all the way through.

### Challenges Encountered

  * **LLM Inconsistency (The `query` vs. `sql_query` problem):** The SQL Generation LLM would randomly change its output JSON key.
      * **Solution:** A "few-shot" prompt to force the correct key (`sql_query`) and a robust n8n expression (`...sql_query || ...query`) to catch failures.
  * **LLM "Meltdowns" (Garbled Text):** This was a critical configuration error from conflicting settings (JSON mode OFF, JSON prompt ON).
      * **Solution:** Aligning both—setting the node to JSON mode *and* explicitly asking for JSON in the prompt.
  * **n8n Context Management:** `Edit Fields` nodes replace data by default, which deleted previous data.
      * **Solution:** *Always* enabling the **"Include Other Input Fields"** toggle to ensure data was cumulative.

<!-- end list -->

```
```