# Linear Regression and Performance Metrics

## 1. Introduction to Simple Linear Regression
Simple Linear Regression is a supervised machine learning algorithm used for solving **regression problems** (predicting continuous output values).

* **Goal:** To find a **Best Fit Line** that describes the relationship between a single independent input feature ($x$) and a dependent output feature ($y$).
* **Example:** Predicting *Height* (dependent) based on *Weight* (independent).



### Geometric Representation
The algorithm attempts to minimize the distance (error) between the true data points and the predicted points on the line.

---

## 2. Mathematical Equations and Notation

### The Hypothesis Function
The equation of the best fit line (prediction line) is denoted as:

$$h_\theta(x) = \theta_0 + \theta_1 x$$

* **$x$**: Independent feature (Input).
* **$h_\theta(x)$ or $\hat{y}$**: Predicted value.
* **$\theta_0$ (Intercept):** The value of $y$ when $x = 0$ (where the line crosses the y-axis).
* **$\theta_1$ (Slope/Coefficient):** Represents the unit movement in $y$ for a unit movement in $x$.

### The Error (Residual)
For any specific data point $i$, the error is the difference between the actual value and the predicted value:
$$Error = y^{(i)} - \hat{y}^{(i)}$$

---

## 3. Cost Function (Mean Squared Error)
To find the "best" line, we need to minimize the error across all data points. We use a **Cost Function**, denoted as $J(\theta_0, \theta_1)$.

The specific cost function used is **Mean Squared Error (MSE)**:

$$J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})^2$$

* **$m$**: Total number of data points.
* **Squaring**: Ensures positive values and penalizes larger errors.
* **$\frac{1}{2}$**: Added for mathematical convenience when calculating derivatives later.

**Visualizing the Cost Function:**
If we plot the Cost Function against the parameters ($\theta_0, \theta_1$), it forms a convex shape (like a bowl). The lowest point of this bowl is the **Global Minima**, which represents the optimal parameters for the best fit line.



---

## 4. Optimization: Gradient Descent & Convergence Algorithm
We cannot randomly guess $\theta_0$ and $\theta_1$. We use an optimization algorithm called **Gradient Descent** to find the values that minimize the cost function.

### The Algorithm
Repeat until convergence (reaching global minima):

$$\theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta_0, \theta_1)$$

* **$\alpha$ (Alpha) - Learning Rate:** Controls the speed of convergence (step size).
    * *Too small:* Slow convergence.
    * *Too large:* May overshoot the minima and fail to converge.
* **Derivative ($\frac{\partial}{\partial \theta_j}$):** Calculates the slope of the cost function at the current point.

### How it works (Slope Intuition)


1.  **Negative Slope:** The derivative is negative. The equation becomes $\theta_j := \theta_j - (-value)$, so $\theta_j$ increases (moves right toward minima).
2.  **Positive Slope:** The derivative is positive. The equation becomes $\theta_j := \theta_j - (+value)$, so $\theta_j$ decreases (moves left toward minima).

---

## 5. Multiple Linear Regression
When the dataset has **more than one** independent feature (e.g., House Price prediction based on Size, Rooms, Location).

### Equation
$$h_\theta(x) = \theta_0 + \theta_1 x_1 + \theta_2 x_2 + \dots + \theta_n x_n$$

* $\theta_0$: Intercept (always one).
* $\theta_1, \theta_2 \dots$: Coefficients corresponding to each specific feature.

The Gradient Descent concept remains the same, but it optimizes for all parameters ($\theta_0$ to $\theta_n$) simultaneously in an n-dimensional space.

---

## 6. Performance Metrics (R² and Adjusted R²)
Used to evaluate "how good" the model is.

### R-Squared ($R^2$)
Measures the proportion of variance in the dependent variable explained by the independent variables.

$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}}$$

* **$SS_{res}$ (Sum of Squares Residual):** $\sum (y_i - \hat{y}_i)^2$
* **$SS_{tot}$ (Sum of Squares Total):** $\sum (y_i - \bar{y})^2$ (Variance from the mean).
* **Range:** 0 to 1 (higher is usually better).

**Problem with $R^2$:**
$R^2$ **never decreases** when new features are added, even if those features are junk (not correlated with output).

### Adjusted R-Squared
Solves the problem of $R^2$ by penalizing the addition of irrelevant features.

$$Adjusted R^2 = 1 - (1-R^2) \frac{N - 1}{N - p - 1}$$

* $N$: Number of data points.
* $p$: Number of independent features.
* **Behavior:** If a new feature is not useful, Adjusted $R^2$ decreases. If it is useful, it increases.

---

## 7. Loss Functions Comparison (MSE vs. MAE vs. RMSE)

| Metric | Formula | Advantages | Disadvantages |
| :--- | :--- | :--- | :--- |
| **MSE** (Mean Squared Error) | $\frac{1}{n} \sum (y - \hat{y})^2$ | 1. Differentiable (great for gradient descent).<br>2. One global minima (convex). | 1. **Not robust to outliers** (squares the error, penalizing outliers heavily).<br>2. Changes the unit (e.g., \$ becomes \$²). |
| **MAE** (Mean Absolute Error) | $\frac{1}{n} \sum |y - \hat{y}|$ | 1. **Robust to outliers**.<br>2. Same unit as output. | 1. Not differentiable at 0 (requires sub-gradients).<br>2. Convergence takes more time. |
| **RMSE** (Root Mean Squared Error) | $\sqrt{MSE}$ | 1. Same unit as output.<br>2. Differentiable. | 1. Still not robust to outliers (inherits from MSE). |

---

## 8. Overfitting and Underfitting (Bias-Variance Trade-off)
To evaluate a model, data is split into **Train**, **Validation**, and **Test** sets.



### 1. Generalize Model (Ideal)
* High accuracy on Training Data.
* High accuracy on Test Data.
* **Characteristics:** Low Bias, Low Variance.

### 2. Overfitting
* High accuracy on Training Data.
* **Low accuracy** on Test Data.
* **Why:** The model learned the noise in the training data rather than the pattern.
* **Characteristics:** Low Bias, **High Variance**.

### 3. Underfitting
* **Low accuracy** on Training Data.
* Low accuracy on Test Data.
* **Why:** The model is too simple to capture the relationship.
* **Characteristics:** **High Bias**, High Variance.



---

## 9. Ordinary Least Squares (OLS)
OLS is a non-iterative (analytical) method to find the parameters $\beta_0$ (Intercept) and $\beta_1$ (Slope) by setting the derivatives of the error to zero.

### Derived Formulas
Instead of iterating like Gradient Descent, OLS calculates the parameters directly:

**1. Coefficient (Slope $\beta_1$):**
$$\beta_1 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n} (x_i - \bar{x})^2}$$

**2. Intercept ($\beta_0$):**
$$\beta_0 = \bar{y} - \beta_1 \bar{x}$$

*Note: OLS and Gradient Descent should yield approximately the same results for Linear Regression.*