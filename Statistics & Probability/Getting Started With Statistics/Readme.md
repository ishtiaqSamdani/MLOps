# Statistics for Data Science: Comprehensive Notes

## 1. Introduction to Statistics
**Definition:** Statistics is a field dealing with the **Collection, Organization, Analysis, Interpretation, and Presentation** of data.

* **Primary Goal:** To understand data to make informed decisions (Data-driven decision making).
* **Key Applications:**
    * Machine Learning & Data Science.
    * Business Intelligence & Analytics.
    * Risk Analysis (Banking).
    * Medical Studies (e.g., Vaccination safety/efficacy).

---

## 2. Types of Statistics
Statistics is broadly classified into two categories:

### A. Descriptive Statistics
Focuses on summarizing and organizing the data we have. It describes the features of a specific dataset.
* **Techniques involved:**
    * **Measure of Central Tendency:** Mean, Median, Mode.
    * **Measure of Dispersion:** Variance, Standard Deviation.
    * **Visualization:** Histograms, PDF, CDF.

### B. Inferential Statistics
Focuses on making conclusions (inferences) about a larger population based on a smaller sample.
* **Techniques involved:**
    * Hypothesis Testing (Z-test, t-test).
    * P-values.
* **Process:** Collect Sample Data $\rightarrow$ Perform Experiments $\rightarrow$ Infer about Population.

---

## 3. Population vs. Sample

| Term | Symbol | Definition | Example |
| :--- | :---: | :--- | :--- |
| **Population** | $N$ | The entire group you are studying. | All people in a country (Census). |
| **Sample** | $n$ | A subset of the population used to make inferences. | A survey of 10,000 voters (Exit Polls). |

> **Note:** Collecting data for the entire population is often impractical (cost/time), so we use samples.



---

## 4. Measure of Central Tendency
Used to identify the center point of a data distribution.

### A. Mean (Average)
The sum of all values divided by the number of values.

> **Population Mean ($\mu$):**
> $$\mu = \frac{\sum_{i=1}^{N} x_i}{N}$$

> **Sample Mean ($\bar{x}$):**
> $$\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}$$

* **Drawback:** Highly sensitive to **outliers** (extreme values can skew the mean significantly).

### B. Median
The middle value when the data is sorted in ascending order.
* **Procedure:** Sort data $\rightarrow$ Pick the central element.
* **Even number of elements:** Take the average of the two middle elements.
* **Advantage:** **Robust to outliers** (Outliers do not affect the median position).

### C. Mode
The most frequent element in the dataset.
* **Advantage:** Useful for categorical data and robust to outliers.

---

## 5. Measure of Dispersion (Spread)
Describes how "spread out" or dispersed the data is around the mean.

### A. Variance
The average squared difference of data points from the mean.

> **Population Variance ($\sigma^2$):**
> $$\sigma^2 = \frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}$$

> **Sample Variance ($s^2$):**
> $$s^2 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n - 1}$$

### B. Standard Deviation
The square root of the variance. It represents the distance of a data point from the mean in the same units as the data.

> **Population Std Dev ($\sigma$):**
> $$\sigma = \sqrt{\sigma^2}$$

> **Sample Std Dev ($s$):**
> $$s = \sqrt{s^2}$$

---

## 6. Bessel's Correction ($n-1$)
**Why do we divide by $n-1$ for Sample Variance?**
* If we divide by $n$, we tend to **underestimate** the true population variance (biased estimate).
* Using $n-1$ increases the result slightly, providing an **unbiased estimator** of the population variance.
* $n-1$ represents the **Degrees of Freedom**.

---

## 7. Variables and Random Variables

### A. Variable Types
A variable is a property that can take on any value.

1.  **Quantitative (Numerical):**
    * **Discrete:** Whole numbers, distinct counts. (e.g., No. of children, Bank accounts). No decimals allowed.
    * **Continuous:** Measurable quantities, can take any value within a range including decimals. (e.g., Height, Weight, Rainfall).
2.  **Qualitative (Categorical):**
    * Non-numerical categories. (e.g., Gender, Colors, Location).

### B. Random Variables ($X$)
A function that assigns values to outcomes of a random experiment.
* **Discrete Random Variable:** Outcomes are distinct (e.g., Tossing a coin: Head=0, Tail=1; Rolling a dice).
* **Continuous Random Variable:** Outcomes are infinite within a range (e.g., Time taken to run a race).

---

## 8. Histograms
A graphical representation of the distribution of numerical data.
* **Construction:** Data is grouped into "bins" (intervals). The height of the bar represents the frequency (count) of data points in that bin.
* **Usage:** Visualizing the underlying frequency distribution (e.g., Normal Distribution).
* **Smoothing:** Applying **Kernel Density Estimation (KDE)** to a histogram creates a **Probability Density Function (PDF)** curve.



---

## 9. Percentiles and Quartiles

### Percentile
A value below which a certain percentage of observations lie.
* *Example:* 99th percentile means the student scored better than 99% of the participants.

> **Formula for Rank/Index:**
> $$\text{Index} = \frac{\text{Percentile}}{100} \times (n + 1)$$

### Quartiles
Specific percentiles that divide the data into four equal parts.
1.  **Q1 (First Quartile):** 25th Percentile.
2.  **Q2 (Second Quartile):** 50th Percentile (The **Median**).
3.  **Q3 (Third Quartile):** 75th Percentile.

---

## 10. Five Number Summary & Outliers
Used to describe the distribution and identify outliers.

**The 5 Components:**
1.  Minimum
2.  Q1 (25%)
3.  Median (Q2)
4.  Q3 (75%)
5.  Maximum



**Detecting Outliers (Box Plot Method):**
To remove outliers, we calculate fences.

> **Interquartile Range (IQR):**
> $$IQR = Q3 - Q1$$

> **Lower Fence:**
> $$\text{Lower Fence} = Q1 - 1.5 \times IQR$$

> **Higher Fence:**
> $$\text{Higher Fence} = Q3 + 1.5 \times IQR$$

* *Rule:* Any data point **< Lower Fence** or **> Higher Fence** is considered an outlier.

---

## 11. Covariance and Correlation
Used to quantify the relationship between two continuous variables ($X$ and $Y$).

### A. Covariance
Measures the direction of the linear relationship.

> **Sample Covariance Formula:**
> $$Cov(X, Y) = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{n - 1}$$

* **Positive Covariance:** $X \uparrow$, $Y \uparrow$ (Variables move together).
* **Negative Covariance:** $X \uparrow$, $Y \downarrow$ (Variables move inversely).
* **Disadvantage:** The value is not normalized (ranges from $-\infty$ to $+\infty$). Hard to compare the strength of relationships across different datasets.

### B. Pearson Correlation Coefficient ($\rho$ or $r$)
Measures the **strength and direction** of the linear relationship. It normalizes covariance.

> **Formula:**
> $$\rho_{x,y} = \frac{Cov(X, Y)}{\sigma_x \sigma_y}$$

* **Range:** $[-1, 1]$
    * $+1$: Perfect positive correlation.
    * $-1$: Perfect negative correlation.
    * $0$: No linear correlation.
* **Limitation:** Only captures **linear** relationships.

### C. Spearman Rank Correlation
Used for non-linear (monotonic) relationships.
* **Method:** Instead of using raw values, it calculates the Pearson correlation on the **Ranks** of the data.
* **Formula:** Uses Covariance of Rank(X) and Rank(Y).
* **Advantage:** Captures monotonic relationships where Pearson might fail (e.g., an S-curve).