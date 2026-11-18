from pathlib import Path
from html import escape
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Roast & Grind | Analytics", layout="wide")
ROOT = Path(__file__).resolve().parent
SEGMENTS = ROOT / "data/processed/customer_segments_final.csv"
RAW = ROOT / "data/raw/roast_and_grind_transactions.csv"
PALETTE = ["#7B907E", "#5F7667", "#9FB0A1", "#B7C5B7", "#3F5146", "#D9E0D5"]

st.markdown("""
<style>
:root {--ink:#242B24;--muted:#667064;--line:#CED5CB;--paper:#FFFFFF;--shell:#F4F2EB;}
.subtitle {display:none!important;}
.stApp {background:var(--shell);color:#242B24;font-family:"Segoe UI", Arial, sans-serif;}
[data-testid="stHeader"] {background:transparent;height:0;}
[data-testid="stMainBlockContainer"] {background:var(--paper);padding:2.35rem 2.15rem 2rem;max-width:1500px;min-height:100vh;margin:0 auto;}
[data-testid="stSidebar"] {background:#B7C5B7;border-right:1px solid #A7B7A8;width:280px!important;}
[data-testid="stSidebar"] > div:first-child {padding:2.5rem 1.15rem 1rem;width:280px!important;}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {gap:.55rem;}
h1,h2,h3 {color:var(--ink);letter-spacing:-.45px;}
h1 {font-size:2.45rem!important;font-weight:760!important;margin:0 0 1.15rem!important;padding-bottom:.45rem;color:#242B24;text-shadow:0 1px 0 #fff;border-bottom:1px solid #DDE3DB;}
.brand {font-size:23px;font-weight:780;color:#242B24;margin:0 0 24px;line-height:1.15;}
.brand-mark {font-size:21px;margin-right:7px;vertical-align:-2px;}
.brand-sub {display:none;}
.sidebar-label {font-size:12px;font-weight:650;color:#503d37;margin:10px 0 5px;}
.kpi-grid {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:0 0 20px;}
.kpi {background:linear-gradient(145deg,#fff 70%,#F4F2EB);border:1px solid #CED5CB;border-radius:7px;padding:12px 10px 10px;text-align:center;box-shadow:0 3px 9px #3F514612;min-height:108px;}
.kpi-label {font-size:15px;color:#667064;line-height:18px;}
.kpi-value {font-size:clamp(24px,2.15vw,31px);font-weight:780;line-height:1.25;color:#242B24;margin-top:7px;overflow-wrap:anywhere;}
.kpi-note {font-size:11px;color:#6f9a6d;margin-top:2px;}
[data-testid="stVerticalBlockBorderWrapper"] {border:0!important;border-radius:0!important;box-shadow:none!important;padding:.15rem 0!important;}
[data-testid="stVerticalBlockBorderWrapper"] h3 {font-size:17px;font-weight:700;margin:.05rem .45rem .35rem!important;}
[data-testid="stPlotlyChart"] {border:1px solid #CED5CB;border-radius:7px;background:#fff;padding:6px 8px 2px;box-shadow:0 3px 10px #3F514610;overflow:hidden;}
[data-testid="stSidebar"] label {color:#242B24!important;font-size:13px!important;}
[data-testid="stSelectbox"] > div > div,[data-testid="stMultiSelect"] > div > div {background:#fff!important;border-color:#d5cec4!important;min-height:38px!important;border-radius:5px!important;}
[data-testid="stRadio"] > div {gap:1px!important;}
[data-testid="stRadio"] label {border-radius:5px;padding:7px 8px!important;}
[data-testid="stRadio"] label:hover {background:#f8f7f3;}
[data-testid="stDataFrame"] {border:none!important;font-size:13px!important;}
[data-testid="stDataFrame"] th {background:#f4f1eb!important;color:#4a3a35!important;}
.stButton button,.stDownloadButton button {border-radius:6px;border-color:#bfb5a9;color:#4b4038;}
.block-container [data-testid="stHorizontalBlock"] {gap:1.25rem;}
.footer {border-top:1px solid #eee9e1;margin-top:30px;padding-top:16px;color:#91867c;font-size:12px;}
@media(max-width:700px){[data-testid="stSidebar"]{width:230px!important;}[data-testid="stMainBlockContainer"]{padding:1.5rem 1.25rem}.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
@media(max-width:650px){[data-testid="stMainBlockContainer"]{padding:1.2rem 1rem}.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr));}h1{font-size:1.75rem!important;}.subtitle{display:none!important;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def read_csv(path, modified):
    return pd.read_csv(path, dtype={"CustomerID": "string"})

def load(path):
    return read_csv(str(path), path.stat().st_mtime)

def chart_style(fig, height=320):
    fig.update_layout(template="plotly_white", height=height,
        paper_bgcolor="white", plot_bgcolor="white", font=dict(color="#242B24", size=12),
        margin=dict(l=12,r=15,t=15,b=15), legend_title_text="",
        colorway=PALETTE)
    fig.update_xaxes(gridcolor="#E5E9E2", zeroline=False)
    fig.update_yaxes(gridcolor="#E5E9E2", zeroline=False)
    return fig

if not SEGMENTS.exists():
    st.title("Roast & Grind — Customer Analytics")
    st.error("Final customer file missing. Run your clustering notebook and export data/processed/customer_segments_final.csv.")
    st.stop()

df = load(SEGMENTS)
required = {"CustomerID", "SegmentName", "recency", "frequency", "monetary"}
missing = required - set(df.columns)
if missing:
    st.error("Missing required columns: " + ", ".join(sorted(missing)))
    st.stop()
for col in ["recency", "frequency", "monetary"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
if df.empty or df[list(required)].isna().any().any() or df.CustomerID.duplicated().any():
    st.error("Use one row per customer with valid customer IDs, segments, and numeric RFM values.")
    st.stop()
if (df.frequency <= 0).any() or (df.monetary < 0).any() or (df.recency < 0).any():
    st.error("Frequency must be positive; recency and monetary values must be nonnegative.")
    st.stop()
names = sorted(df.SegmentName.astype(str).unique())
colors = {name: PALETTE[i % len(PALETTE)] for i,name in enumerate(names)}

raw_categories = []
raw_df = pd.DataFrame()
if RAW.exists():
    raw_df = load(RAW)
    if "Category" in raw_df:
        raw_categories = sorted(raw_df["Category"].dropna().astype(str).unique())

with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">☕</span>Roast &amp; Co.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Date Range</div>', unsafe_allow_html=True)
    date_range = st.selectbox("Date Range", ["Last 30 Days", "Last 90 Days", "Last 365 Days", "All Time"], index=3, label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Product Category</div>', unsafe_allow_html=True)
    categories = sorted(raw_categories) if "raw_categories" in globals() else []
    selected_categories = st.multiselect("Product Category", categories, default=categories, label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Customer Segments</div>', unsafe_allow_html=True)
    selected = st.multiselect("Customer Segments", names, default=names, label_visibility="collapsed")

    currency = st.selectbox("Display currency", ["INR", "USD", "EUR", "GBP"], index=0)
    st.divider()
    page = st.radio("Navigation", ["Overview", "Segment Analysis", "Customer Lookup", "Recommendations"], label_visibility="collapsed")
    st.divider()
    if "Cluster" in df:
        st.caption(f"Available clusters: {df.Cluster.nunique()}")

view = df[df.SegmentName.isin(selected)].copy()
st.title("Roast & Co. — E-Commerce Analytics")
if view.empty:
    st.info("Select at least one customer segment in the sidebar.")
    st.stop()
symbol = {"Unspecified":"", "INR":"₹", "USD":"$", "EUR":"€", "GBP":"£"}[currency]
def money(v):
    return f"{symbol}{v:,.2f}"

# Currency formatting.
# Use the currency your dataset actually represents.
currency_symbols = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£"
}

symbol = currency_symbols.get(currency, "")


def money(value):
    """Display monetary values with a currency symbol and two decimals."""
    if symbol:
        return f"{symbol}{value:,.2f}"

    return f"{value:,.2f} (currency unspecified)"


# Calculate metrics for the selected customer segments.
customers = view["CustomerID"].nunique()
revenue = view["monetary"].sum()
orders = view["frequency"].sum()

aov = revenue / orders if orders > 0 else 0

average_frequency = (
    orders / customers
    if customers > 0
    else 0
)

average_customer_spend = (
    revenue / customers
    if customers > 0
    else 0
)

# Four dashboard cards.
metrics = [
    (
        "Total Revenue",
        money(revenue),
        "Selected segment spend"
    ),
    (
        "Total Orders",
        f"{orders:,.0f}",
        "Completed purchase frequency"
    ),
    (
        "Avg Order Value",
        money(aov),
        "Revenue per order"
    ),
    (
        "Repeat Customers",
        f"{(view['frequency'] > 1).mean() * 100:.1f}%",
        "Customers with repeat orders"
    )
]

html = '<div class="kpi-grid">'

for label, value, note in metrics:
    html += (
        '<div class="kpi">'
        f'<div class="kpi-label">{escape(label)}</div>'
        f'<div class="kpi-value">{escape(value)}</div>'
        f'<div class="kpi-note">{escape(note)}</div>'
        '</div>'
    )

html += '</div>'

st.markdown(html, unsafe_allow_html=True)

profile = view.groupby("SegmentName", as_index=False).agg(
    Customers=("CustomerID","count"), Revenue=("monetary","sum"),
    Orders=("frequency","sum"), Recency=("recency","mean"),
    Frequency=("frequency","mean"), Spend=("monetary","mean"))
profile["Revenue Share (%)"] = profile.Revenue / revenue * 100 if revenue else 0
profile["Average Order Value"] = profile.Revenue / profile.Orders

if page == "Overview":
    tx = pd.DataFrame()
    if not raw_df.empty:
        cols = {"CustomerID","InvoiceDate","InvoiceNo","Quantity","UnitPrice","ProductName"}
        if cols.issubset(raw_df.columns):
            tx = raw_df.copy()
            tx["InvoiceDate"] = pd.to_datetime(tx["InvoiceDate"], errors="coerce")
            for col in ["Quantity","UnitPrice"]:
                tx[col] = pd.to_numeric(tx[col], errors="coerce")
            tx["PurchaseAmount"] = tx["Quantity"] * tx["UnitPrice"]
            tx = tx[tx["CustomerID"].isin(view["CustomerID"])]
            tx = tx[tx["Quantity"].gt(0) & tx["UnitPrice"].gt(0)]
            if "Category" in tx and selected_categories:
                tx = tx[tx["Category"].isin(selected_categories)]
            if date_range != "All Time" and tx["InvoiceDate"].notna().any():
                days = {"Last 30 Days":30,"Last 90 Days":90,"Last 365 Days":365}[date_range]
                cutoff = tx["InvoiceDate"].max() - pd.Timedelta(days=days)
                tx = tx[tx["InvoiceDate"] >= cutoff]

    with st.container():
        st.subheader("Daily E-Commerce Revenue Trend")
        if not tx.empty:
            trend = tx.groupby(tx["InvoiceDate"].dt.normalize(), as_index=False)["PurchaseAmount"].sum()
            trend.columns = ["Date","Revenue"]
            fig = px.area(trend, x="Date", y="Revenue", labels={"Revenue":"Revenue","Date":""})
            fig.update_traces(line_shape="spline", line_width=3, line_color="#7B907E", fillcolor="rgba(183,197,183,.38)")
            fig.update_layout(showlegend=False, xaxis_title=None, hovermode="x unified")
            fig.update_xaxes(showgrid=False, zeroline=False)
            fig.update_yaxes(gridcolor="#E5E9E2", tickformat="~s")
            st.plotly_chart(chart_style(fig, 360), use_container_width=True)
        else:
            st.info("No transaction data matches the selected filters.")

    with st.container():
        st.subheader("Top-Selling Coffee SKUs")
        if not tx.empty:
            top_skus = tx.groupby("ProductName", as_index=False)["Quantity"].sum().nlargest(5,"Quantity")
            top_skus = top_skus.sort_values("Quantity")
            sku_colors = ["#D9E0D5","#B7C5B7","#9FB0A1","#7B907E","#5F7667"]
            sku_map = {row.ProductName: sku_colors[i] for i, row in enumerate(top_skus.itertuples())}
            fig = px.bar(top_skus, x="Quantity", y="ProductName", orientation="h",
                text="Quantity", color="ProductName", category_orders={"ProductName":top_skus["ProductName"].tolist()},
                color_discrete_map=sku_map)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None,
                bargap=.28, uniformtext_minsize=10)
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_xaxes(showgrid=True, gridcolor="#E5E9E2", zeroline=False)
            st.plotly_chart(chart_style(fig, 360), use_container_width=True)
        else:
            st.info("No product data matches the selected filters.")

    with st.container():
        st.subheader("Recent Online Orders")
        if not tx.empty:
            recent = tx.sort_values("InvoiceDate", ascending=False).groupby("InvoiceNo", as_index=False).agg(
                Customer=("CustomerID","first"), Date=("InvoiceDate","max"),
                Items=("Quantity","sum"), Total=("PurchaseAmount","sum"))
            recent = recent.head(8).copy()
            recent["Date"] = recent["Date"].dt.strftime("%m/%d/%Y")
            recent["Total"] = recent["Total"].map(money)
            recent = recent.rename(columns={"InvoiceNo":"Order ID","Customer":"Customer","Date":"Date","Items":"Items","Total":f"Total ({currency})"})
            st.dataframe(recent, hide_index=True, use_container_width=True)
        else:
            st.info("No recent orders match the selected filters.")

elif page == "Segment Analysis":
    with st.container(border=True):
        st.subheader("Customer recency vs total spend")
        fig = px.scatter(view, x="recency", y="monetary", color="SegmentName", size="frequency",
            size_max=24, hover_name="CustomerID", color_discrete_map=colors,
            labels={"recency":"Days since last purchase", "monetary":f"Total spend ({currency})", "frequency":"Orders"})
        st.plotly_chart(chart_style(fig,430), use_container_width=True)
    shares = [c for c in ["coffee_beans_share","brew_gear_share","accessories_share"] if c in view]
    if shares:
        with st.container(border=True):
            st.subheader("Product preferences")
            pref = view.groupby("SegmentName")[shares].mean().reset_index().melt(id_vars="SegmentName", var_name="Category", value_name="Share")
            pref["Category"] = pref.Category.str.replace("_share", "", regex=False).str.replace("_", " ").str.title()
            fig = px.bar(pref,x="SegmentName",y="Share",color="Category",barmode="group",color_discrete_sequence=PALETTE)
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(chart_style(fig,370), use_container_width=True)
            st.caption("Mean customer-level spend share; each customer has equal weight.")

elif page == "Customer Lookup":
    with st.container(border=True):
        st.subheader("Customer profile")
        identifier = st.text_input("Customer ID", placeholder="CUST_0001")
        if identifier:
            found = view[view.CustomerID.str.casefold() == identifier.strip().casefold()]
            if found.empty:
                st.warning("Customer not found within the selected segments.")
            else:
                customer = found.iloc[0]
                st.write("Segment:", customer.SegmentName)
                a,b,c = st.columns(3)
                a.metric("Total Spend",money(customer.monetary))
                b.metric("Orders",f"{customer.frequency:,.0f}")
                c.metric("Recency",f"{customer.recency:.0f} days")
                if "RecommendedAction" in found and pd.notna(customer.RecommendedAction):
                    st.info(str(customer.RecommendedAction))
                st.dataframe(found,hide_index=True,use_container_width=True)

else:
    with st.container(border=True):
        st.subheader("Segment action plan")
        if "RecommendedAction" in view:
            recommendations = view[["SegmentName","RecommendedAction"]].dropna().drop_duplicates()
            st.dataframe(recommendations,hide_index=True,use_container_width=True)
            st.caption("Recommendations come from your notebook. They are proposed actions, not measured campaign results.")
        else:
            st.info("Add a RecommendedAction column in the clustering notebook to display your strategy here.")

st.download_button("Download selected customers",view.to_csv(index=False).encode("utf-8"),
    file_name="roast_and_grind_segments.csv",mime="text/csv")
st.markdown('<div class="footer">Roast & Grind | Customer Intelligence · Portfolio analytics dashboard</div>', unsafe_allow_html=True)
