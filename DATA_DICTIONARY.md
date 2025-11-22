# 📖 Data Dictionary

## Overview
This dataset merges CDC PLACES health outcome data with USDA Food Access metrics to identify healthcare deserts in California at the census tract level.

---

## Files

### 1. `california_health_equity.csv`
- **Records**: 9,070 (all California census tracts)
- **Use**: Statewide analysis and visualization

### 2. `santa_clara_health_equity.csv`
- **Records**: 408 (Santa Clara County only)
- **Use**: Local deep-dive analysis

### 3. `california_providers_sample.csv`
- **Records**: 200 (sample)
- **Use**: Healthcare provider locations for drive-time analysis

---

## Column Definitions

### Geographic Identifiers

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `tract_fips` | String (11 digits) | Census Tract FIPS code (unique ID) | "06085502002" |
| `location_name` | String | Human-readable tract name | "Census Tract 5020.02" |
| `county_name` | String | County name | "Santa Clara County" |

> **Note**: `tract_fips` MUST be treated as text (not number) to preserve leading zeros.

---

### Health Outcome Measures (%)
*All values are percentages (0-100) representing crude prevalence among adults*

| Column | Description | High Risk Threshold |
|--------|-------------|---------------------|
| `diabetes_prevalence` | Adults with diagnosed diabetes | > 15% |
| `heart_disease_prevalence` | Adults with coronary heart disease | > 10% |
| `stroke_prevalence` | Adults who have had a stroke | > 5% |
| `obesity_prevalence` | Adults with BMI ≥ 30 | > 35% |
| `high_bp_prevalence` | Adults with high blood pressure | > 40% |
| `smoking_prevalence` | Current smokers | > 20% |
| `annual_checkup_pct` | Had checkup in past year | < 70% (lower is worse) |
| `no_insurance_pct` | Lacking health insurance | > 15% |

**Source**: CDC PLACES 2024, Census Tract Level

---

### Food Access Metrics

| Column | Type | Description |
|--------|------|-------------|
| `LILATracts_1And10` | Integer (0 or 1) | **Low Income Low Access** designation<br>1 = Food desert<br>0 = Adequate access |
| `is_food_desert` | Boolean | Simplified flag (True/False) |
| `Urban` | Integer (0 or 1) | 1 = Urban, 0 = Rural |

**Criteria for Food Desert** (USDA):
- **Urban**: > 500 people or 33% of population > 1 mile from supermarket
- **Rural**: > 500 people or 33% of population > 10 miles from supermarket

**Source**: USDA Food Access Research Atlas 2019

---

### Calculated Risk Scores

| Column | Type | Description | Calculation |
|--------|------|-------------|-------------|
| `health_risk_score` | Float (0-100) | Composite health risk | Average of 5 key measures:<br>• Diabetes<br>• Heart disease<br>• Obesity<br>• High BP<br>• No insurance |
| `health_risk_category` | String | Simplified risk tier | Low < 10%<br>Medium 10-15%<br>High 15-20%<br>Critical > 20% |
| `combined_risk` | String | **Primary analysis metric** | See below ↓ |

---

## Combined Risk Categories (KEY METRIC!)

| Category | Criteria | Visualization Color | Count (CA) |
|----------|----------|---------------------|------------|
| **High Risk: Desert + Disease** | `health_risk_score` > 15% AND food desert | 🔴 Dark Red | 374 |
| **High Risk: Disease Only** | `health_risk_score` > 15% AND NOT food desert | 🟠 Orange | 6,013 |
| **Moderate Risk: Desert Only** | `health_risk_score` ≤ 15% AND food desert | 🟡 Yellow | 31 |
| **Low Risk** | `health_risk_score` ≤ 15% AND NOT food desert | 🟢 Light Green | 2,652 |

**Use This** for your primary Tableau map!

---

## Provider Location Data

### `california_providers_sample.csv`

| Column | Type | Description |
|--------|------|-------------|
| `npi` | String | National Provider Identifier (unique) |
| `name` | String | Provider name (individual) |
| `organization` | String | Organization name (if applicable) |
| `taxonomy` | String | Taxonomy code (207Q00000X = Family Medicine) |
| `address` | String | Street address |
| `city` | String | City |
| `postal_code` | String | ZIP code |
| `latitude` | Float | Latitude (for mapping) |
| `longitude` | Float | Longitude (for mapping) |

> **Note**: This is a sample of 200 providers. For complete coverage, see NPPES download instructions.

---

## Data Processing Notes

### Missing Values
- Health measures with no data: Left as `NaN` (appears blank in Tableau)
- Food access data: Missing values assumed to be `0` (not a food desert)

### FIPS Code Formatting
- All FIPS codes are **11 digits** with leading zeros preserved
- Format: `[2-digit state][3-digit county][6-digit tract]`
- Example: `06` (CA) + `085` (Santa Clara) + `502002` (tract)

### Data Joins
- **Primary join**: CDC PLACES ← USDA Food Access on `tract_fips`
- **Join type**: Left join (keeps all health data even if food access missing)

---

## Validation Checks

✅ **All checks passed:**
- Total California census tracts: 9,070
- Santa Clara County tracts: 408
- Food desert data coverage: 75% (6,828 / 9,070)
- No duplicate FIPS codes

---

## Citation

When using this data in reports, cite:

> Data sources: CDC PLACES Project 2024 (census tract level) and USDA Food Access Research Atlas 2019. Analysis conducted [Month Year].

---

## Questions?

Refer to original documentation:
- CDC PLACES: https://www.cdc.gov/places/
- USDA Food Atlas: https://www.ers.usda.gov/data-products/food-access-research-atlas/
