# 🚲 VCub Anomaly Detection

This project aims to automatically detect anomalies in usage data for VCub stations, Bordeaux Métropole's bike-sharing service, using historical data collected via an open API.

---

## 🧠 Objectives

* Collect minute-by-minute occupancy data from VCub stations via the Bordeaux Métropole API.
* Analyze daily and weekly occupancy trends.
* Use time series models (Prophet) to forecast expected occupancy.
* Identify anomalies where observed data falls outside the forecast confidence intervals.
* Visualize data, anomalies, and time series components (trend, weekly, daily).

---

## 📂 Project Structure

```
.
├── data/                  # Directory storing collected JSON data
├── main.py                # Main analysis and visualization script
├── pull_data.py           # Data retrieval script from the API
├── pull_data.sh           # Shell script to run pull_data.py
├── plan.md                # Design and experimentation notes
├── graph2022.pdf          # Visualization of results and anomalies
├── components.pdf         # Prophet model components
├── README.md              # Project overview
└── key.txt                # API key (not included)
```

---

## 🏗️ Workflow

### 1. Data Collection

Run:

```bash
python pull_data.py <station_id>
```

By default, `pull_data.sh` runs with station `106`. Data includes:

* Available bikes (`nbvelos`)
* Free slots (`nbplaces`)
* Station status (`etat`)
* Timestamp (`mdate`)

---

### 2. Analysis & Modeling

`main.py`:

* Computes occupancy rate: `occupancy = nbvelos / (nbvelos + nbplaces)`
* Aggregates data hourly
* Trains a Prophet model to forecast occupancy
* Flags anomalies when observations fall outside the forecast confidence intervals

---

### 3. Visualization

Generates:

* `graph2022.pdf`: Observations, anomalies, disconnections, and Prophet forecast
* `components.pdf`: Model components (trend, daily and weekly seasonality)

---

## 📊 Example Output

![graph2022.pdf](graph2022.pdf)

---

## 🔍 Future Improvements

* Anomaly detection by day type (holiday, weekday, weekend)
* Interactive dashboard (Dash, Streamlit)
* Real-time integration (streaming)

---

## 🔑 Dependencies

* Python ≥ 3.7
* `pandas`, `matplotlib`, `numpy`
* [`prophet`](https://facebook.github.io/prophet/)

Install with:

```bash
pip install pandas matplotlib numpy prophet
```

---

## 📬 Data Source

Data is retrieved from:
👉 [https://data.bordeaux-metropole.fr](https://data.bordeaux-metropole.fr)

Place your API key in `key.txt`.

---

## 👨‍💻 Authors

Angel Hippolyte
Charles Martin
