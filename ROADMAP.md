# Project roadmap

Planned data science and computer science projects. Each one builds on the
GeoAI for Cities work and adds a skill the current portfolio doesn't show yet.

**Ground rules**

- No empty repos. A project gets its own repository only when it has working
  code, one real figure and a README that states the question, data and limits.
- Real data, or a label. Anything run on synthetic or sample data says so in
  the first screen of its README and on the profile.
- One at a time. Finish and publish before starting the next.

| # | Title | Status |
|---|---|---|
| 1 | Will It Get Built? (real-data run) | **Next** |
| 2 | Who Waits Longer? | Planned |
| 3 | Minutes to Opportunity | Planned |
| 4 | Streets That See | Planned |
| 5 | Flood Line | Planned |
| 6 | Dangerous by Design | Planned |
| 7 | Zoning to Data | Planned |
| 8 | spatialcv | Planned |

---

### 1 · Will It Get Built? (real-data run)
**Question:** Which San Diego Housing Element sites actually got housing approvals, and does a model beat the city's capacity assumptions?
**Data:** City of San Diego Housing Element site inventory and permit records (ArcGIS REST, already scripted in `hsr.download`).
**Methods:** Existing pipeline: spatial CV, LightGBM, calibration, SHAP, equity audit.
**Why first:** The method is built and tested. Running it on real data turns a demo into a finding.

### 2 · Who Waits Longer?
**Question:** After accounting for complaint type, do 311 requests take longer to close in some NYC neighborhoods than others?
**Data:** NYC 311 Service Requests (NYC Open Data), ACS demographics.
**Methods:** Survival analysis (Kaplan–Meier, Cox models with spatial random effects), fairness metrics.
**New skill:** Time-to-event modeling on millions of rows; out-of-memory data with DuckDB or Polars.

### 3 · Minutes to Opportunity
**Question:** How many jobs can residents reach by transit in 45 minutes, and who loses most when service is cut?
**Data:** MTA GTFS feeds, OpenStreetMap, LEHD LODES job counts.
**Methods:** Travel-time matrices with r5py, accessibility indices, service-cut scenarios.
**New skill:** Graph routing at city scale; scenario analysis.

### 4 · Streets That See
**Question:** Can street-level imagery map tree cover and sidewalk condition well enough to fill gaps in city inventories?
**Data:** Mapillary open street-level imagery; NYC Street Tree Census for validation.
**Methods:** Transfer learning (CNN or vision transformer) for detection and segmentation, spatial validation.
**New skill:** Computer vision and GPU training; labeled-data workflows.

### 5 · Flood Line
**Question:** How much housing, and whose, sits inside NYC's modeled stormwater flood zones?
**Data:** NYC DEP Stormwater Flood Maps, MapPLUTO, ACS.
**Methods:** Overlay analysis, exposure indices, spatial regression.
**Why it fits:** Connects directly to my MS4/NPDES stormwater work in San Diego.

### 6 · Dangerous by Design
**Question:** Which street design features predict serious crashes, and does a graph model beat a tabular one?
**Data:** NYPD Motor Vehicle Collisions (NYC Open Data), OSMnx street networks.
**Methods:** Graph neural networks (PyTorch Geometric) vs. gradient boosting, spatial CV.
**New skill:** Deep learning on graphs.

### 7 · Zoning to Data
**Question:** Can a language model turn zoning code text into structured, checkable rules?
**Data:** NYC Zoning Resolution and San Diego Municipal Code text.
**Methods:** LLM extraction with a hand-labeled evaluation set; precision and recall by rule type.
**New skill:** NLP evaluation; honest measurement of where AI fails on legal text.

### 8 · spatialcv
**Question:** Can the spatial cross-validation used across these projects be one reusable library?
**Methods:** Python package with spatial block, buffered and leave-one-region-out CV, tests, CI and documentation, published to PyPI.
**New skill:** Software engineering: API design, packaging, versioning.
