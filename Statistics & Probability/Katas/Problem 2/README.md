# Problem 2 Solution: Comparing Officer Incomes

**Problem Statement:**
A random sample of 17 police officers in Brownsville has a mean annual income of $35,800 and a standard deviation of $7,800. In Greensville, a random sample of 18 police officers has a mean annual income of $35,100 and a standard deviation of $7,375. Test the claim at $\alpha = 0.01$ that the mean annual incomes in the two cities are not the same. Assume the population variances are equal.

---

### 1. Formulate Hypotheses
We want to test if the means are **different** (not specifically higher or lower), so this is a **two-tailed test**.

* **Null Hypothesis ($H_0$):** $\mu_1 = \mu_2$ (The mean incomes are equal).
* **Alternative Hypothesis ($H_1$):** $\mu_1 \neq \mu_2$ (The mean incomes are not equal).

### 2. Identify the Test
* **Data Type:** Continuous (Means).
* **Samples:** Two Independent Samples ($n_1=17, n_2=18$).
* **Population Standard Deviation:** Unknown (we use sample $s$).
* **Assumption:** Variances are equal.

**Selected Test:** Two-Sample Pooled t-test.

### 3. Calculations

**A. Degrees of Freedom ($df$)**
$$df = n_1 + n_2 - 2$$
$$df = 17 + 18 - 2 = 33$$

**B. Pooled Variance ($s_p^2$)**
Since we assume equal variances, we calculate a weighted average of the two sample variances.

$$s_p^2 = \frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}$$

* $s_1 = 7,800 \rightarrow s_1^2 = 60,840,000$
* $s_2 = 7,375 \rightarrow s_2^2 = 54,390,625$

$$s_p^2 = \frac{(16)(60,840,000) + (17)(54,390,625)}{33}$$
$$s_p^2 \approx 57,517,594.70$$

**C. The t-Statistic**
$$t = \frac{(\bar{x}_1 - \bar{x}_2)}{\sqrt{s_p^2 \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}$$

* **Numerator (Signal):** $35,800 - 35,100 = 700$
* **Denominator (Noise/Standard Error):**
    $$\sqrt{57,517,594.70 \times \left(\frac{1}{17} + \frac{1}{18}\right)}$$
    $$\sqrt{57,517,594.70 \times 0.11438} \approx \sqrt{6,578,805} \approx 2,564.92$$

$$t = \frac{700}{2,564.92} \approx 0.273$$

### 4. Decision Rule
* **Significance Level ($\alpha$):** 0.01
* **Test Type:** Two-tailed
* **Degrees of Freedom:** 33

Using a t-table for $df \approx 30$ (closest value) and $\alpha = 0.01$ (two-tails), the **Critical Value** is approximately **2.750**.

* **Rejection Region:** Reject $H_0$ if $|t| > 2.750$.
* **Result:** Since $0.273 < 2.750$, the test statistic falls in the acceptance region.

### 5. Conclusion
**We fail to reject the Null Hypothesis.** There is not enough statistical evidence at the 1% significance level to claim that the mean annual incomes in Brownsville and Greensville are different.

---

### Note on Statistical Methods

**Statistical Methods Used:**
To investigate the disparity in police officer incomes between Brownsville and Greensville, a **Two-Sample Pooled t-test** was conducted. This method was selected because:
1.  We are comparing the means of two independent groups.
2.  The sample sizes ($n < 30$) required a t-test rather than a z-test.
3.  The assumption of equal population variances justified pooling the standard deviations.

**Findings:**
The analysis yielded a t-statistic of **0.273**, which is well below the critical threshold ($t_{crit} = 2.750$) required for statistical significance at the $\alpha = 0.01$ level. Therefore, the observed difference of $700 in annual income is likely due to random sampling variation rather than a genuine economic difference between the two cities.