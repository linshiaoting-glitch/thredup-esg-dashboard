"""
ThredUp Inc. — ESG & Circularity Dashboard (FY2016–FY2025)
SAM 503 · Lab 4 · Streamlit app

Audience : Sustainability analysts monitoring ESG metrics
Purpose  : Inform the Sustainability Director, who reports findings, risks and
           progress to the Board of Directors.
Data     : ThredUp 2025 Impact Report (FY2025, no external assurance), earlier
           impact reports / ESG overview, IPO prospectus (2021), 10-K filings,
           FY2025 results; Lab 2 screening estimate of the carbon footprint.
Run      : streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="ThredUp ESG Dashboard", page_icon="♻️", layout="wide")

DATA = Path(__file__).parent / "data"
C = {
    "s1": "#2a78d6", "s2": "#eb6834", "s3": "#1baf7a", "s4": "#eda100",
    "muted": "#8a8984", "grid": "#e6e5e0", "ink": "#0b0b0b", "ink2": "#52514e",
    "good": "#008300", "warn": "#c98500", "bad": "#e34948", "band": "rgba(138,137,132,0.12)",
}

st.markdown(
    """
    <style>
      .block-container {padding-top: 1.6rem;}
      div[data-testid="stMetricValue"] {font-size: 1.55rem;}
      .note {color:#52514e; font-size:0.85rem;}
      .pill {display:inline-block;padding:2px 10px;border-radius:12px;font-size:0.8rem;
             font-weight:600;margin-right:6px}
      .ok {background:#e3f2e3;color:#1f5e1f} .wa {background:#fdf0d5;color:#7a5200}
      .ba {background:#fbe3e3;color:#8a1c1c}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load():
    ts = pd.read_csv(DATA / "thredup_timeseries.csv")
    flow = pd.read_csv(DATA / "thredup_item_flow_2025.csv")
    prof = pd.read_csv(DATA / "thredup_profitability.csv")
    disc = pd.read_csv(DATA / "thredup_disclosure_matrix.csv")
    kpi = pd.read_csv(DATA / "thredup_kpis_2025.csv")
    return ts, flow, prof, disc, kpi


ts, flow, prof, disc, kpi = load()

# Lab 2 screening estimate (tCO2e, FY2025) — see Lab2_CarbonFootprint_ThredUp2025.xlsx
EST = {"Scope 1<br>(not estimated)": 0.0, "Scope 2<br>(proxy: 4 DCs)": 1648.7,
       "Scope 3<br>(Cat. 3 + 9 only)": 1469.4}
AVOIDED = pd.DataFrame({"year": [2020, 2023, 2025], "m_lbs": [1000, 791.1, 1300],
                        "source": ["IPO prospectus", "ESG overview 2023", "2025 Impact Report"]})


def base_layout(fig, title, ytitle, height=360, years=True):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=C["ink"])),
        height=height, margin=dict(l=10, r=10, t=50, b=70),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Inter, Arial, sans-serif", color=C["ink2"], size=12),
        legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="left", x=0),
        hovermode="x unified",
    )
    if years:
        fig.update_xaxes(showgrid=False, linecolor=C["grid"], dtick=1, range=[yr[0] - 0.5, yr[1] + 0.5])
    else:
        fig.update_xaxes(showgrid=False, linecolor=C["grid"])
    fig.update_yaxes(title=ytitle, gridcolor=C["grid"], zeroline=False)
    return fig


def add_eras(fig, show):
    if not show:
        return fig
    for x0, x1, label in ((2020.5, 2022.5, "incl. Europe"), (2022.5, 2025.5, "US continuing ops")):
        if x1 > yr[0] and x0 < yr[1]:
            fig.add_vrect(x0=max(x0, yr[0] - 0.5), x1=min(x1, yr[1] + 0.5),
                          fillcolor=C["band"] if label == "incl. Europe" else "rgba(0,0,0,0)", line_width=0)
            fig.add_annotation(x=(max(x0, yr[0] - 0.5) + min(x1, yr[1] + 0.5)) / 2, y=1.04, yref="paper",
                               text=label, showarrow=False, font=dict(size=11, color=C["ink2"]))
    return fig


