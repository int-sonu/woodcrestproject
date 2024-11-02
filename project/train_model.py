import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('C:/ecom/ecom_project/ecom_project/project/sales_data.csv')

# Check for missing values
print("Missing values in each column:\n", data.isnull().sum())

# Visualize the distribution of the target variable
plt.figure(figsize=(10, 6))
sns.histplot(data['Amount'], bins=30, kde=True)
plt.title('Distribution of Amount')
plt.xlabel('Amount')
plt.ylabel('Frequency')
plt.show()

# Check for outliers in Amount and Quantity
plt.figure(figsize=(12, 6))
sns.boxplot(data=data[['Amount', 'Quantity']])
plt.title('Boxplot of Amount and Quantity')
plt.show()

# After addressing issues, consider re-training the model and checking RMSE
