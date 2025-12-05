
## 1. Handling Missing Values
**File:** `1.0-Handling-Missing-values.ipynb`

### The Concept
Real-world data often has gaps (`NaN` or `Null`). Understanding the *mechanism* of missingness is crucial:
* **MCAR (Missing Completely at Random):** No pattern; missingness is random (e.g., lost survey pages).
* **MAR (Missing at Random):** Missingness is related to other observed data (e.g., men might skip the "age" question more than women).
* **MNAR (Missing Not at Random):** Missingness is related to the missing value itself (e.g., high-debt individuals skipping "debt" questions).

### The Code
**1. Detection & Deletion**
```python
# Check for nulls
df.isnull().sum()

# Drop rows with nulls (Use only if dataset is large and missingness is low)
df.dropna() 


**2. Imputation (Filling Gaps)**

  * **Numerical Data:**

      * **Mean:** Use for normally distributed data.
      * **Median:** Use for skewed data or data with outliers (robust).

    <!-- end list -->

    ```python
    df['Age_mean'] = df['age'].fillna(df['age'].mean())
    df['age_median'] = df['age'].fillna(df['age'].median())
    ```

  * **Categorical Data:**

      * **Mode:** Use the most frequent value.

    <!-- end list -->

    ```python
    # Example: Filling missing 'Embarked' port
    mode_value = df['embarked'].mode()[0]
    df['embarked_mode'] = df['embarked'].fillna(mode_value)
    ```

**⚠️ Risk:** Filling too many missing values with the **Mode** can create a "fake majority," biasing the model.

-----

## 2\. Handling Imbalanced Datasets

**File:** `2.0-Handling-Imbalance-Dataset.ipynb`

### The Concept

When one class (Majority) vastly outnumbers the other (Minority)—e.g., Fraud Detection (99% vs 1%)—models become "lazy" and predict the majority class every time to achieve high accuracy but fail to detect the minority class.

### The Code

**1. Upsampling (Over-sampling)**
Duplicating minority records to match the majority count.

```python
from sklearn.utils import resample

df_minority_upsampled = resample(
    df_minority, 
    replace=True,    # Duplicates data
    n_samples=len(df_majority), 
    random_state=42
)
```

**2. Downsampling (Under-sampling)**
Deleting majority records to match the minority count.

```python
df_majority_downsampled = resample(
    df_majority, 
    replace=False, 
    n_samples=len(df_minority), 
    random_state=42
)
```

**⚠️ Risk:** Simple Upsampling leads to **Overfitting** because the model memorizes the duplicated points instead of learning general traits.

-----

## 3\. SMOTE (Synthetic Minority Over-sampling Technique)

**File:** `3.0-SMOTE.ipynb`

### The Concept

Solves the overfitting problem of upsampling. Instead of duplicating, it creates **new synthetic points**.

1.  Pick a minority point.
2.  Find its nearest neighbors (KNN).
3.  Draw a line between them and create a new point along that line.

### The Code

```python
from imblearn.over_sampling import SMOTE

oversample = SMOTE()
# Generates new synthetic rows
X_resampled, y_resampled = oversample.fit_resample(X, y)
```

**⚠️ Risk:** If the minority points are **Outliers** (noise), SMOTE will create a "bridge" of noise, amplifying the problem. Handle outliers first\!

-----

## 4\. Handling Outliers

**File:** `4.0-Handling-Outliers.ipynb`

### The Concept

Outliers are data points significantly different from others. They skew statistics (Mean) and confuse models. We detect them using the **IQR (Interquartile Range)** method.

### The Code

```python
import numpy as np

# 1. Calculate Percentiles
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)

# 2. Calculate IQR
IQR = Q3 - Q1

# 3. Define Fences (Any point outside these is an outlier)
lower_fence = Q1 - (1.5 * IQR)
higher_fence = Q3 + (1.5 * IQR)
```

*Note: Increasing the multiplier from `1.5` to `3` identifies only "extreme" outliers.*

-----

## 5\. Nominal vs. One Hot Encoding (OHE)

**File:** `5.0-Nominal-or-OHE.ipynb`

### The Concept

**Nominal Data:** Categories with **no intrinsic order** (e.g., Colors: Red, Blue, Green).
Assigning numbers (Red=1, Blue=2) confuses the model into thinking Blue \> Red.

**Solution:** One Hot Encoding creates a binary column for each category.

  * Red -\> `[1, 0, 0]`
  * Blue -\> `[0, 1, 0]`

### The Code

```python
# Using Pandas (Easiest way)
pd.get_dummies(df, columns=['color'])

# Using Sklearn
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
encoded = encoder.fit_transform(df[['color']]).toarray()
```

**⚠️ Risk:** **Curse of Dimensionality**. If you have a column with 50 categories (e.g., Cities), OHE adds 50 new columns, making the dataset massive and slow.

-----

## 6\. Label and Ordinal Encoding

**File:** `7.0-Label-and-Ordinal.ipynb`

### The Concept

**A. Label Encoding:** Assigns unique integers arbitrarily (Apple=1, Banana=2).

  * **Use for:** Target Variable (`y`) only. Do not use for features (`X`) unless there is an order.

**B. Ordinal Encoding:** Assigns integers based on **rank/order**.

  * **Use for:** Ordered features (e.g., Education: High School=1 \< Bachelor's=2 \< Master's=3). Preserves the relationship for the model.

### The Code

```python
from sklearn.preprocessing import OrdinalEncoder

# Define order manually to ensure correctness
categories = [['Small', 'Medium', 'Large']]
encoder = OrdinalEncoder(categories=categories)

df['size_encoded'] = encoder.fit_transform(df[['size']])
```

-----

## 7\. Target Guided Ordinal Encoding

**File:** `8.0-Target-Guided-Ordinal-Encoding.ipynb`

### The Concept

Used when a categorical variable has **many labels** (high cardinality, e.g., 50 Cities) and OHE is not feasible.
We replace the category name with the **Mean of the Target Variable** for that category.

  * *Example:* Replace "London" with the average house price in London.

### The Code

```python
# 1. Calculate mean of target ('price') for each category ('city')
mean_price = df.groupby('city')['price'].mean().to_dict()

# 2. Map the means to the original column
df['city_encoded'] = df['city'].map(mean_price)
```

**⚠️ Risk:** Since it relies on the Mean, it is sensitive to **Outliers**. One multi-million dollar mansion in a small city can skew the encoding for the entire city.

```
```