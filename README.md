# ☕ Roast & Grind | Customer Segmentation & Retention Analytics

An end-to-end customer segmentation project for a simulated specialty coffee and home-brewing e-commerce store.

This project identifies actionable customer groups using RFM analysis and unsupervised machine learning, then translates the results into practical retention, cross-sell, and win-back strategies.

---

## Business Problem

Online coffee and home-brewing stores serve different types of customers, including frequent premium-bean buyers, occasional shoppers, equipment-focused customers, beginners, and inactive high-value customers. A single marketing message is unlikely to work effectively for all customer groups.

This project answers the following business question:

> Which customer groups should the store target with retention, premium-bean upselling, beginner brewing kits, and win-back campaigns?

---

## Project Objective

- Clean and prepare transaction-level e-commerce data.
- Create customer-level RFM and behavioral features.
- Segment customers using unsupervised machine learning.
- Compare multiple clustering models and validate the results.
- Profile customer segments and assign business-friendly persona names.
- Recommend targeted marketing actions for each segment.
- Present the results through an interactive Streamlit dashboard.

---

## Project Workflow

```text
Raw transaction data
        ↓
Data quality and cleaning
        ↓
Customer RFM feature engineering
        ↓
Customer segmentation and clustering
        ↓
Segment analysis and business insights
        ↓
Interactive Streamlit dashboard
```

---

## Dataset

The dataset is **synthetic/simulated** for portfolio demonstration purposes. It represents transaction-level orders from a fictional specialty coffee and home-brewing e-commerce store.

The raw dataset includes:

| Column | Description |
|---|---|
| InvoiceNo | Unique order/invoice identifier |
| CustomerID | Unique customer identifier |
| InvoiceDate | Date and time of the transaction |
| ProductName | Name of the purchased product |
| Category | Product category |
| Quantity | Number of units purchased |
| UnitPrice | Price per unit |
| TotalAmount | Total transaction value |

Negative quantities are treated as returns and are handled separately from completed purchases.

---

## Project Structure

```text
roast-and-grind/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   │   └── roast_and_grind_transactions.csv
│   └── processed/
│       ├── cleaned_transactions.csv
│       ├── customer_features.csv
│       ├── customer_features_scaled.csv
│       └── customer_segments_final.csv
│
├── notebooks/
│   ├── 01_data_quality_and_cleaning.ipynb
│   ├── 02_customer_rfm_feature_engineering.ipynb
│   ├── 03_customer_segmentation_clustering.ipynb
│   └── 04_exploratory_data_analysis_and_business_insights.ipynb
│
├── outputs/
│   ├── figures/
│   └── tables/
│
└── .streamlit/
    └── config.toml
```

---

## Notebooks

### 01. Data Quality and Cleaning

This notebook prepares the raw transaction dataset for analysis.

- Loads and inspects the raw data.
- Identifies missing values, duplicates, and invalid records.
- Converts `InvoiceDate` to datetime format.
- Separates returns from completed purchases.
- Removes invalid prices and quantities.
- Creates a cleaned transaction dataset for RFM analysis.

**Output:** `cleaned_transactions.csv`

### 02. Customer RFM Feature Engineering

This notebook converts transaction-level data into one row per customer.

RFM features:

| Feature | Definition |
|---|---|
| Recency | Days since the customer’s most recent purchase |
| Frequency | Number of unique completed orders |
| Monetary | Total amount spent by the customer |

Additional behavioral features:

- Average order value
- Customer tenure
- Coffee beans spend share
- Brew gear spend share
- Accessories spend share
- Scaled features for clustering

**Output:** `customer_features.csv` and `customer_features_scaled.csv`

### 03. Customer Segmentation Clustering

This notebook applies and compares unsupervised clustering models.

Models used:

- K-Means Clustering
- Agglomerative Hierarchical Clustering
- Gaussian Mixture Model

Model validation methods:

- Elbow method
- Silhouette score
- Davies-Bouldin index
- Cluster size balance
- PCA visualization
- Business interpretability

