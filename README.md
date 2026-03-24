# Mentored-AI-Projects-
A curated collection of projects I mentored during my SDE internship, highlighting technical guidance, architectural decisions, and collaborative development practices.

## Project 2: AI based Pollution Source Identifier
> **Role:** Technical Mentor | **Tech Stack:** Python, Scikit-Learn, Pandas, SHAP, Streamlit, API

### Overview
An advanced environmental monitoring system that integrates multi-source API data to identify and visualize pollution origins. As a mentor, I oversaw the data curation, data cleaning and integration of geospatial libraries and the development of a heuristic-based labeling system for source classification.

---

### Development Roadmap & Mentorship Milestones

#### ** Milestone 1: Multi-Source Data Orchestration (Weeks 1-2)**
* **Module 1: Automated Data Collection**
    * **Air Quality:** Real-time ingestion of PM2.5, NO2, and SO2 via the **OpenAQ API**.
    * **Meteorological Data:** Weather variables (humidity, wind vectors) from **OpenWeatherMap**.
    * **Geospatial Features:** Extraction of industrial zones and road networks using **OSMnx**.
* **Module 2: Pipeline Engineering & Spatial Features**
    * Implemented data cleaning, normalization, and missing value interpolation.
    * **Feature Engineering:** Calculated spatial proximity (distance to nearest road/factory) and temporal features (hour/season) to capture cyclical pollution patterns.

#### ** Milestone 2: Synthetic Labeling & Predictive Modeling (Weeks 3-4)**
* **Module 3: Heuristic Source Labeling**
    * Designed a rule-based logic to categorize pollution sources (e.g., High NO2 + Proximity to Road = **Vehicular**).
    * Validated simulated ground-truth labels using domain-specific heuristics.
* **Module 4: Classification Engine**
    * Evaluated **Random Forest**, **XGBoost**, and **Decision Trees** for multi-class classification.
    * Guided the team through **Hyperparameter Tuning** (GridSearchCV) and performance benchmarking (F1-score/Confusion Matrix).

#### ** Milestone 3: Geospatial Intelligence & Dashboarding (Weeks 5-6)**
* **Module 5: Interactive Heatmapping**
    * Developed dynamic pollution layers using **Folium** and **GeoPandas**.
    * Implemented source-specific markers and risk-level gradients for high-severity zones.
* **Module 6: Real-Time Streamlit Dashboard**
    * Built an interactive UI featuring real-time alerts, trend charts, and source distribution pie charts.
    * Integrated filtering capabilities for date, location, and predicted source category.

#### ** Milestone 4: Deployment & Technical Reporting (Weeks 7-8)**
* **Module 7: Architecture Documentation**
    * Drafted the system architecture and data flow diagrams.
    * Finalized the technical report, including feature importance analysis and model evaluation metrics.
    * **Deployment:** Managed the application launch on **Streamlit Cloud/Hugging Face Spaces**.

---

## Key Mentorship Contributions
* **Data Integration Strategy:** Architected the method for merging disparate API outputs (Pollution vs. Weather vs. OSM) into a single, high-dimensional DataFrame.
* **Algorithmic Logic:** Assisted the team in creating the "Source Labeling" heuristics, bridging the gap between raw data and supervised learning when labels were unavailable.
* **Geospatial Best Practices:** Mentored the team on using coordinate-based filtering to optimize map rendering speeds.

---