# Sidebar
with st.sidebar:
    st.header("Filters")
    yr = st.slider("Year range", 2016, 2025, (2016, 2025))
    show_eras = st.toggle("Show reporting-basis changes", value=True)
    st.divider()
    st.markdown(
        "**Company:** ThredUp Inc. (Nasdaq & LTSE: TDUP)  \n**Sector:** Online apparel resale  \n"
        "**Reporting:** voluntary Impact Report (4th edition); no CSRD/ISSB mandate  \n"
        "**Assurance:** none on impact data"
    )
    st.caption("Built for SAM 503 Lab 4 · Data compiled Nov 2026")

view = ts[(ts.year >= yr[0]) & (ts.year <= yr[1])].copy()

st.title("ThredUp — ESG & Circularity Dashboard")
st.markdown(
    '<span class="note">For sustainability analysts → Sustainability Director → Board. FY2016–FY2025. '
    "ThredUp is a private company until its 2021 IPO, so public data starts in FY2018.</span>",
    unsafe_allow_html=True,
)

k = st.columns(6)
k[0].metric("Revenue 2025", "$310.8M", "+19.5% vs 2024")
k[1].metric("Loss from cont. ops", "$20.2M", "-6.5% of revenue", delta_color="off")
k[2].metric("Items processed (cumul.)", "261M", "since 2009", delta_color="off")
k[3].metric("Items kept in use", "~90%", "10% recycled", delta_color="off")
k[4].metric("CO₂e avoided (cumul., LCA)", "1.3B lbs", "not an inventory", delta_color="off")
k[5].metric("Own GHG inventory", "Not disclosed", "no target", delta_color="off")

tabs = st.tabs(["🧭 Board summary", "📈 Business", "♻️ Circularity", "🌍 Climate",
                "👥 Social & governance", "🔎 Data quality & sources"])

# 1. Board summary
with tabs[0]:
    left, right = st.columns([1.15, 1])
    with left:
        st.subheader("Key ESG questions this dashboard answers")
        qa = [
            ("1. Is the circular model delivering impact?",
             "Yes on outcomes: ~90% of received items go back into use; 261M items processed since 2009."),
            ("2. Is growth now profitable?",
             "Improving: revenue +19.5% to $310.8M; loss narrowed to 6.5% of revenue; adj. EBITDA 4.4%."),
            ("3. What is ThredUp's own carbon footprint?",
             "Unknown: no Scope 1–3 inventory or target. Our proxy estimate is ~3 kt CO₂e (partial, low confidence)."),
            ("4. Are the avoided-emissions claims reliable?",
             "Directionally: cumulative CO₂e avoided moved 1.0B → 0.79B → 1.3B lbs as the LCA changed; no assurance."),
            ("5. How transparent is social reporting?",
             "Weaker: 2025 report drops the workforce and board diversity figures published in 2022–23."),
            ("6. Can the Board compare trends over 10 years?",
             "Only financially from 2018, with a break for Europe (2021–24). ESG trends are not possible."),
        ]
        st.markdown("\n".join(["| Question | Short answer |", "|---|---|"] + [f"| {a} | {b} |" for a, b in qa]))
        st.subheader("The story the data tells")
        st.markdown(
            "- **The business model is the impact.** Every resold item displaces a new one; ThredUp's LCA puts the "
            "saving at 8.41 lbs CO₂e per item (≈25% lower than buying new).\n"
            "- **Growth is back and losses are shrinking.** After divesting Europe in 2024, US revenue grew 19.5% "
            "and active buyers rose 30% to 1.65M.\n"
            "- **Measurement lags the mission.** ThredUp reports what its customers avoid, not what it emits, and "
            "nothing is externally assured.\n"
            "- **Disclosure is moving backwards on 'S'.** Diversity data were dropped in the 2025 report."
        )
    with right:
        st.subheader("Areas needing urgent attention")
        st.markdown(
            '<span class="pill ba">HIGH</span> **No GHG inventory or climate target** — a 2021–22 inventory was '
            "completed but never published. At $311M revenue ThredUp is below California SB 253's $1B "
            "threshold, so disclosure stays voluntary — yet RaaS brand partners need this data for their own Scope 3.<br>"
            '<span class="pill ba">HIGH</span> **Avoided-emissions claims without assurance** — greenwashing and '
            "litigation risk as FTC Green Guides and EU-style rules tighten.<br>"
            '<span class="pill wa">MED</span> **Declining social transparency** — diversity, pay and safety data '
            "absent for a 1,817-person warehouse workforce.<br>"
            '<span class="pill wa">MED</span> **RaaS volumes falling** — 2.3M → 1.7M items (−26%) despite '
            "50+ brand partners.<br>"
            '<span class="pill ok">LOW</span> **Recycling channel shrinking** — Clean Out bags recycled 182,400 → '
            "126,840 lbs.",
            unsafe_allow_html=True,
        )
        st.subheader("Recommendations")
        st.markdown(
            "1. **Publish a FY2025 GHG inventory (Scope 1–3)** using the existing 2021–22 work as a base, "
            "and set a science-based target.\n"
            "2. **Obtain limited assurance** on the LCA-based avoided-emissions figures and report them "
            "separately from the inventory.\n"
            "3. **Restore workforce metrics**: gender, pay equity, injury rate and training hours for DC staff.\n"
            "4. **Disclose DC energy use and procure renewable electricity** for the four distribution centres.\n"
            "5. **Report RaaS and aftermarket results consistently each year** so trends can be tracked."
        )

