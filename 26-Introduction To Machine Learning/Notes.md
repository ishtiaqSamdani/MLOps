# Machine Learning & Data Science Course Notes

## 1. AI, Machine Learning, Deep Learning, and Data Science
Understanding the hierarchy and distinctions between these terminologies is fundamental to the field.

### A. Artificial Intelligence (AI)
The broadest universe in this context.
* **Definition:** Creating an application capable of performing its own tasks without any human intervention.
* **Examples:**
    * **Netflix Recommendation System:** Automatically suggests movies based on viewing history.
    * **Self-Driving Cars:** Vehicles that detect traffic lights and objects to drive autonomously.
    * **E-commerce:** Product recommendations based on user activity.

### B. Machine Learning (ML)
A subset of Artificial Intelligence.
* **Definition:** Provides statistical tools to analyze, visualize, predict, and forecast data.
* **Goal:** To analyze data and derive insights or predictions.

### C. Deep Learning (DL)
A subset of Machine Learning.
* **Origin:** In the 1950s, scientists aimed to train machines to learn similarly to the human brain.
* **Mechanism:** Uses **Multi-Layered Neural Networks** to mimic human learning processes.
* **Application:** Used for complex tasks (e.g., image recognition, natural language processing).

### D. Data Science
An overarching field that overlaps with AI, ML, and DL.
* **Scope:** Utilizes mathematics, statistics, linear algebra, and tools from AI/ML/DL to solve complex data problems.
* **Role:** A Data Scientist may work on EDA (Exploratory Data Analysis), feature engineering, or building AI applications depending on the project.

---

## 2. Types of Machine Learning Techniques

### A. Supervised Machine Learning
Learning where the model is trained on a labeled dataset containing both input (independent) features and output (dependent) features.

* **Key Components:**
    * **Independent Features:** Input data (e.g., Size of House, Number of Rooms).
    * **Dependent Feature:** Output data to be predicted (e.g., Price of House).
* **Problem Types:**
    1.  **Regression:** The output feature is **continuous** (e.g., House Price: $450k, $500k).
    2.  **Classification:** The output feature is **categorical**.
        * *Binary Classification:* Two categories (e.g., Pass/Fail).
        * *Multi-class Classification:* More than two categories.

**Algorithms:**
* *Regression:* Linear Regression, Ridge, Lasso, Elastic Net.
* *Classification:* Logistic Regression.
* *Hybrid:* Decision Trees, Random Forest, AdaBoost, XGBoost.

### B. Unsupervised Machine Learning
Learning where the data is unlabeled (no output/dependent feature).

* **Goal:** To find patterns, structures, or groups (clusters) within the data.
* **Example: Customer Segmentation**
    * *Features:* Salary, Spending Score.
    * *Objective:* Group customers (e.g., "High Salary, High Spending" vs. "Low Salary, Low Spending") to target marketing.
* **Algorithms:** K-Means Clustering, Hierarchical Clustering, DBScan.

### C. Reinforcement Learning
A method where an agent learns to make decisions by performing actions and receiving feedback.
* **Mechanism:** Learning via **Rewards and Penalties**.
* **Analogy:** A baby learning to walk (trying, falling/pain, adjusting, succeeding/reward).

---

## 3. Mathematical Foundations: Lines, Planes, and Hyperplanes

This section covers the geometric intuition required for algorithms like Logistic Regression and Support Vector Machines (SVM).

### A. Equation of a Straight Line (2D)
In a 2-dimensional space ($x, y$ axes), a line is represented as:
$$y = mx + c$$
Or in general form:
$$ax + by + c = 0$$

**Vector Notation:**
For feature spaces, we use weights ($w$) and inputs ($x$).
$$w^T x + b = 0$$

* **$w$ (Weights):** Represents the coefficients/slope.
* **$b$ (Bias/Intercept):** The point where the line intercepts the axis when $x=0$.
* **Line passing through origin:** If the intercept $b=0$:
$$w^T x = 0$$

### B. Equation of a Plane (3D) and Hyperplane ($n$-dimensions)
* **3D Plane:** With axes $x_1, x_2, x_3$:
$$w_1x_1 + w_2x_2 + w_3x_3 + b = 0$$
* **Hyperplane ($n$-dimensions):**
$$\pi : w^T x + b = 0$$

**Geometric Property of $w$:**
The vector $w$ is always **perpendicular (normal)** to the plane/hyperplane $\pi$.

---

## 4. Distance of a Point from a Plane

### A. The Setup
* Let $\pi$ be a plane passing through the origin defined by $w^T x = 0$.
* Let $w$ be the normal vector to the plane.
* Let $S$ be a point vector.

### B. Distance Formula
The distance $d$ of point $S$ from the plane defined by $w$ is given by:

$$d = \frac{w^T S}{||w||}$$

### C. Interpretation using Dot Product
From linear algebra, the dot product is defined as:
$$w^T S = ||w|| \cdot ||S|| \cos\theta$$

**Significance of the Sign:**
1.  **Positive Distance:** If the point $S$ is on the same side as the normal vector $w$ ($\theta < 90^{\circ}$), the distance is positive.
2.  **Negative Distance:** If the point $S$ is on the opposite side of the plane ($\theta > 90^{\circ}$), the result is negative.