# MacroGauge — Zambia Macro Dashboard

MacroGauge is a dynamic, Streamlit-based macro intelligence system for Zambia.
It provides **real-time fiscal, monetary and commodity insights**, delivering interactive visualizations, trend analyses and key macroeconomic metrics with dynamic realtime insight.

---

## Features

* **FX Overview** — Track USD/ZMW exchange rate trends with commentary.
* **Inflation Analysis** — Monthly and historical inflation trends.
* **Fiscal Dashboard** — T-Bill and government bond metrics, fiscal stress indicators.
* **Commodities Dashboard** — Key commodities including copper, maize, and oil.
* **Yield Curve Analysis** — Latest yield curves, annual averages, and curve shape commentary.
* **Macro Brief** — Generate monthly snapshot briefs for internal use or external publication.
* **Macro Risk Monitor** — Recession probability gauge and policy stance classification.
* **Dynamic Updates** — All metrics and charts update automatically with new data.

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/macrogauge.git
cd macrogauge
```

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## Running the App

Run the Streamlit app locally:

```bash
streamlit run app.py
```

* Navigate through the pages using the sidebar:

  * **Macro Brief** — Monthly snapshot and exportable brief.
  * **Macro Risk Monitor** — Market-implied recession risk and policy stance.
  * **Fiscal Dashboard** — Treasury and fiscal metrics.
  * **Commodities Dashboard** — Key commodity trends.

---

## Macro Brief Export

The macro brief can be exported to **PDF** for:

* Blog posts
* Social media (LinkedIn, Twitter, WhatsApp)
* Internal distribution

Export scripts dynamically determine the **latest snapshot month**.

---

## Project Structure

```
macrogauge/
├── app.py                     # Main Streamlit app
├── pages/
│   ├── macro_brief_dashboard.py
│   ├── macro_risk_monitor.py
│   ├── fiscal_dashboard.py
│   └── commodities_dashboard.py
├── utils/
│   ├── data_loader.py
│   ├── economic_analysis.py
│   └── macro_brief_exporter.py
├── data/                      # Raw and processed CSVs
├── requirements.txt
└── README.md
```

---

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Round Gogos** — Economist & Developer
MacroGauge aims to be a **macro intelligence system** for Zambia, integrating fiscal, monetary, and commodity analytics with consistent branding for professional communication.
