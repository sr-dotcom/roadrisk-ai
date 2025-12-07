# 🚦 RoadRisk AI

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-orange.svg)](https://scikit-learn.org/)

> **Real-time traffic accident risk prediction powered by Machine Learning and live weather data.**

[▶️ Live Demo](https://roadrisk-ai.streamlit.app) · [📊 Demo Scenarios](DEMO_SCENARIOS.md)

---

## 📌 Overview

This application predicts the **probability of traffic accidents** based on:

| Factor | Description |
|--------|-------------|
| 📍 **Location** | Address and state (DC, PA, FL, NC, NY, CA) |
| 🌤️ **Weather** | Live data from Open-Meteo API (temperature, precipitation, wind) |
| 🕐 **Time** | Current or manually selected time of day |
| 🚗 **Vehicle** | Vehicle type and driver information |

The model was trained on **traffic violation data** and uses a **Random Forest Classifier** to predict accident risk.

---

## 🖥️ Screenshots

| Main Interface | Risk Prediction |
|----------------|-----------------|
| *Address search with auto-suggest* | *Visual risk gauge with weather info* |

---

## 🛠️ Technologies Used

- **Frontend**: [Streamlit](https://streamlit.io/) - Modern Python web framework
- **ML Model**: [scikit-learn](https://scikit-learn.org/) - Random Forest Classifier
- **Geocoding**: [Nominatim/OpenStreetMap](https://nominatim.org/) - Address lookup
- **Weather API**: [Open-Meteo](https://open-meteo.com/) - Free weather data
- **Data Processing**: Pandas, NumPy

---

## 📁 Project Structure

```
ABIA_PROJECT/
├── data/
│   └── processed/           # Cleaned, transformed data
├── models/                  # Trained model artifacts (.pkl)
├── notebooks/               # Jupyter notebooks for exploration
├── src/                     # Reusable Python modules
│   ├── config.py            # Constants and mappings
│   ├── data_processing.py   # Data cleaning functions
│   ├── features.py          # Feature engineering
│   └── models.py            # Model loading utilities
├── streamlit_app/           # Streamlit web application
│   └── main.py
├── .streamlit/              # Streamlit Cloud config
├── run.py                   # App launcher script
├── requirements.txt         # Python dependencies
├── DEMO_SCENARIOS.md        # Test scenarios for presentation
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sr-dotcom/roadrisk-ai.git
   cd roadrisk-ai
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```
   Or directly:
   ```bash
   streamlit run streamlit_app/main.py
   ```

5. **Open your browser** at `http://localhost:8501`

---

## 📊 Model Information

| Aspect | Details |
|--------|---------|
| **Algorithm** | Random Forest Classifier |
| **Features** | Weather, time, location, vehicle type |
| **Training Data** | Traffic violation records |
| **Output** | Accident probability (0-100%) |

### Risk Levels
- 🟢 **Low Risk** (0-25%): Favorable conditions
- 🟡 **Moderate Risk** (25-50%): Exercise caution
- 🔴 **High Risk** (50%+): Consider delaying travel

---

## 🌐 Deployment

### Streamlit Cloud
This app is deployed on [Streamlit Community Cloud](https://streamlit.io/cloud).

To deploy your own:
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Set main file: `streamlit_app/main.py`
6. Deploy!

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Naga Sathwik Reddy Gona**  
Master's in Data Science and Business Analytics  
University of North Carolina at Charlotte

[![GitHub](https://img.shields.io/badge/GitHub-sr--dotcom-181717?logo=github)](https://github.com/sr-dotcom)

---

## 🙏 Acknowledgments

- [Open-Meteo](https://open-meteo.com/) for free weather API
- [OpenStreetMap/Nominatim](https://nominatim.org/) for geocoding services
- [Streamlit](https://streamlit.io/) for the amazing web framework
