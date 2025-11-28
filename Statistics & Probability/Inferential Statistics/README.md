# Statistics and Hypothesis Testing Notes

## 1. Hypothesis Testing Mechanism
Hypothesis testing is a part of **Inferential Statistics**. The goal is to draw conclusions (inferences) about an unknown population parameter using sample data.

### **The 4 Steps of Hypothesis Testing**
1.  **Null Hypothesis ($H_0$):** The default assumption or the status quo. The assumption you begin with (e.g., "The person is not guilty").
2.  **Alternate Hypothesis ($H_1$):** The opposite of the Null Hypothesis. The conclusion you want to prove (e.g., "The person is guilty").
3.  **Statistical Analysis:** Perform experiments (Z-test, T-test, Chi-Square, ANOVA) to collect proof.
4.  **Conclusion:** Decide whether to **Accept** (Fail to Reject) or **Reject** the Null Hypothesis based on P-values and Significance levels.

---

## 2. P-Value and Significance Level
The **P-value** is the probability of finding the observed, or more extreme, results when the Null Hypothesis ($H_0$) is true.

* **Significance Level ($\alpha$):** A threshold set by the domain expert (commonly 0.05). It defines the **Confidence Interval (CI)**.
    * If $CI = 95\%$, then $\alpha = 1 - 0.95 = 0.05$.
* **Decision Rule:**
    > **If $P\text{-value} < \alpha$:** Reject $H_0$ (The result is statistically significant).
    >
    > **If $P\text{-value} > \alpha$:** Fail to reject $H_0$.



[Image of hypothesis testing rejection region]


---

## 3. Z-Test
Used to determine if there is a significant difference between sample and population means.

### **Conditions for Z-Test**
1.  Population Standard Deviation ($\sigma$) is **Known**.
2.  Sample size ($n$) is **$\ge$ 30**.

### **Formula**
> $$Z = \frac{\bar{x} - \mu}{\frac{\sigma}{\sqrt{n}}}$$
>
> Where:
> * $\bar{x}$ = Sample Mean
> * $\mu$ = Population Mean
> * $\sigma$ = Population Standard Deviation
> * $n$ = Sample Size

### **Types of Tests**
* **Two-Tailed:** Checking if mean is *different* ($\neq$). Rejection regions on both sides.
* **One-Tailed:** Checking if mean is *greater than* ($>$) or *less than* ($<$). Rejection region on one side.

---

## 4. Student's T-Test
Used when population parameters are unknown or sample size is small.

### **Conditions for T-Test**
1.  Population Standard Deviation ($\sigma$) is **Unknown** (we use sample std dev $s$).
2.  Sample size ($n$) can be $< 30$.

### **Formula**
> $$t = \frac{\bar{x} - \mu}{\frac{s}{\sqrt{n}}}$$
>
> Where:
> * $s$ = Sample Standard Deviation

### **Degrees of Freedom (DOF)**
Used to look up values in the T-table.
> $$DOF = n - 1$$

---

## 5. Z-Test vs. T-Test Decision Flow
How to decide which test to use:

1.  **Do you know the Population Standard Deviation ($\sigma$)?**
    * **No** $\rightarrow$ Use **T-Test**.
    * **Yes** $\rightarrow$ Check Sample Size ($n$).
        * Is $n \ge 30$?
            * **Yes** $\rightarrow$ Use **Z-Test**.
            * **No** $\rightarrow$ Use **T-Test**.

---

## 6. Type 1 and Type 2 Errors
Errors occur when the decision made via hypothesis testing does not match reality.



| Reality | Decision: Reject $H_0$ | Decision: Retain $H_0$ |
| :--- | :--- | :--- |
| **$H_0$ is True** | **Type 1 Error** (False Positive) | Correct Decision |
| **$H_0$ is False** | Correct Decision | **Type 2 Error** (False Negative) |

---

## 7. Bayes Theorem
Deals with conditional probability (Probability of Event A given Event B has occurred).

### **Formula**
> $$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$
>
> Where:
> * $P(A|B)$ = Posterior probability.
> * $P(B|A)$ = Likelihood.
> * $P(A)$ = Prior probability.
> * $P(B)$ = Marginal likelihood.

**Independent Events:** One event does not impact the other (e.g., Rolling dice).
**Dependent Events:** One event impacts the probability of the next (e.g., Drawing marbles without replacement).

---

## 8. Confidence Interval (CI) & Margin of Error
Instead of a "Point Estimate" (single value), we use an interval to estimate a population parameter with a certain confidence level.

### **Formula**
> $$\text{Confidence Interval} = \bar{x} \pm \text{Margin of Error}$$
>
> $$\text{Margin of Error (Z)} = Z_{\alpha/2} \cdot \left(\frac{\sigma}{\sqrt{n}}\right)$$

*Note: For T-test, replace $Z_{\alpha/2}$ with $t_{\alpha/2}$ and $\sigma$ with $s$.*

---

## 9. Chi-Square Test ($\chi^2$)
A non-parametric test used for **Categorical Data** (Goodness of Fit).

* **Null Hypothesis:** The data meets the expected distribution (Goodness of fit).
* **Assumptions:** Comparing **Observed** data vs. **Expected** (Theory) data.

### **Formula**
> $$\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$$
>
> Where:
> * $O_i$ = Observed Frequency
> * $E_i$ = Expected Frequency

### **Degrees of Freedom (Chi-Square)**
> $$DF = \text{Number of Categories} - 1$$

**Decision:** If calculated $\chi^2 >$ Critical Value (from table), **Reject $H_0$**.



[Image of chi square distribution curve]


---

## 10. ANOVA (Analysis of Variance)
Used to compare the means of **two or more groups**.

### **Terminology**
* **Factors:** The independent variable (e.g., Medication type).
* **Levels:** Different groups within the factor (e.g., 5mg, 10mg, 15mg).

### **Assumptions of ANOVA**
1.  **Normality:** Sampling distribution of means is normal.
2.  **No Outliers:** Outliers must be removed.
3.  **Homogeneity of Variance:** Variances of populations are equal ($\sigma_1^2 = \sigma_2^2 = ...$).
4.  **Independence:** Samples are independent and random.

### **Types of ANOVA**
1.  **One-Way:** One factor, independent levels (e.g., 3 different groups of people taking 3 different doses).
2.  **Repeated Measures:** One factor, dependent levels (e.g., The *same* group of people running on Day 1, Day 2, Day 3).
3.  **Factorial:** Two or more factors (e.g., Running Factor + Gender Factor).

---

## 11. F-Test (for ANOVA)
ANOVA uses the F-Test statistics to compare variances.

### **Hypotheses**
* **$H_0$:** $\mu_1 = \mu_2 = \mu_3 ...$ (All means are equal).
* **$H_1$:** At least one mean is different.

### **F-Statistic Formula**
> $$F = \frac{\text{Variance Between Samples}}{\text{Variance Within Samples}}$$
>
> $$F = \frac{MS_{between}}{MS_{within}}$$

**Steps for Calculation:**
1.  Calculate **Sum of Squares Between ($SS_{between}$)**.
2.  Calculate **Sum of Squares Within ($SS_{within}$)**.
3.  Calculate **Mean Squared ($MS$)** by dividing SS by Degrees of Freedom ($df$).
4.  Calculate **F-Value**.
5.  Compare F-value with Critical Value (from F-table).



[Image of F distribution curve]


> **Decision Rule:**
> If $F_{calculated} > F_{critical}$: **Reject $H_0$** (Means are significantly different).