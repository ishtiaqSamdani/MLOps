# Problem 1: Sales Training Hypothesis Test

## Problem Statement

After a new sales training is given to employees the average sale goes up to $150 (a sample of 25 employees was examined) with a standard deviation of $12. Before the training, the average sale was $100. Check if the training helped at 
α = 0.05.
Write a note describing the statistical methods/ tests used.


---

## Solution Steps

### 1. State the Hypotheses
Since we are checking if sales **went up** (increased), this is a **One-Tailed (Right-Tailed) Test**.

* **Null Hypothesis ($H_0$):** The training did not increase sales.
    $$H_0: \mu \le 100$$
* **Alternate Hypothesis ($H_1$):** The training increased sales.
    $$H_1: \mu > 100$$

### 2. Determine the Statistical Test
* **Population Standard Deviation ($\sigma$):** Unknown (we only have sample $s$).
* **Sample Size ($n$):** 25 (which is $< 30$).
* **Conclusion:** Use the **One-Sample T-Test**.

### 3. Calculate Degrees of Freedom (DOF)
$$DOF = n - 1$$
$$DOF = 25 - 1 = 24$$

### 4. Find the Critical Value
Using the T-Distribution Table for **$df=24$** and **$\alpha=0.05$** (One-Tail):

> **$t_{critical} \approx 1.711$**

*Decision Rule: If $t_{calculated} > 1.711$, we Reject $H_0$.*

### 5. Calculate the T-Statistic
$$t = \frac{\bar{x} - \mu}{\frac{s}{\sqrt{n}}}$$

**Given:**
* $\bar{x} = 150$
* $\mu = 100$
* $s = 12$
* $n = 25$

**Calculation:**
$$t = \frac{150 - 100}{\frac{12}{\sqrt{25}}}$$

$$t = \frac{50}{\frac{12}{5}}$$

$$t = \frac{50}{2.4}$$

$$t \approx 20.83$$

### 6. Conclusion
Compare the calculated statistics to the critical value:
$$20.83 > 1.711$$

**Result:** Since the calculated t-score falls significantly into the rejection region, we **Reject the Null Hypothesis**.

**Interpretation:** There is strong statistical evidence (at 95% confidence) to conclude that the sales training **helped** increase the average sales.

---


### Why T-Test instead of Z-Test?
We selected the **Student's T-test** because the problem presents two specific constraints:
1.  **Unknown $\sigma$:** We were provided the standard deviation of the *sample* ($s=12$), not the population.
2.  **Small Sample Size:** The sample size ($n=25$) is less than 30. When $n < 30$, the Central Limit Theorem cannot be fully applied to assume a perfect Normal distribution, so the T-distribution (which has fatter tails) is used to account for higher uncertainty.

### Why One-Tailed Test?
The problem specifically asked if the training **"helped"** (implies increase). This is a directional inquiry ($\mu > 100$). If the problem asked if the training simply "changed" the sales (up or down), we would have used a Two-Tailed test.