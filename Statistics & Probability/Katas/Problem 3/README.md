# Problem 3 Solution: Drug Effectiveness Test

**Problem Statement:**
A commonly prescribed drug for relieving nervous tension is believed to be only 60% effective. Experimental results with a new drug administered to a random sample of 100 adults who were suffering from nervous tension show that 70 received relief. Is this sufficient evidence to conclude that the new drug is superior to the one commonly prescribed? Use a 0.05 level of significance.

---

### 1. Formulate Hypotheses
We are testing a claim about a population proportion ($p$). Specifically, we want to know if the new drug's effectiveness is **greater than** the historical standard of 60%.

* **Null Hypothesis ($H_0$):** $p \le 0.60$ (The new drug is no better than the old one).
* **Alternative Hypothesis ($H_1$):** $p > 0.60$ (The new drug is superior).

*Note: Since the claim uses "superior," this is a **One-Tailed (Right)** test.*

### 2. Identify the Test
* **Data Type:** Categorical/Proportions (Success/Failure).
* **Sample Size:** $n = 100$ (Large sample, $n \ge 30$).
* **Comparison:** One sample proportion against a known population standard.

**Selected Test:** One-Sample Z-Test for Proportions.

### 3. Calculations

**A. Parameters**
* Sample Size ($n$): 100
* Number of Successes ($x$): 70
* Sample Proportion ($\hat{p}$): $70 / 100 = 0.70$
* Hypothesized Proportion ($p_0$): $0.60$

**B. Standard Error**
The standard error depends on the hypothesized proportion ($p_0$).

$$SE = \sqrt{\frac{p_0(1 - p_0)}{n}}$$
$$SE = \sqrt{\frac{0.60 \times 0.40}{100}} = \sqrt{\frac{0.24}{100}} = \sqrt{0.0024} \approx 0.04899$$

**C. The Z-Statistic**
$$z = \frac{\hat{p} - p_0}{SE}$$
$$z = \frac{0.70 - 0.60}{0.04899} = \frac{0.10}{0.04899} \approx 2.041$$

### 4. Decision Rule
* **Significance Level ($\alpha$):** 0.05
* **Test Type:** One-Tailed (Right)

Using a Standard Normal (Z) Table, the critical value for the top 5% of the curve is **1.645**.

* **Rejection Region:** Reject $H_0$ if $z > 1.645$.
* **Result:** Since $2.041 > 1.645$, the test statistic falls in the rejection region.

### 5. Conclusion
**We reject the Null Hypothesis.** There is sufficient statistical evidence at the 5% significance level to conclude that the new drug is superior to the commonly prescribed one.

---

### Note on Statistical Methodology

**Statistical Methods Used:**
To evaluate the efficacy of the new nervous tension drug, a **One-Sample Z-Test for Proportions** was conducted. This method was appropriate because the data involved binary outcomes (relief vs. no relief) and the sample size ($n=100$) was sufficiently large to approximate a normal distribution.

**Findings:**
The test produced a z-statistic of **2.04**, which exceeds the critical value of 1.645 required for a 0.05 significance level. This indicates that the observed 70% relief rate is statistically significantly higher than the historical baseline of 60%. Therefore, we can confidently claim the new drug offers superior performance.