# 2. Business
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(x=view.year, y=view.revenue_m_usd, name="Revenue",
                               marker=dict(color=C["s1"], cornerradius=4),
                               text=[f"{v:,.0f}" if pd.notna(v) else "" for v in view.revenue_m_usd],
                               textposition="outside", cliponaxis=False))
        base_layout(fig, "Revenue ($M)", "$M")
        st.plotly_chart(add_eras(fig, show_eras), use_container_width=True)
    with c2:
        fig = go.Figure(go.Scatter(x=view.year, y=view.net_margin_pct, mode="lines+markers",
                                   line=dict(color=C["s2"], width=2), marker=dict(size=8),
                                   name="Net loss margin"))
        fig.add_hline(y=0, line_color=C["muted"], line_width=1)
        base_layout(fig, "Net loss as % of revenue (2023+ = continuing ops)", "%")
        st.plotly_chart(add_eras(fig, show_eras), use_container_width=True)
    c3, c4 = st.columns(2)
    with c3:
        p = prof[prof.metric.str.contains("margin")]
        fig = go.Figure()
        for col, yname, colr in (("v_2023", "2023", C["grid"]), ("v_2024", "2024", C["muted"]), ("v_2025", "2025", C["s1"])):
            fig.add_trace(go.Bar(x=p.metric, y=p[col], name=yname, marker=dict(color=colr, cornerradius=4)))
        base_layout(fig, "Margins, continuing operations (%)", "%", years=False)
        fig.update_layout(barmode="group")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        ab = ts[ts.active_buyers_m.notna()]
        fig = go.Figure(go.Scatter(x=ab.year, y=ab.active_buyers_m, mode="lines+markers",
                                   line=dict(color=C["s3"], width=2), marker=dict(size=9), name="Active buyers"))
        base_layout(fig, "Active buyers (millions, where reported)", "million")
        st.plotly_chart(fig, use_container_width=True)
    st.caption("2021–2022 include Remix (Europe, acquired Oct-2021). Europe was divested Nov-2024; 2023–2025 "
               "are continuing (US) operations as restated. FY2023 total revenue incl. Europe was $322.0M.")

