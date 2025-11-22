# 🏥 Medical Desert & Health Equity Map - California

> **"Your zip code determines your lifespan."**  
> This project visualizes healthcare access disparities across California, with a focus on Santa Clara County.

[![Tableau Public](https://img.shields.io/badge/Tableau-Public-blue)](https://public.tableau.com)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📊 Project Overview

This data analysis project explores the intersection of **health outcomes** and **food access** to identify "medical deserts" - areas with poor health outcomes and limited access to healthy food options.

**Key Findings:**
- 🎯 *[Your findings will go here after analysis]*
- 📍 *[Santa Clara County specific insights]*
- 🚨 *[High-risk areas identified]*

---

## 🗺️ Interactive Dashboard

> [!IMPORTANT]
> 🔗 **[View the Interactive Tableau Dashboard →](#)** *(Link will be added after publishing)*

![Dashboard Preview](visualizations/dashboard_preview.png)
*Preview of the split-screen correlation map showing diabetes prevalence vs. food access*

---

## 📁 Data Sources

### Primary Data
| Source | Dataset | Granularity | Year |
|--------|---------|-------------|------|
| **CDC** | [PLACES 2024](https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2024-/cwsq-ngmh) | Census Tract | 2024 |
| **USDA** | [Food Access Research Atlas](https://www.ers.usda.gov/data-products/food-access-research-atlas/) | Census Tract | 2019 |

### Health Measures Analyzed
- Diabetes prevalence
- Heart disease prevalence
- Obesity rates
- High blood pressure
- Lack of health insurance

### Food Access Metrics
- **LILA Tracts**: Low Income Low Access designation
- **Distance thresholds**: 1 mile (urban) / 10 miles (rural)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Tableau Public (free)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/medical-desert-california.git
cd medical-desert-california

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
# Step 1: Download data
python scripts/download_data.py

# Step 2: Process and merge data
python scripts/process_data.py

# Step 3: Open in Tableau Public
# Load data/processed/california_health_equity.csv
```

---

## 🔬 Methodology

### Healthcare Desert Risk Score

Our composite risk metric combines:

1. **Health Outcome Score** (0-100)
   - Average of diabetes, heart disease, obesity, hypertension, and uninsured rates
   
2. **Food Access Flag**
   - USDA-defined Low Income Low Access (LILA) designation

3. **Combined Risk Categories**
   - 🔴 **High Risk: Desert + Disease** - Poor health + food desert
   - 🟠 **High Risk: Disease Only** - Poor health, adequate food access
   - 🟡 **Moderate Risk: Desert Only** - Good health, but food desert
   - 🟢 **Low Risk** - Good health + adequate access

### FIPS Code Joining
All datasets joined on 11-digit Census Tract FIPS codes with proper zero-padding to ensure accurate geographic matching.

---

## 📂 Project Structure

```
medical-desert-california/
├── data/
│   ├── raw/                          # Original downloads (gitignored)
│   └── processed/                    # Clean CSVs for Tableau
│       ├── california_health_equity.csv
│       └── santa_clara_health_equity.csv
├── scripts/
│   ├── download_data.py              # Automated data fetcher
│   └── process_data.py               # ETL pipeline
├── notebooks/
│   └── exploratory_analysis.ipynb    # Jupyter analysis
├── visualizations/                   # Screenshots & exports
├── README.md
└── requirements.txt
```

---

## 📈 Key Insights

> [!NOTE]
> *This section will be populated after completing the Tableau visualization*

### Santa Clara County Highlights
- Total census tracts analyzed: *[TBD]*
- Food deserts identified: *[TBD]*
- High-risk areas: *[TBD]*

---

## 🛠️ Technologies Used

- **Python** - Data processing and analysis
  - pandas, numpy - Data manipulation
  - requests - API calls
  - openpyxl - Excel file handling
- **Tableau Public** - Interactive visualization
- **CDC PLACES API** - Health outcome data
- **USDA Data** - Food access metrics

---

## 📝 Future Enhancements

- [ ] Add drive-time analysis to nearest hospital/clinic
- [ ] Incorporate pharmacy location data
- [ ] Time-series analysis of health trends
- [ ] Predictive modeling for intervention targeting

---

## 🤝 Contributing

This is a portfolio project, but I welcome feedback and suggestions!  
Feel free to open an issue or reach out on [LinkedIn](#).

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👤 Author

**[Your Name]**  
Data Analyst | Healthcare Analytics Enthusiast

- 📧 Email: your.email@example.com
- 💼 LinkedIn: [your-profile](#)
- 🌐 Portfolio: [your-website](#)

---

## 🙏 Acknowledgments

- CDC PLACES team for maintaining exceptional public health data
- USDA Economic Research Service for food access research
- Tableau Public for free data visualization platform

---

<div align="center">
<sub>Built with ❤️ for improving healthcare equity</sub>
</div>
