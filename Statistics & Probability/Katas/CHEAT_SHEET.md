# Statistical Hypothesis Testing Formula Cheat Sheet

This guide covers the most common scenarios for hypothesis testing involving Means (Continuous Data) and Proportions (Categorical Data).

---

## 1. Single Population Tests

Use these when comparing a single sample group against a known standard or historical value.

### A. Testing a Mean ($\mu$)
**Decision:** Do we know the Population Standard Deviation ($\sigma$)?

#### Scenario 1: $\sigma$ is Known (or $n \ge 30$)
* **Test:** One-Sample Z-Test
* **Formula:**
    $$z = \frac{\bar{x} - \mu}{\sigma / \sqrt{n}}$$

#### Scenario 2: $\sigma$ is Unknown (and $n < 30$)
* **Test:** One-Sample t-test
* **Formula:**
    $$t = \frac{\bar{x} - \mu}{s / \sqrt{n}}$$
* **Degrees of Freedom ($df$):** $n - 1$

---

### B. Testing a Proportion ($p$)
Use this for percentages or success/failure counts.

* **Test:** One-Sample Z-Test for Proportions
* **Formula:**
    $$z = \frac{\hat{p} - p_0}{\sqrt{\frac{p_0(1-p_0)}{n}}}$$
    * $\hat{p}$: Sample Proportion ($x/n$)
    * $p_0$: Hypothesized Proportion

---

## 2. Two Population Tests (Comparing Groups)

Use these when comparing two independent groups (e.g., Group A vs. Group B).

### A. Comparing Two Means ($\mu_1 - \mu_2$)
**Decision:** Do we know the Population Standard Deviations? If not, are variances equal?

#### Scenario 1: Population SDs ($\sigma_1, \sigma_2$) Known
* **Test:** Two-Sample Z-Test
* **Formula:**
    $$z = \frac{(\bar{x}_1 - \bar{x}_2)}{\sqrt{ \frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2} }}$$

#### Scenario 2: Population SDs Unknown (Assume Equal Variances)
* **Test:** Two-Sample Pooled t-test
* **Requirements:** $s_1 \approx s_2$ or problem states "equal variances."
* **Pooled Variance ($s_p^2$):**
    $$s_p^2 = \frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}$$
* **Test Statistic:**
    $$t = \frac{\bar{x}_1 - \bar{x}_2}{ \sqrt{ s_p^2 \left( \frac{1}{n_1} + \frac{1}{n_2} \right) } }$$
* **Degrees of Freedom ($df$):** $n_1 + n_2 - 2$

#### Scenario 3: Population SDs Unknown (Assume Unequal Variances)
* **Test:** Welch’s t-test (Unpooled)
* **Requirements:** $s_1$ and $s_2$ are significantly different.
* **Formula:**
    $$t = \frac{\bar{x}_1 - \bar{x}_2}{ \sqrt{ \frac{s_1^2}{n_1} + \frac{s_2^2}{n_2} } }$$
* **Degrees of Freedom ($df$):** Calculated via Satterthwaite formula (or estimated as $\text{min}(n_1-1, n_2-1)$ for hand calculations).

---

### B. Comparing Two Proportions ($p_1 - p_2$)
Use this to check if the success rate differs between two groups.

* **Test:** Two-Proportions Z-Test
* **Step 1: Calculate Pooled Proportion ($\bar{p}$):**
    $$\bar{p} = \frac{x_1 + x_2}{n_1 + n_2}$$
* **Step 2: Calculate Z-Statistic:**
    $$z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{ \bar{p}(1 - \bar{p}) \left( \frac{1}{n_1} + \frac{1}{n_2} \right) }}$$

---

## Quick Reference: Critical Values (Z-Table)

For Z-tests (Proportions or Large Sample Means), you don't need degrees of freedom.

| Significance Level ($\alpha$) | One-Tailed | Two-Tailed |
| :--- | :--- | :--- |
| **0.05 (5%)** | 1.645 | 1.960 |
| **0.01 (1%)** | 2.330 | 2.575 |
| **0.10 (10%)** | 1.280 | 1.645 |