# 3. Circularity
with tabs[2]:
    c1, c2 = st.columns(2)
    with c1:
        f = flow.sort_values("pct_2025")
        colors = [C["s3"] if "Recycled" not in d else C["s4"] for d in f.destination]
        fig = go.Figure(go.Bar(y=f.destination, x=f.pct_2025, orientation="h",
                               marker=dict(color=colors, cornerradius=4),
                               text=[f"{v}%" for v in f.pct_2025], textposition="outside", cliponaxis=False))
        base_layout(fig, "Where received items went in 2025 (% of items)", "", years=False)
        fig.update_xaxes(range=[0, 75], title="% of items received")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        it = ts[ts.cum_items_processed_m.notna()]
        fig = go.Figure(go.Scatter(x=it.year, y=it.cum_items_processed_m, mode="lines+markers+text",
                                   text=[f"{v:.0f}M" for v in it.cum_items_processed_m], textposition="top center",
                                   line=dict(color=C["s1"], width=2), marker=dict(size=9), name="Items"))
        base_layout(fig, "Cumulative secondhand items processed (millions; 2020/2023 = 'over')", "million")
        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)
    c3, c4 = st.columns(2)
    with c3:
        r = ts[ts.raas_items_m.notna()]
        fig = go.Figure(go.Bar(x=r.year, y=r.raas_items_m, marker=dict(color=C["s2"], cornerradius=4),
                               text=[f"{v}M" for v in r.raas_items_m], textposition="outside", name="RaaS"))
        base_layout(fig, "Resale-as-a-Service items recirculated (millions)", "million")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        a = ts[ts.azek_bags_recycled_lbs.notna()]
        fig = go.Figure(go.Bar(x=a.year, y=a.azek_bags_recycled_lbs / 1000, marker=dict(color=C["s4"], cornerradius=4),
                               text=[f"{v/1000:,.0f}k" for v in a.azek_bags_recycled_lbs], textposition="outside",
                               name="Bags"))
        base_layout(fig, "Clean Out bags recycled into decking (thousand lbs)", "thousand lbs")
        st.plotly_chart(fig, use_container_width=True)
    m = st.columns(3)
    m[0].metric("Rescue items sold 2025", "680,421", "-11.8% vs 2024", delta_color="normal")
    m[1].metric("RaaS brand partners", "50+", "Gap, Reformation, J.Crew…", delta_color="off")
    m[2].metric("DC02 electricity", "−117,000 kWh", "−8.5% (LED + scheduling)")

# 4. Climate
with tabs[3]:
    st.info("ThredUp does not publish Scope 1, 2 or 3 emissions. The bars below are our **Lab 2 screening "
            "estimate** from proxies (DC02 electricity × 4 DCs, outbound parcels). Treat as low-confidence.")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(x=list(EST.keys()), y=list(EST.values()),
                               marker=dict(color=[C["muted"], C["s2"], C["s3"]], cornerradius=4),
                               text=[f"{v:,.0f} t" if v else "gap" for v in EST.values()], textposition="outside"))
        base_layout(fig, "Estimated own footprint FY2025 (t CO₂e) — partial", "t CO₂e", years=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = go.Figure(go.Bar(x=AVOIDED.year.astype(str) + "<br>" + AVOIDED.source, y=AVOIDED.m_lbs,
                               marker=dict(color=C["s3"], cornerradius=4),
                               text=[f"{v:,.0f}M lbs" for v in AVOIDED.m_lbs], textposition="outside"))
        base_layout(fig, "Cumulative CO₂e avoided by buyers, as claimed (million lbs)", "million lbs", years=False)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**How to read this:** the cumulative 'avoided' figure fell from 1.0B lbs (2020 prospectus) to 791M lbs "
        "(2023) before rising to 1.3B lbs (2025) — a cumulative total cannot fall, so the LCA method changed. "
        "Under the GHG Protocol, avoided emissions are reported **separately** and never subtracted from a "
        "company's own inventory. Estimated own footprint ≈ 3,100 t CO₂e ≈ 10 t per $M revenue (partial)."
    )

