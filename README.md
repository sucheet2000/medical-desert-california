# 🏥 Medical Desert & Health Equity Map - California

> **"Your zip code determines your lifespan."**

An analysis of healthcare access disparities across California, examining the intersection of health outcomes and food access at the census tract level.

[![Tableau Public](https://img.shields.io/badge/Tableau-Public-blue)](https://public.tableau.com)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📊 Project Overview

This project identifies "medical deserts" - geographic areas experiencing both poor health outcomes and limited access to healthy food. Using census tract-level data, I analyzed 9,070 California communities to uncover patterns in health equity.

### Key Findings

- **374 high-risk census tracts** combine poor health outcomes (diabetes >15%) with food desert status
- **6,013 tracts** show high disease prevalence despite adequate food access
- **Santa Clara County**: 408 census tracts analyzed with localized risk assessment
- **405 food deserts** identified statewide using USDA criteria

---

## 🗺️ Interactive Dashboard

> [!IMPORTANT]
> 🔗 **[View Interactive Tableau Dashboard →](https://public.tableau.com/app/profile/sai.sucheet.boppana/viz/CaliforniaMedicalDeserts-HealthEquityAnalysis/Sheet1)**

*Interactive map showing 374 high-risk medical deserts across California's 9,070 census tracts*

---

## 📁 Data Sources

| Source | Dataset | Granularity | Records |
|--------|---------|-------------|---------|
| **CDC PLACES** | [2024 Release](https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2024-/cwsq-ngmh) | Census Tract | 362,792 CA records |
| **USDA ERS** | [Food Access Research Atlas](https://www.ers.usda.gov/data-products/food-access-research-atlas/) | Census Tract | 8,024 CA records |
| **NPPES** | NPI Registry (sample) | Provider Location | 200 providers |

### Health Metrics
- Diabetes prevalence
- Coronary heart disease
- Obesity rates
- High blood pressure
- Lack of health insurance

### Food Access Definition
**USDA Low Income Low Access (LILA) Criteria:**
- **Urban**: >500 people or 33% of population >1 mile from supermarket
- **Rural**: >500 people or 33% of population >10 miles from supermarket

---

## 🔬 Methodology

### Composite Risk Score

I developed a healthcare desert risk score combining:

1. **Health Risk Score** (0-100 scale)
   - Calculated as the mean of 5 key health indicators
   - Threshold: >15% indicates high risk

2. **Food Access Status**
   - Binary classification using USDA LILA designation

3. **Combined Risk Categories**
   | Category | Criteria | Count |
   |----------|----------|-------|
   | 🔴 High Risk: Desert + Disease | Health score >15% AND food desert | 374 |
   | 🟠 High Risk: Disease Only | Health score >15%, NOT food desert | 6,013 |
   | 🟡 Moderate Risk: Desert Only | Health score ≤15% AND food desert | 31 |
   | 🟢 Low Risk | Health score ≤15%, NOT food desert | 2,652 |

### Data Processing
- **Join method**: Left join on 11-digit Census Tract FIPS codes
- **Missing data**: Food access nulls assumed non-desert status
- **Validation**: Zero duplicate FIPS codes, 75% food access coverage

---

## 🚀 Reproducibility

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/medical-desert-california.git
cd medical-desert-california

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Pipeline

```bash
# Download datasets (CDC PLACES, USDA Food Access, NPPES)
python scripts/download_data.py

# Process and merge data
python scripts/process_data.py

# Output: data/processed/california_health_equity.csv (ready for Tableau)
```

---

## 📂 Repository Structure

```
medical-desert-california/
├── data/
│   ├── raw/                    # Source data (gitignored, 800+ MB)
│   └── processed/              # Analysis-ready CSVs
│       ├── california_health_equity.csv      (9,070 tracts)
│       └── santa_clara_health_equity.csv     (408 tracts)
├── scripts/
│   ├── download_data.py        # Automated data fetching
│   └── process_data.py         # ETL pipeline with risk scoring
├── DATA_DICTIONARY.md          # Complete column reference
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 🛠️ Technical Stack

- **Python 3.13** - Data engineering
  - `pandas` - Data manipulation and merging
  - `requests` - API integration
  - `openpyxl` - Excel file processing
- **Tableau Public** - Interactive visualization
- **Git** - Version control

---

## 📊 Sample Insights

### Statewide Analysis
- **9,070 census tracts** across California
- **4.1% of tracts** are high-risk medical deserts
- Clustering observed in Central Valley and rural counties

### Santa Clara County
- **408 census tracts** analyzed
- Local risk distribution available in `santa_clara_health_equity.csv`
- Suitable for targeted public health interventions

---

## 📝 Next Steps

- [ ] Publish interactive Tableau dashboard
- [ ] Add drive-time analysis to healthcare facilities
- [ ] Incorporate temporal trends (2015-2024 comparison)
- [ ] Develop predictive model for intervention prioritization

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👤 Contact

**Sucheet Boppana**  
Data Analyst | Healthcare Analytics

- 💼 [LinkedIn](https://linkedin.com/in/yourprofile)
- 📧 your.email@example.com
- 🌐 [Portfolio](https://yourportfolio.com)

---

## 🙏 Acknowledgments

Data sources:
- CDC PLACES Project (2024)
- USDA Economic Research Service
- CMS National Plan and Provider Enumeration System (NPPES)

---

<div align="center">
<sub>Analyzing health equity through data</sub>
</div>