The final clustering model assigns each customer to a segment. Cluster labels are then profiled and renamed into meaningful customer personas.

**Output:** `customer_segments_final.csv`

### 04. Exploratory Data Analysis and Business Insights

This notebook analyzes the final segmented customer dataset.

It includes:

- Segment size and revenue contribution.
- RFM profile comparison across segments.
- Product-category preferences by segment.
- Identification of high-value and at-risk customers.
- Customer personas.
- Marketing recommendations for each segment.

---

## Customer Segments

The final segment names should be assigned after reviewing the actual cluster profiles. Possible customer personas include:

| Segment | Typical Behavior | Recommended Action |
|---|---|---|
| Specialty Coffee Champions | Recent, frequent, high-value customers | Loyalty rewards and early access to premium beans |
| Home-Brew Beginners | New or low-frequency customers | Starter kits, brewing guides, and product bundles |
| Equipment-First Buyers | Customers focused on brewing equipment | Cross-sell coffee beans and maintenance accessories |
| Occasional Value Shoppers | Low-frequency, price-sensitive customers | Seasonal offers and email nurture campaigns |
| Lapsed Premium Buyers | High historical spend but low recency | Personalized win-back campaigns |

---

## Dashboard

The Streamlit dashboard allows users to explore the final customer segments interactively.

### Dashboard Features

- Business overview KPIs
- Customer segment distribution
- Revenue contribution by segment
- RFM customer behavior analysis
- Product-category preference analysis
- Customer segment lookup
- Marketing recommendations
- Downloadable segmented customer data

### Run the Dashboard

```bash
streamlit run app.py
```

---

## Tools and Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter Notebook
- Git
- GitHub

---

## How to Run the Project

1. Clone the repository:

```bash
git clone [https://github.com/your-username/roast-and-grind-customer-segmentation.git](https://github.com/your-username/roast-and-grind-customer-segmentation.git)
cd roast-and-grind-customer-segmentation
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the notebooks in order:

```bash
jupyter notebook
```

Run:

```text
01_data_quality_and_cleaning.ipynb
02_customer_rfm_feature_engineering.ipynb
03_customer_segmentation_clustering.ipynb
04_exploratory_data_analysis_and_business_insights.ipynb
```

4. Launch the Streamlit dashboard:

```bash
streamlit run app.py
```

---

## Key Results

After running the notebooks, this section can be updated with your actual results, such as:

- Total number of customers analyzed
- Number of customer segments identified
- Revenue contribution of the highest-value segment
- Percentage of repeat customers
- Number of high-value customers at risk of churn

Example:

```text
- Analyzed 3,000 customers and 22,000 transactions.
- Identified four actionable customer segments.
- High-value customers contributed the largest share of total revenue.
- A group of previously high-spending customers showed high recency and became a priority for win-back campaigns.
```

---

## Business Impact

This project helps the business move beyond generic marketing by identifying customer groups with different needs and value levels.

Potential actions include:

- Retaining high-value customers through loyalty programs.
- Converting beginners into repeat coffee-bean buyers.
- Cross-selling coffee beans to equipment-focused customers.
- Recovering inactive high-value customers through targeted win-back offers.
- Reducing unnecessary discounts for customers who do not respond to promotions.

---

## Future Improvements

- Add customer demographic and engagement data.
- Incorporate product-level recommendations.
- Use customer lifetime value (CLV) modeling.
- Test additional clustering algorithms.
- Deploy the dashboard to Streamlit Cloud.
- Add automated data-validation tests.
- Build a Power BI version of the dashboard.

---

## Limitations

- The dataset is synthetic and does not represent real customer behavior.
- Customer segments are based on historical transactions and may change over time.
- Clustering results depend on feature selection, scaling, and the chosen number of clusters.
- Marketing recommendations should be validated through A/B testing before full implementation.

---

## Author

**Your Name**  
Data Analytics | Python | SQL | Machine Learning | Dashboarding

- GitHub: https://github.com/your-username
- LinkedIn: https://www.linkedin.com/in/your-linkedin-profile
