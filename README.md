<p align="center"><img src="assets/banner.svg" width="100%" alt="Johan Fernandez, urban data science and GeoAI. Map of NYC's 42 UHF neighborhoods colored by heat-related ER visit rate, from 2.6 to 15.3 per 100,000, highest in Port Richmond."></p>

### Urban data scientist · GeoAI for housing, land use and infrastructure

I build **location-aware machine learning and spatial analysis** around one question: **who gets what in cities?** My work combines GIS, spatial statistics and predictive modeling with California and New York planning policy.

🎓 B.A. Urban Studies & Planning, UC San Diego · preparing for doctoral study in urban data science
📍 San Diego, CA · 📫 jhoven.jan98@gmail.com
🌐 **[GeoAI for Cities research site](https://johanarisato.github.io/geoai-for-cities/)** · [Portfolio](https://johanarisato.github.io/Johan.github.io/)

---

### 🧭 Research focus

- **GeoAI for housing policy:** predicting where zoned capacity actually becomes housing, and auditing those predictions for equity
- **Spatially honest machine learning:** spatial cross-validation, calibration and explainability, so models hold up in places they have never seen
- **Ranking and fairness:** how the rule a city uses to rank neighborhoods decides who benefits first
- **Responsible AI in city government:** transparency and resident voice in AI-assisted decisions (3rd place, UCSD Urban Expo)

---

### ✍️ Blog: GeoAI for Cities series

- **[Part 1 · What Is GeoAI? Definitions, Foundations and Five Verbs Across U.S. Cities](https://johanarisato.github.io/geoai-for-cities/#part-1)**
- **[Part 2 · Who Gets the Shade? Ranking New York Neighborhoods for Tree Planting](https://johanarisato.github.io/geoai-for-cities/#part-2)** (working paper)
- [Research Notes: Questions, Methods and Data](https://johanarisato.github.io/geoai-for-cities/#research) · [All posts](https://johanarisato.github.io/geoai-for-cities/#blog)

---

### 🗺️ GeoAI for Cities: research projects

Each project has an interactive demo: [shade map](https://johanarisato.github.io/geoai-for-cities/explore/shade.html) · [housing explorer](https://johanarisato.github.io/geoai-for-cities/explore/housing.html) · [CurbCall app](https://johanarisato.github.io/geoai-for-cities/explore/curbcall.html) · [database explorer](https://johanarisato.github.io/geoai-for-cities/explore/database.html)

| Project | Question | Methods |
|---|---|---|
| **[Will It Get Built?](https://github.com/JohanArisato/housing-site-realization)** | Which of San Diego's 2021 Housing Element sites actually got housing approvals, and can a model predict it better than the city's capacity assumptions? *Pipeline built and validated on synthetic data; real-data run in progress.* | Spatial CV, LightGBM, calibration, SHAP, equity audit |
| **[Who Gets the Shade?](https://github.com/JohanArisato/who-gets-the-shade)** | When NYC ranks neighborhoods for tree planting, how much does the ranking rule change who benefits? | Moran's I/LISA, spatial lag & error models, leave-one-borough-out CV, 5,000 random weightings |
| **[CurbCall](https://github.com/JohanArisato/curbcall)** | If residents report and vote on what to fix first, whose problems get heard? | Product prototype, PostGIS data model, per-area ranking |
| **[GeoAI for Cities](https://github.com/JohanArisato/geoai-for-cities)** | What is GeoAI, and who benefits when cities use it to decide? | Research website and article series |
| **[geoai-cities-db](https://github.com/JohanArisato/geoai-cities-db)** | One spatial database behind every project | GeoPackage + PostGIS, data catalog with synthetic-data flags, cross-project spatial views |

**Who Gets the Shade? in one line:** across NYC's 42 UHF neighborhoods, each point of tree canopy is associated with 0.17 °F lower surface temperature, but heat-related ER visits track poverty (r = 0.59) far more than heat. Switching the ranking rule moves the poorest neighborhoods from 4 to 9 of the first 10 planted. (The equity-weighted rule includes poverty directly, so part of that jump is by design; the open question is what each rule trades away.)

<p align="center">
  <a href="https://github.com/JohanArisato/who-gets-the-shade"><img src="https://raw.githubusercontent.com/JohanArisato/who-gets-the-shade/main/figures/04_maps.png" width="100%" alt="Two NYC maps: heat-related ER visit rates by neighborhood, and how often each neighborhood lands in the top 10 planting priorities across 5,000 ranking weightings"></a>
</p>
<p align="center">
  <a href="https://github.com/JohanArisato/who-gets-the-shade"><img src="https://raw.githubusercontent.com/JohanArisato/who-gets-the-shade/main/figures/03_ranking_rules.png" width="70%" alt="Bar chart: poorest-third neighborhoods among the first 10 planted under five ranking rules, from 4 of 10 (canopy gap) to 9 of 10 (equity-weighted)"></a>
</p>
<p align="center"><sub>Real data: NYC Environment &amp; Health Data Portal, 42 UHF neighborhoods. Code and reproduction tests in <a href="https://github.com/JohanArisato/who-gets-the-shade">who-gets-the-shade</a>.</sub></p>

#### How the projects fit together

<p align="center"><img src="assets/system_map.svg" width="100%" alt="System map: NYC health data, San Diego Housing Element sites and resident reports feed geoai-cities-db, which powers Who Gets the Shade? (live, real data), Will It Get Built? (testing, synthetic data) and CurbCall (prototype)."></p>

---

### 🚧 Next up

Planned projects, built one at a time. Full list with data sources and methods in **[ROADMAP.md](ROADMAP.md)**.

- **Will It Get Built? (real-data run):** run the tested pipeline on San Diego's actual permit records
- **Who Waits Longer?:** survival analysis of NYC 311 response times by neighborhood
- **Minutes to Opportunity:** transit access to jobs from MTA GTFS with r5py
- **Streets That See:** computer vision on street-level imagery, validated against NYC's tree census

---

### 🛠️ Applied GIS work

| Project | What I did |
|---|---|
| Municipal stormwater priority mapping | Geodatabases ranking Capital Improvement Plan sites across four San Diego cities under MS4/NPDES permits |
| UCSD campus CAD-to-GIS & UAV mapping | Georeferenced 1,788 AutoCAD drawings into an ArcGIS Pro basemap; drone orthomosaics with Drone2Map |
| Community health equity mapping | Census/ACS data joined with infrastructure layers to find service gaps in underserved neighborhoods |

---

### 🧰 Toolkit

**GeoAI & ML:** Python · GeoPandas · PySAL (esda, spreg) · scikit-learn · LightGBM · SHAP
**Spatial data:** PostgreSQL/PostGIS · GeoPackage · GDAL/OGR · SQL · ArcGIS Pro · ArcPy · QGIS · Drone2Map
**Web & viz:** Folium/Leaflet · D3 · Power BI · Tableau
**Planning:** Housing Element & RHNA · land use & zoning · CEQA · MS4/NPDES · equity mapping