# 5. Social & governance
with tabs[4]:
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.subheader("What ThredUp discloses, by report year")
        d = disc.copy()
        z = d[["report_FY2023", "report_FY2025"]].values
        fig = go.Figure(go.Heatmap(z=z, x=["FY2023 report / ESG overview", "FY2025 report"], y=d.topic,
                                   colorscale=[[0, "#fbe3e3"], [0.5, "#fdf0d5"], [1, "#d6ecd6"]], zmin=0, zmax=1,
                                   showscale=False, xgap=3, ygap=3,
                                   text=[["Yes" if v == 1 else "Partial" if v == 0.5 else "No" for v in row] for row in z],
                                   texttemplate="%{text}", hovertext=[[n] * 2 for n in d.note], hoverinfo="text"))
        fig.update_layout(height=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white",
                          font=dict(family="Inter, Arial, sans-serif", size=12, color=C["ink2"]))
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Green = disclosed, amber = partial, red = not disclosed. FY2023 = 2024 Impact Report coverage "
                   "and ThredUp ESG overview; FY2024 report not fully retrieved.")
    with c2:
        st.subheader("Employee survey 2025")
        sv = pd.DataFrame({"item": ["Understand how work contributes", "Invested in mission & values",
                                    "Manager is supportive", "Equal opportunity for all backgrounds"],
                           "pct": [96, 91, 90, 85]})
        fig = go.Figure(go.Bar(y=sv.item, x=sv.pct, orientation="h", marker=dict(color=C["s1"], cornerradius=4),
                               text=[f"{v}%" for v in sv.pct], textposition="outside", cliponaxis=False))
        base_layout(fig, "% favourable", "", height=260, years=False)
        fig.update_xaxes(range=[0, 110])
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Diversity — last disclosed")
        st.table(pd.DataFrame({
            "Metric": ["Workforce female", "Workforce minority", "Board female", "Board racial minority"],
            "FY2022": ["66%", "72%", "50%", "20%"], "FY2023": ["73%", "73%", "44%", "22%"],
            "FY2025": ["n/d", "n/d", "n/d", "n/d"]}).set_index("Metric"))
    st.caption("Governance: all directors except the CEO independent; Nominating & ESG Committee oversees ESG "
               "with quarterly briefings; Code of Conduct and whistleblower hotline; SOC 2 Type 2 and PCI DSS L2; "
               "listed on the Long-Term Stock Exchange. No B Corp certification or public-benefit-corporation status is disclosed.")

# 6. Data quality
with tabs[5]:
    st.subheader("How far can each number be trusted?")
    dq = pd.DataFrame({
        "Data": ["Financials (10-K)", "Operating KPIs (buyers, orders)", "Item flows & circularity",
                 "Avoided emissions (LCA)", "Own GHG footprint", "Social & diversity", "Governance"],
        "Score": [100, 90, 55, 45, 10, 35, 60],
        "Why": ["Audited financial statements; Europe restated as discontinued",
                "Company-reported KPIs in earnings releases",
                "Company estimates in % only; no tonnes; no assurance",
                "Green Story LCA; cumulative totals changed with method; no assurance",
                "Not disclosed — Lab 2 proxy estimate only",
                "Survey % only in 2025; diversity data dropped",
                "Qualitative; board size/diversity only in proxy statement"],
    })
    fig = go.Figure(go.Bar(y=dq.Data, x=dq.Score, orientation="h",
                           marker=dict(color=[C["good"] if v >= 80 else C["warn"] if v >= 40 else C["bad"]
                                              for v in dq.Score], cornerradius=4),
                           text=dq.Score, textposition="outside"))
    base_layout(fig, "Indicative data quality score (Lab 1 rubric, 0–100)", "", height=320, years=False)
    fig.update_xaxes(range=[0, 110], dtick=20)
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(dq, hide_index=True, use_container_width=True)
    st.subheader("FY2025 KPI register")
    st.dataframe(kpi, hide_index=True, use_container_width=True)
    st.subheader("Time series")
    st.dataframe(ts, hide_index=True, use_container_width=True)
    st.download_button("Download time series (CSV)", ts.to_csv(index=False).encode(),
                       "thredup_esg_timeseries.csv", "text/csv")
    st.markdown(
        "**Sources**  \n"
        "- ThredUp 2025 Impact Report (FY2025).  \n"
        "- ThredUp FY2024 Impact Report press release (Aug 2025); FY2023 Impact Report coverage; ThredUp ESG "
        "overview (2023).  \n"
        "- ThredUp IPO prospectus (424B4, Mar 2021); 10-K FY2022, FY2024, FY2025; Q4/FY2024 and Q4/FY2025 results."
    )
