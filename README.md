# ThredUp — ESG & Circularity Dashboard (SAM 503 · Lab 4)

Interactive Streamlit dashboard on ThredUp Inc.'s ESG and circularity performance, FY2016–FY2025, for
sustainability analysts who brief the Sustainability Director and the Board.

## Student inputs (Lab 4 brief)
| Item | Input |
|---|---|
| Company | ThredUp Inc. (Nasdaq & LTSE: TDUP), Oakland, CA |
| Industry | Online apparel resale / e-commerce |
| Audience | Sustainability analysts monitoring and reporting ESG metrics |
| Purpose | Inform the Sustainability Director → Board on findings, risks and progress |
| Time horizon | FY2016–FY2025 (public data from FY2018; private before the 2021 IPO) |
| Key questions | Is the circular model delivering impact? Is growth profitable? What is ThredUp's own footprint? Are avoided-emissions claims reliable? How transparent is social reporting? Can trends be compared? |
| Environmental | Item end-of-life flows, items processed, RaaS volumes, Clean Out bag recycling, DC energy, avoided CO₂e (LCA), Lab 2 screening footprint |
| Social | Employees, employee survey, last-disclosed workforce diversity |
| Governance | Board independence & ESG oversight, ethics, cybersecurity, disclosure matrix, assurance |
| Targets | None disclosed (shown as a gap) |
| Visuals | KPI cards, revenue/margin trends with reporting-basis bands, item-flow bars, disclosure heatmap, footprint vs avoided-emissions bars |

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
Deploy on Streamlit Community Cloud: push to GitHub → share.streamlit.io → New app → `app.py`.

## Data caveats
- **ThredUp publishes no Scope 1–3 inventory.** The footprint shown is our Lab 2 screening estimate (DC02
  electricity scaled to 4 DCs; outbound parcels) — low confidence.
- **Avoided emissions** (1.3B lbs CO₂e cumulative) come from a Green Story LCA, are not assured and changed
  with methodology (1.0B lbs in 2020 → 791M lbs in 2023 → 1.3B lbs in 2025).
- **Reporting basis:** 2021–2022 include Europe (Remix); Europe was divested Nov-2024; 2023–2025 are US
  continuing operations as restated.

## Sources
ThredUp 2025 Impact Report; FY2024 Impact Report press release (Aug 2025); ESG overview (2023); IPO prospectus
(424B4, 2021); 10-K FY2022, FY2024, FY2025; Q4/FY2024 and Q4/FY2025 results.
