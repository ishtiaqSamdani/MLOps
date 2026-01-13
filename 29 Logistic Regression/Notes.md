# Lecture Notes: Classification and Logistic Regression

## 1. Introduction to Classification

Classification is a type of supervised learning where the target output variable  takes on a limited number of discrete values, as opposed to a continuous range (Linear Regression).

### 1.1 Binary Classification

The most common form is **Binary Classification**, where there are only two possible classes.

* **Classes:**
* **0 (Negative Class):** Represents "No", "False", or "Absence" (e.g., Benign tumor, Non-spam).
* **1 (Positive Class):** Represents "Yes", "True", or "Presence" (e.g., Malignant tumor, Spam).


* **Notation:** 

### 1.2 Limitations of Linear Regression for Classification

Using Linear Regression to fit a line to categorical data often fails for two reasons:

1. **Output Range:** Linear regression outputs values like  or , which do not make sense as probabilities.
2. **Sensitivity to Outliers:** Adding an outlier training example (e.g., a tumor size far to the right on the x-axis) shifts the best-fit line significantly, moving the decision threshold and causing misclassification of data points that were previously correctly classified.

---

## 2. The Logistic Regression Model

Despite the name, Logistic Regression is a **classification** algorithm. It solves the issues of linear regression by transforming the output to ensure it always falls between 0 and 1.

### 2.1 The Sigmoid Function (Logistic Function)

To map predictions to the interval , we use the Sigmoid function, denoted as .

**Properties of the Sigmoid:**

* If , .
* If , .
* If , .

### 2.2 Model Representation

The Logistic Regression model  applies the sigmoid function to the linear equation used in regression.

**Step 1:** Calculate the linear combination (z):


**Step 2:** Apply the sigmoid function:


### 2.3 Interpreting the Output

The output represents the **probability** that the class is 1 (positive) given input .

* **Example:** If , there is a 70% chance the output is 1.
* Because probabilities must sum to 1:



---

## 3. Decision Boundaries

The decision boundary is the line (or curve) that separates the area where  from the area where .

### 3.1 Thresholding

To predict a discrete class, a threshold is applied to the probability output:

* Predict  if 
* Predict  if 

### 3.2 Geometric Representation

Based on the sigmoid properties,  when . Therefore:

**The Decision Boundary** is defined by the equation:


* **Linear Decision Boundaries:** With features , the boundary is a straight line (e.g., ).
* **Non-Linear Decision Boundaries:** Using polynomial features (e.g., ), the boundary can be a circle, ellipse, or complex shape (e.g.,  creates a circular boundary).

---

## 4. Cost Function

We cannot use the Squared Error cost function from linear regression because the sigmoid function makes  **non-convex** (wavy with many local minima), preventing Gradient Descent from finding the global minimum.

### 4.1 The Logistic Loss Function

We define a specific Loss function  for a single training example that guarantees convexity (a single bowl shape).

* **If :** We want  to be close to 1. If , Loss . If , Loss .
* **If :** We want  to be close to 0. If , Loss . If , Loss .

### 4.2 Simplified Loss Representation

Because  is always either 0 or 1, we can compress the two cases into a single mathematical expression:

### 4.3 Total Cost Function

The cost  is the average loss over all  training examples.

*Note: This specific cost function is derived from the principle of Maximum Likelihood Estimation.*

---

## 5. Gradient Descent for Logistic Regression

To minimize the cost function , we apply Gradient Descent. We simultaneously update the parameters  and .

### 5.1 Update Rules

Repeat until convergence:

### 5.2 The Derivatives

Remarkably, the derivatives for Logistic Regression look identical to those for Linear Regression:

> **Critical Distinction:** While the update rules *look* the same as linear regression, they are mathematically distinct because the definition of  has changed.
> * Linear Regression: 
> * Logistic Regression: 
> 
> 

### 5.3 Implementation Concepts

* **Vectorization:** Vectorized implementations are used to speed up the calculation of the gradient.
* **Feature Scaling:** Scaling features to a similar range (e.g.,  to ) improves the convergence speed of Gradient Descent for Logistic Regression, just as it does for Linear Regression.

---
