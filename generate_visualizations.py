"""
SUPERSCOPE Visual Dashboard Generator (Pixel-Perfect Polished Edition)
Produces publication-grade, ultra-clean, modern dark/navy analytics dashboards.
Elevate Labs Data Analyst Internship - Task 2: Data Visualization and Storytelling
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
import pandas as pd
import numpy as np

# Modern typography & dark palette
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#F8FAFC'
plt.rcParams['axes.labelcolor'] = '#94A3B8'
plt.rcParams['xtick.color'] = '#94A3B8'
plt.rcParams['ytick.color'] = '#94A3B8'

BG_COLOR = '#0A0E1A'        # Very dark navy background
CARD_BG = '#131B2E'         # Slate dark card container
CARD_BORDER = '#22304A'     # Subtle border
TEXT_MUTED = '#94A3B8'      # Slate 400
TEXT_MAIN = '#F8FAFC'       # Slate 50
ACCENT_BLUE = '#0EA5E9'     # Sky / Cyan accent
ACCENT_CYAN = '#06B6D4'     # Electric Cyan
ACCENT_GREEN = '#10B981'    # Emerald profit
ACCENT_AMBER = '#F59E0B'    # Warning amber
ACCENT_RED = '#EF4444'      # Crimson loss
ACCENT_PURPLE = '#8B5CF6'   # Indigo purple

def load_data():
    df = pd.read_csv('data/cleaned/Superstore_Cleaned.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    return df

def draw_header(fig, title_act, subtitle):
    """Draws standardized, perfectly spaced header banner"""
    fig.text(0.04, 0.958, "SUPERSCOPE", fontsize=24, fontweight='bold', color=ACCENT_CYAN, va='top')
    fig.text(0.185, 0.958, f"|  {title_act}", fontsize=21, fontweight='bold', color=TEXT_MAIN, va='top')
    fig.text(0.04, 0.922, subtitle, fontsize=11.5, color=TEXT_MUTED, va='top')
    fig.text(0.96, 0.958, "US MULTI-REGION • 9,994 TRANSACTIONS", fontsize=10.5, fontweight='bold', color=ACCENT_BLUE,
             ha='right', va='top', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1E293B', edgecolor=ACCENT_BLUE, lw=1))

# ==============================================================================
# DASHBOARD 1: EXECUTIVE DASHBOARD
# ==============================================================================
def create_executive_dashboard(df):
    fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG_COLOR, dpi=150)
    draw_header(fig, "Retail Intelligence & Sales Story",
                "From raw transactions to actionable business decisions. Multi-year enterprise performance analysis (2014–2017)")

    # --- TOP KPI METRICS (5 Cards) ---
    kpi_specs = [
        ("TOTAL REVENUE", "$2,297,201", "+20.4% YoY Growth", ACCENT_BLUE),
        ("TOTAL NET PROFIT", "$286,397", "12.47% Net Margin", ACCENT_GREEN),
        ("TOTAL ORDERS", "5,009", "793 Unique Customers", ACCENT_PURPLE),
        ("AVG ORDER VALUE", "$458.61", "$57.18 Profit / Order", ACCENT_AMBER),
        ("DISCOUNT CAPITAL BURN", "-$125,007", "On Discounts > 30%", ACCENT_RED),
    ]
    
    card_width = 0.17
    gap = 0.015
    start_x = 0.04
    kpi_y = 0.79
    kpi_h = 0.095
    
    for i, (title, val, sub, col) in enumerate(kpi_specs):
        cx = start_x + i * (card_width + gap)
        rect = patches.FancyBboxPatch((cx, kpi_y), card_width, kpi_h, boxstyle="round,pad=0.01",
                                      facecolor=CARD_BG, edgecolor=CARD_BORDER, lw=1.2, transform=fig.transFigure)
        fig.patches.append(rect)
        bar = patches.Rectangle((cx, kpi_y), 0.005, kpi_h, facecolor=col, transform=fig.transFigure)
        fig.patches.append(bar)
        
        fig.text(cx + 0.012, kpi_y + 0.075, title, fontsize=9.5, fontweight='bold', color=TEXT_MUTED, va='top')
        fig.text(cx + 0.012, kpi_y + 0.046, val, fontsize=17.5, fontweight='heavy', color=TEXT_MAIN, va='top')
        fig.text(cx + 0.012, kpi_y + 0.018, sub, fontsize=9.2, fontweight='semibold', color=col, va='top')

    # --- ROW 1 LEFT: Yearly Sales & Profit ---
    ax1 = fig.add_axes([0.04, 0.43, 0.43, 0.31], facecolor=CARD_BG)
    ax1.set_title("Annual Revenue & Profit Escalation (2014 – 2017)", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    yearly = df.groupby('Order Year').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    years = yearly['Order Year']
    x = np.arange(len(years))
    w = 0.35
    
    rects1 = ax1.bar(x - w/2, yearly['Sales']/1000, w, label='Sales ($K)', color=ACCENT_BLUE, alpha=0.9)
    rects2 = ax1.bar(x + w/2, yearly['Profit']/1000, w, label='Profit ($K)', color=ACCENT_GREEN, alpha=0.9)
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=10.5, fontweight='semibold')
    ax1.set_ylabel("Amount ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax1.grid(axis='y', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax1.legend(loc='upper left', frameon=False, fontsize=9.5)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(CARD_BORDER)
    ax1.spines['bottom'].set_color(CARD_BORDER)
    
    for r in rects1:
        h = r.get_height()
        ax1.annotate(f"${h:,.0f}K", (r.get_x() + r.get_width()/2, h), xytext=(0, 4),
                     textcoords="offset points", ha='center', va='bottom', fontsize=9.5, color=TEXT_MAIN, fontweight='bold')
    for r in rects2:
        h = r.get_height()
        ax1.annotate(f"${h:,.0f}K", (r.get_x() + r.get_width()/2, h), xytext=(0, 4),
                     textcoords="offset points", ha='center', va='bottom', fontsize=9.5, color=ACCENT_GREEN, fontweight='bold')
    ax1.set_ylim(0, 850)

    # --- ROW 1 RIGHT: Category Dynamics ---
    ax2 = fig.add_axes([0.53, 0.43, 0.43, 0.31], facecolor=CARD_BG)
    ax2.set_title("Category Revenue vs Net Profit Realization (The Furniture Deficit)", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    cats = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values(by='Sales', ascending=True)
    y_pos = np.arange(len(cats))
    
    bar_sales = ax2.barh(y_pos + 0.18, cats['Sales']/1000, height=0.32, label='Revenue ($K)', color=ACCENT_CYAN, alpha=0.9)
    bar_profit = ax2.barh(y_pos - 0.18, cats['Profit']/1000, height=0.32, label='Net Profit ($K)',
                          color=[ACCENT_GREEN if p > 50000 else ACCENT_AMBER for p in cats['Profit']], alpha=0.9)
    
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(cats.index, fontsize=10.5, fontweight='semibold')
    ax2.set_xlabel("Amount ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax2.grid(axis='x', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax2.legend(loc='lower right', frameon=False, fontsize=9.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(CARD_BORDER)
    ax2.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bar_sales:
        w_val = r.get_width()
        ax2.annotate(f" ${w_val:,.0f}K", (w_val, r.get_y() + r.get_height()/2), xytext=(4, 0),
                     textcoords="offset points", ha='left', va='center', fontsize=9.5, color=TEXT_MAIN, fontweight='bold')
    for r in bar_profit:
        w_val = r.get_width()
        ax2.annotate(f" ${w_val:,.0f}K", (w_val, r.get_y() + r.get_height()/2), xytext=(4, 0),
                     textcoords="offset points", ha='left', va='center', fontsize=9.5,
                     color=ACCENT_GREEN if w_val > 50 else ACCENT_AMBER, fontweight='bold')
    ax2.set_xlim(0, 950)

    # --- ROW 2 LEFT: Regional Contribution & Twin Axis Margins ---
    ax3 = fig.add_axes([0.04, 0.06, 0.40, 0.29], facecolor=CARD_BG)
    ax3.set_title("Regional Contribution: West & East Outperform Central Margin", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    regions = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values(by='Sales', ascending=False)
    r_pos = np.arange(len(regions))
    
    ax3.bar(r_pos, regions['Sales']/1000, width=0.45, color=ACCENT_BLUE, alpha=0.85, label='Sales ($K)')
    ax3.set_xticks(r_pos)
    ax3.set_xticklabels(regions.index, fontsize=10.5, fontweight='semibold')
    ax3.set_ylabel("Sales ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax3.grid(axis='y', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color(CARD_BORDER)
    ax3.spines['bottom'].set_color(CARD_BORDER)
    ax3.set_ylim(0, 850)
    
    ax3_twin = ax3.twinx()
    margins = (regions['Profit'] / regions['Sales']) * 100
    ax3_twin.plot(r_pos, margins, color=ACCENT_GREEN, marker='o', linewidth=2.5, markersize=8, label='Profit Margin %')
    ax3_twin.set_ylabel("Profit Margin %", fontsize=10, color=ACCENT_GREEN)
    ax3_twin.set_ylim(0, 22)
    ax3_twin.spines['top'].set_visible(False)
    ax3_twin.spines['left'].set_visible(False)
    ax3_twin.spines['right'].set_color(CARD_BORDER)
    
    for i, m in enumerate(margins):
        ax3_twin.annotate(f"{m:.1f}%", (i, m), xytext=(0, 9), textcoords="offset points",
                          ha='center', fontsize=9.5, color=ACCENT_GREEN, fontweight='bold')
    
    lines, labels = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines + lines2, labels + labels2, loc='upper right', frameon=False, fontsize=9)

    # --- ROW 2 RIGHT: Sub-Category Profit Spectrum ---
    ax4 = fig.add_axes([0.53, 0.06, 0.43, 0.29], facecolor=CARD_BG)
    ax4.set_title("Sub-Category Profit Spectrum: Top Profit Champions vs Loss Bleeders", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    subcats = df.groupby('Sub-Category')['Profit'].sum().sort_values()
    focus_subs = pd.concat([subcats.head(3), subcats.tail(5)])
    colors = [ACCENT_RED if v < 0 else ACCENT_GREEN for v in focus_subs.values]
    
    y_sub = np.arange(len(focus_subs))
    bars_sub = ax4.barh(y_sub, focus_subs.values/1000, height=0.55, color=colors, alpha=0.9)
    ax4.axvline(0, color=TEXT_MUTED, linestyle='-', linewidth=1.2)
    ax4.set_yticks(y_sub)
    ax4.set_yticklabels(focus_subs.index, fontsize=10, fontweight='semibold')
    ax4.set_xlabel("Net Profit / Loss ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax4.grid(axis='x', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.spines['left'].set_color(CARD_BORDER)
    ax4.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bars_sub:
        val = r.get_width()
        pos = val + 1.2 if val >= 0 else val - 1.2
        ha = 'left' if val >= 0 else 'right'
        col = ACCENT_GREEN if val >= 0 else ACCENT_RED
        ax4.annotate(f"${val:,.1f}K", (pos, r.get_y() + r.get_height()/2),
                     ha=ha, va='center', fontsize=9.2, color=col, fontweight='bold')
    ax4.set_xlim(-25, 65)

    out_path = 'screenshots/executive_dashboard.png'
    plt.savefig(out_path, dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.savefig('dashboard/dashboard_screenshots/01_executive_overview.png', dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# DASHBOARD 2: SALES STORY (TIME-SERIES, PEAKS, SEASONALITY)
# ==============================================================================
def create_sales_story_dashboard(df):
    fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG_COLOR, dpi=150)
    draw_header(fig, "Act 1: The Sales Trajectory & Seasonality",
                "Tracing chronological sales expansion, Q4 holiday demand spikes, and month-by-month margin consistency.")

    # Top Full Width Plot: Monthly Time Series
    ax1 = fig.add_axes([0.04, 0.49, 0.92, 0.35], facecolor=CARD_BG)
    ax1.set_title("Monthly Revenue & Net Profit Trajectory (Jan 2014 – Dec 2017) with Inflection Points",
                  fontsize=13, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    monthly = df.set_index('Order Date').resample('ME').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    
    ax1.plot(monthly['Order Date'], monthly['Sales']/1000, color=ACCENT_BLUE, linewidth=2.8, label='Monthly Sales ($K)', zorder=4)
    ax1.fill_between(monthly['Order Date'], monthly['Sales']/1000, color=ACCENT_BLUE, alpha=0.15, zorder=2)
    
    ax1.plot(monthly['Order Date'], monthly['Profit']/1000, color=ACCENT_GREEN, linewidth=2.4, linestyle='-', label='Monthly Profit ($K)', zorder=4)
    ax1.axhline(0, color=ACCENT_RED, linestyle='--', alpha=0.5, linewidth=1)
    
    # 1. Nov 2017 Peak ($97K)
    peak_date = monthly.loc[monthly['Sales'].idxmax(), 'Order Date']
    peak_sales = monthly['Sales'].max() / 1000
    ax1.scatter([peak_date], [peak_sales], color=ACCENT_CYAN, s=90, zorder=5)
    ax1.annotate(f"All-Time Peak Sales\nNov 2017: ${peak_sales:,.0f}K",
                 xy=(peak_date, peak_sales), xytext=(-65, 18), textcoords='offset points',
                 arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=1.5),
                 fontsize=9.5, fontweight='bold', color=ACCENT_CYAN,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG, edgecolor=ACCENT_CYAN))
    
    # 2. Q4 2016 Spike
    nov_16 = monthly[monthly['Order Date'] == '2016-11-30']
    if not nov_16.empty:
        s16 = nov_16['Sales'].values[0] / 1000
        d16 = nov_16['Order Date'].values[0]
        ax1.scatter([d16], [s16], color=ACCENT_BLUE, s=70, zorder=5)
        ax1.annotate("Q4 2016 Holiday Surge\nSales: $79.4K",
                     xy=(d16, s16), xytext=(-75, -35), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->", color=ACCENT_BLUE, lw=1.2),
                     fontsize=9.2, color=TEXT_MAIN,
                     bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG, edgecolor=CARD_BORDER))

    # 3. Jan Seasonal Slump
    jan_slump = monthly[monthly['Order Date'] == '2015-01-31']
    if not jan_slump.empty:
        js = jan_slump['Sales'].values[0] / 1000
        jd = jan_slump['Order Date'].values[0]
        ax1.scatter([jd], [js], color=ACCENT_AMBER, s=70, zorder=5)
        ax1.annotate("Annual Post-Holiday Slump\nSales drops to $18.1K",
                     xy=(jd, js), xytext=(20, 20), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->", color=ACCENT_AMBER, lw=1.2),
                     fontsize=9.2, color=ACCENT_AMBER,
                     bbox=dict(boxstyle='round,pad=0.3', facecolor=CARD_BG, edgecolor=ACCENT_AMBER))

    ax1.set_ylabel("Monthly Amount ($ Thousands)", fontsize=10.5, color=TEXT_MUTED)
    ax1.grid(color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax1.legend(loc='upper left', frameon=False, fontsize=10)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(CARD_BORDER)
    ax1.spines['bottom'].set_color(CARD_BORDER)
    ax1.set_ylim(-15, 125)

    # Bottom Left: Seasonality Profile
    ax2 = fig.add_axes([0.04, 0.06, 0.43, 0.33], facecolor=CARD_BG)
    ax2.set_title("Seasonality Profile: Cumulative Sales Concentration by Calendar Month",
                  fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    df['Month_Num'] = df['Order Date'].dt.month
    month_agg = df.groupby('Month_Num').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    colors_month = [ACCENT_CYAN if m in [9, 11, 12] else ACCENT_BLUE for m in month_agg['Month_Num']]
    
    bars_m = ax2.bar(month_agg['Month_Num'], month_agg['Sales']/1000, color=colors_month, width=0.6, alpha=0.85)
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels(month_names, fontsize=10, fontweight='semibold')
    ax2.set_ylabel("Total Cumulative Sales ($K)", fontsize=10, color=TEXT_MUTED)
    ax2.grid(axis='y', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(CARD_BORDER)
    ax2.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bars_m:
        h = r.get_height()
        if h > 250:
            ax2.annotate(f"${h:,.0f}K", (r.get_x() + r.get_width()/2, h), xytext=(0, 4),
                         textcoords="offset points", ha='center', fontsize=9.2, color=ACCENT_CYAN, fontweight='bold')
    
    ax2.text(0.04, 0.86, "Q4 generates 33.2% of total annual revenue\n(Nov & Dec are prime retail peaks)",
             transform=ax2.transAxes, fontsize=9.5, color=TEXT_MUTED,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#1E293B', edgecolor=CARD_BORDER))

    # Bottom Right: Logistics Fulfillment
    ax3 = fig.add_axes([0.53, 0.06, 0.43, 0.33], facecolor=CARD_BG)
    ax3.set_title("Logistics Fulfillment: Ship Mode Revenue Share & Average Delivery Speed",
                  fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    ship = df.groupby('Ship Mode').agg({'Sales': 'sum', 'Profit': 'sum', 'Shipping Days': 'mean'}).sort_values(by='Sales', ascending=False)
    spos = np.arange(len(ship))
    
    ax3.bar(spos, ship['Sales']/1000, width=0.45, color=ACCENT_PURPLE, alpha=0.85, label='Sales ($K)')
    ax3.set_xticks(spos)
    ax3.set_xticklabels(ship.index, fontsize=10, fontweight='semibold')
    ax3.set_ylabel("Total Sales ($K)", fontsize=10, color=TEXT_MUTED)
    ax3.grid(axis='y', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color(CARD_BORDER)
    ax3.spines['bottom'].set_color(CARD_BORDER)
    ax3.set_ylim(0, 1600)
    
    ax3_twin = ax3.twinx()
    ax3_twin.plot(spos, ship['Shipping Days'], color=ACCENT_AMBER, marker='s', linewidth=2.5, markersize=8, label='Avg Days to Ship')
    ax3_twin.set_ylabel("Avg Shipping Days", fontsize=10, color=ACCENT_AMBER)
    ax3_twin.set_ylim(0, 7)
    ax3_twin.spines['top'].set_visible(False)
    ax3_twin.spines['left'].set_visible(False)
    ax3_twin.spines['right'].set_color(CARD_BORDER)
    
    for i, d in enumerate(ship['Shipping Days']):
        ax3_twin.annotate(f"{d:.1f} days", (i, d), xytext=(0, 7), textcoords="offset points",
                          ha='center', fontsize=9.5, color=ACCENT_AMBER, fontweight='bold')
        
    lines, labels = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines + lines2, labels + labels2, loc='upper right', frameon=False, fontsize=9.2)

    out_path = 'screenshots/sales_story.png'
    plt.savefig(out_path, dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.savefig('dashboard/dashboard_screenshots/02_sales_profit_story.png', dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# DASHBOARD 3: PRODUCT & CATEGORY ANALYSIS
# ==============================================================================
def create_product_analysis_dashboard(df):
    fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG_COLOR, dpi=150)
    draw_header(fig, "Act 2: Category Dynamics & Product Drivers",
                "Unveiling what drives revenue versus what captures margin. Diagnosing product champions and unprofitable volume.")

    # Left: Full Sub-Category Profitability Ranked
    ax1 = fig.add_axes([0.04, 0.07, 0.43, 0.77], facecolor=CARD_BG)
    ax1.set_title("Sub-Category Net Profit Ranking: 14 Profitable vs 3 Deficit Categories",
                  fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    sub_prof = df.groupby(['Sub-Category', 'Category'])['Profit'].sum().reset_index().sort_values(by='Profit', ascending=True)
    y_pos = np.arange(len(sub_prof))
    bar_colors = [ACCENT_RED if p < 0 else (ACCENT_GREEN if p > 30000 else ACCENT_CYAN) for p in sub_prof['Profit']]
    
    bars = ax1.barh(y_pos, sub_prof['Profit']/1000, height=0.6, color=bar_colors, alpha=0.9)
    ax1.axvline(0, color=TEXT_MUTED, linestyle='-', linewidth=1.2)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(sub_prof['Sub-Category'], fontsize=10, fontweight='semibold')
    ax1.set_xlabel("Net Profit ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax1.grid(axis='x', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(CARD_BORDER)
    ax1.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bars:
        w_val = r.get_width()
        pos = w_val + 1.2 if w_val >= 0 else w_val - 1.2
        ha = 'left' if w_val >= 0 else 'right'
        col = ACCENT_GREEN if w_val > 30 else (ACCENT_RED if w_val < 0 else TEXT_MAIN)
        ax1.annotate(f"${w_val:,.1f}K", (pos, r.get_y() + r.get_height()/2),
                     ha=ha, va='center', fontsize=9.2, color=col, fontweight='bold')
    ax1.set_xlim(-25, 65)

    # Top Right: Sales vs Profit Scatter Matrix
    ax2 = fig.add_axes([0.53, 0.50, 0.43, 0.34], facecolor=CARD_BG)
    ax2.set_title("Sub-Category Margin Efficiency Matrix: Sales Volume vs Profit Realization",
                  fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    scatter_data = df.groupby(['Sub-Category', 'Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    cat_palette = {'Technology': ACCENT_CYAN, 'Office Supplies': ACCENT_GREEN, 'Furniture': ACCENT_AMBER}
    for cat in ['Technology', 'Office Supplies', 'Furniture']:
        sub = scatter_data[scatter_data['Category'] == cat]
        ax2.scatter(sub['Sales']/1000, sub['Profit']/1000,
                    s=sub['Quantity']/12, label=cat, color=cat_palette[cat], alpha=0.8, edgecolors='white', linewidth=1)
    
    for _, row in scatter_data.iterrows():
        name = row['Sub-Category']
        if name in ['Copiers', 'Phones', 'Tables', 'Binders', 'Paper', 'Chairs', 'Machines']:
            col = ACCENT_RED if row['Profit'] < 0 else TEXT_MAIN
            ax2.annotate(name, (row['Sales']/1000, row['Profit']/1000), xytext=(5, 5), textcoords='offset points',
                         fontsize=9, color=col, fontweight='bold')

    ax2.axhline(0, color=ACCENT_RED, linestyle='--', alpha=0.6)
    ax2.set_xlabel("Sales Volume ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax2.set_ylabel("Net Profit ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax2.grid(color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax2.legend(loc='upper left', frameon=False, fontsize=9.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(CARD_BORDER)
    ax2.spines['bottom'].set_color(CARD_BORDER)

    # Bottom Right: Top 5 Highest Profit Products
    ax3 = fig.add_axes([0.53, 0.07, 0.43, 0.33], facecolor=CARD_BG)
    ax3.set_title("Product Champions: Top 5 Highest Net Profit Contributors",
                  fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    top_prods = df.groupby(['Product Name', 'Category'])['Profit'].sum().sort_values(ascending=True).tail(5)
    clean_names = [name[:30] + "..." if len(name) > 30 else name for name in top_prods.index.get_level_values(0)]
    
    y_p = np.arange(len(top_prods))
    bars_p = ax3.barh(y_p, top_prods.values/1000, height=0.55, color=ACCENT_GREEN, alpha=0.9)
    ax3.set_yticks(y_p)
    ax3.set_yticklabels(clean_names, fontsize=9.5, fontweight='semibold')
    ax3.set_xlabel("Net Profit ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax3.grid(axis='x', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color(CARD_BORDER)
    ax3.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bars_p:
        w_val = r.get_width()
        ax3.annotate(f" ${w_val:,.1f}K", (w_val, r.get_y() + r.get_height()/2),
                     ha='left', va='center', fontsize=9.2, color=ACCENT_GREEN, fontweight='bold')
    ax3.set_xlim(0, 30)

    out_path = 'screenshots/product_analysis.png'
    plt.savefig(out_path, dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.savefig('dashboard/dashboard_screenshots/03_category_product_drivers.png', dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# DASHBOARD 4: OPPORTUNITY RADAR & STRATEGIC PLAYBOOK
# ==============================================================================
def create_opportunity_analysis_dashboard(df):
    fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG_COLOR, dpi=150)
    draw_header(fig, "Act 3 & 4: Strategic Opportunity Matrix & Profit Protection",
                "Identifying high-sales/low-margin leaks, unlocking high-margin hidden gems, and curtailing value-destroying discounts.")

    # Panel 1 (Top Left): 4-Quadrant Strategic Opportunity Radar
    ax1 = fig.add_axes([0.04, 0.49, 0.43, 0.35], facecolor=CARD_BG)
    ax1.set_title("The Opportunity Radar: Sub-Category Strategic Quadrant Matrix",
                  fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    subcats = df.groupby('Sub-Category').agg({'Sales': 'sum', 'Profit': 'sum', 'Discount': 'mean'}).reset_index()
    sales_mid = subcats['Sales'].median() / 1000
    profit_mid = subcats['Profit'].median() / 1000
    
    ax1.axvline(sales_mid, color=CARD_BORDER, linestyle='--', lw=1.5)
    ax1.axhline(profit_mid, color=CARD_BORDER, linestyle='--', lw=1.5)
    
    ax1.set_xlim(-10, 360)
    ax1.set_ylim(-25, 65)

    ax1.text(0.96, 0.94, "CROWN JEWELS\n(High Sales, High Profit)\n-> Scale & Protect",
             transform=ax1.transAxes, ha='right', va='top', fontsize=8.8, color=ACCENT_CYAN, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#16253B', edgecolor=ACCENT_CYAN, alpha=0.8))
    
    ax1.text(0.04, 0.94, "HIDDEN GEMS\n(Low Sales, High Margin)\n-> Cross-Sell & Expand",
             transform=ax1.transAxes, ha='left', va='top', fontsize=8.8, color=ACCENT_GREEN, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#16382B', edgecolor=ACCENT_GREEN, alpha=0.8))
    
    ax1.text(0.96, 0.06, "PROFIT DRAINS / RISKS\n(High Sales, Low/Neg Profit)\n-> Renegotiate & Fix",
             transform=ax1.transAxes, ha='right', va='bottom', fontsize=8.8, color=ACCENT_RED, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#3B1A1E', edgecolor=ACCENT_RED, alpha=0.8))

    ax1.text(0.04, 0.06, "RATIONALIZE\n(Low Sales, Low Profit)\n-> Streamline Inventory",
             transform=ax1.transAxes, ha='left', va='bottom', fontsize=8.8, color=TEXT_MUTED, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor=CARD_BORDER, alpha=0.8))

    offsets = {
        'Copiers': (6, 2), 'Phones': (-45, -8), 'Accessories': (6, 2),
        'Paper': (6, 2), 'Binders': (6, 2), 'Chairs': (6, -10),
        'Storage': (6, 2), 'Appliances': (6, 2), 'Furnishings': (6, -10),
        'Envelopes': (6, 2), 'Art': (6, -8), 'Labels': (6, 4),
        'Machines': (6, 2), 'Fasteners': (6, -8), 'Supplies': (6, 2),
        'Bookcases': (6, 2), 'Tables': (6, 2)
    }

    for _, row in subcats.iterrows():
        s = row['Sales'] / 1000
        p = row['Profit'] / 1000
        color = ACCENT_RED if p < 0 else (ACCENT_GREEN if p > 30 else ACCENT_BLUE)
        ax1.scatter(s, p, color=color, s=75, edgecolors='white', linewidth=1, zorder=5)
        name = row['Sub-Category']
        off = offsets.get(name, (4, 4))
        ax1.annotate(name, (s, p), xytext=off, textcoords='offset points',
                     fontsize=8.5, color=TEXT_MAIN, fontweight='semibold')

    ax1.set_xlabel("Sales Volume ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax1.set_ylabel("Net Profit ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax1.grid(color=CARD_BORDER, linestyle=':', alpha=0.6)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(CARD_BORDER)
    ax1.spines['bottom'].set_color(CARD_BORDER)

    # Panel 2 (Top Right): Discount Destruction Curve
    ax2 = fig.add_axes([0.53, 0.49, 0.43, 0.35], facecolor=CARD_BG)
    ax2.set_title("The Discount Destruction Curve: Profit Margin Inversion Above 20% Discount",
                  fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    df['Discount Bracket'] = pd.cut(
        df['Discount'],
        bins=[-0.01, 0.0, 0.15, 0.30, 0.50, 1.0],
        labels=['0%\n(No Disc)', '1-15%\n(Low)', '16-30%\n(Moderate)', '31-50%\n(High)', '51-80%\n(Deep)']
    )
    disc_grp = df.groupby('Discount Bracket', observed=False).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    disc_grp['Margin %'] = (disc_grp['Profit'] / disc_grp['Sales']) * 100
    
    x_pos = np.arange(len(disc_grp))
    bar_cols = [ACCENT_GREEN if m > 15 else (ACCENT_CYAN if m > 0 else ACCENT_RED) for m in disc_grp['Margin %']]
    
    bars_d = ax2.bar(x_pos, disc_grp['Margin %'], width=0.5, color=bar_cols, alpha=0.9)
    ax2.axhline(0, color=TEXT_MUTED, linestyle='-', linewidth=1.2)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(disc_grp['Discount Bracket'], fontsize=9.5, fontweight='semibold')
    ax2.set_ylabel("Profit Margin %", fontsize=10, color=TEXT_MUTED)
    ax2.grid(axis='y', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(CARD_BORDER)
    ax2.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bars_d:
        h = r.get_height()
        va = 'bottom' if h >= 0 else 'top'
        y_offset = 3 if h >= 0 else -6
        col = ACCENT_GREEN if h >= 0 else ACCENT_RED
        ax2.annotate(f"{h:+.1f}%", (r.get_x() + r.get_width()/2, h), xytext=(0, y_offset),
                     textcoords="offset points", ha='center', va=va, fontsize=9.5, color=col, fontweight='bold')
        
    ax2.text(0.96, 0.90, "CRITICAL FINDING:\nDiscounts > 30% eroded -$125,007 in capital\nTurning volume growth into steep enterprise loss.",
             transform=ax2.transAxes, ha='right', va='top', fontsize=9, color=ACCENT_RED,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#2A1518', edgecolor=ACCENT_RED))

    # Panel 3 (Bottom Left): Geographic Polarization
    ax3 = fig.add_axes([0.04, 0.06, 0.43, 0.33], facecolor=CARD_BG)
    ax3.set_title("Geographic Polarization: Margin Champions (CA, NY) vs Capital Leaks (TX, OH)",
                  fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    state_perf = df.groupby('State')['Profit'].sum()
    geo_focus = pd.concat([state_perf.sort_values().head(4), state_perf.sort_values().tail(4)])
    y_geo = np.arange(len(geo_focus))
    cols_geo = [ACCENT_RED if v < 0 else ACCENT_GREEN for v in geo_focus.values]
    
    bars_g = ax3.barh(y_geo, geo_focus.values/1000, height=0.55, color=cols_geo, alpha=0.9)
    ax3.axvline(0, color=TEXT_MUTED, linestyle='-', linewidth=1.2)
    ax3.set_yticks(y_geo)
    ax3.set_yticklabels(geo_focus.index, fontsize=10, fontweight='semibold')
    ax3.set_xlabel("Net Profit / Loss ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax3.grid(axis='x', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color(CARD_BORDER)
    ax3.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bars_g:
        w_val = r.get_width()
        pos = w_val + 2 if w_val >= 0 else w_val - 2
        ha = 'left' if w_val >= 0 else 'right'
        col = ACCENT_GREEN if w_val >= 0 else ACCENT_RED
        ax3.annotate(f"${w_val:,.1f}K", (pos, r.get_y() + r.get_height()/2),
                     ha=ha, va='center', fontsize=9.2, color=col, fontweight='bold')
    ax3.set_xlim(-35, 95)

    # Panel 4 (Bottom Right): Strategic Executive Action Matrix
    ax4 = fig.add_axes([0.53, 0.06, 0.43, 0.33], facecolor=CARD_BG)
    ax4.axis('off')
    ax4.set_title("Executive Action Matrix: 4 Immediate Business Interventions",
                  fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    actions = [
        ("1. Cap Promotional Discounts at 20%",
         "Discounts over 30% yield severe negative margins (-24.8% to -119.2%). Enforce automated discount approval gates.", ACCENT_RED),
        ("2. Restructure Furniture Category (Tables & Bookcases)",
         r"Tables generated -\$17.7K net loss on \$207K revenue. Transition to made-to-order fulfillment and renegotiate freight.", ACCENT_AMBER),
        ("3. Scale High-Margin Technology 'Crown Jewels'",
         "Copiers deliver 37.2% margin and $55.6K profit. Bundle copiers with Accessories and Paper to maximize basket profit.", ACCENT_GREEN),
        ("4. Re-engineer Regional Discounting in Central & Texas",
         "Texas accounts for -$25.7K loss due to unmanaged 37% average discounting. Eliminate margin-diluting contract terms.", ACCENT_CYAN),
    ]
    
    for idx, (head, desc, clr) in enumerate(actions):
        y_box = 0.76 - idx * 0.245
        rect = patches.FancyBboxPatch((0.0, y_box), 0.98, 0.205, boxstyle="round,pad=0.01",
                                      facecolor='#1E293B', edgecolor=clr, lw=1.2, transform=ax4.transAxes)
        ax4.add_patch(rect)
        ax4.text(0.03, y_box + 0.14, head, transform=ax4.transAxes, fontsize=10, fontweight='bold', color=clr)
        ax4.text(0.03, y_box + 0.045, desc, transform=ax4.transAxes, fontsize=8.8, color=TEXT_MUTED)

    out_path = 'screenshots/opportunity_analysis.png'
    plt.savefig(out_path, dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.savefig('dashboard/dashboard_screenshots/06_opportunity_radar.png', dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# SUB-DASHBOARD 04: GEOGRAPHIC EXPANSION DEEP DIVE
# ==============================================================================
def create_geographic_dashboard(df):
    fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG_COLOR, dpi=150)
    draw_header(fig, "Geographic Expansion & Regional Profitability",
                "Evaluating multi-state market penetration, regional margin variations, and identifying localized discounting leaks.")

    # Regional Comparison
    ax1 = fig.add_axes([0.04, 0.50, 0.43, 0.34], facecolor=CARD_BG)
    ax1.set_title("Regional Revenue & Profit Contribution by Territory", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    reg_summary = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum', 'Discount': 'mean'}).sort_values(by='Sales', ascending=False)
    x = np.arange(len(reg_summary))
    w = 0.35
    
    ax1.bar(x - w/2, reg_summary['Sales']/1000, w, label='Sales ($K)', color=ACCENT_BLUE, alpha=0.9)
    ax1.bar(x + w/2, reg_summary['Profit']/1000, w, label='Profit ($K)', color=ACCENT_GREEN, alpha=0.9)
    ax1.set_xticks(x)
    ax1.set_xticklabels(reg_summary.index, fontsize=10.5, fontweight='semibold')
    ax1.set_ylabel("Amount ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax1.grid(axis='y', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax1.legend(loc='upper right', frameon=False, fontsize=9.5)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(CARD_BORDER)
    ax1.spines['bottom'].set_color(CARD_BORDER)

    # Top 10 States by Sales
    ax2 = fig.add_axes([0.53, 0.07, 0.43, 0.77], facecolor=CARD_BG)
    ax2.set_title("Top 10 States by Sales Volume & Resulting Net Margin", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    top_states = df.groupby('State').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values(by='Sales', ascending=True).tail(10)
    y_pos = np.arange(len(top_states))
    
    bars_s = ax2.barh(y_pos, top_states['Sales']/1000, height=0.6, color=ACCENT_BLUE, alpha=0.85, label='Sales ($K)')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(top_states.index, fontsize=10, fontweight='semibold')
    ax2.set_xlabel("Sales ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax2.grid(axis='x', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(CARD_BORDER)
    ax2.spines['bottom'].set_color(CARD_BORDER)
    
    for idx, r in enumerate(bars_s):
        s_val = r.get_width()
        p_val = top_states['Profit'].iloc[idx] / 1000
        p_col = ACCENT_RED if p_val < 0 else ACCENT_GREEN
        ax2.annotate(f"Sales: ${s_val:,.0f}K  |  Profit: ${p_val:+,.1f}K", (s_val + 5, r.get_y() + r.get_height()/2),
                     ha='left', va='center', fontsize=9.2, color=p_col, fontweight='bold')
    ax2.set_xlim(0, 580)

    # State Discount vs Profit Relationship
    ax3 = fig.add_axes([0.04, 0.07, 0.43, 0.33], facecolor=CARD_BG)
    ax3.set_title("The Discount Penalty: State Average Discount % vs Net Profit Margin %", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    state_corr = df.groupby('State').agg({'Sales': 'sum', 'Profit': 'sum', 'Discount': 'mean'}).reset_index()
    state_corr['Margin %'] = (state_corr['Profit'] / state_corr['Sales']) * 100
    state_corr['Avg Discount %'] = state_corr['Discount'] * 100
    
    ax3.scatter(state_corr['Avg Discount %'], state_corr['Margin %'], color=ACCENT_CYAN, s=state_corr['Sales']/1000 + 40, alpha=0.8, edgecolors='white', lw=1)
    ax3.axhline(0, color=ACCENT_RED, linestyle='--', alpha=0.7)
    
    state_offsets = {
        'California': (8, -6), 'New York': (8, 6), 'Washington': (8, 6),
        'Texas': (8, -4), 'Illinois': (8, -4), 'Ohio': (8, -8), 'Pennsylvania': (8, 4)
    }
    for _, r in state_corr[state_corr['State'].isin(state_offsets.keys())].iterrows():
        col = ACCENT_RED if r['Margin %'] < 0 else ACCENT_GREEN
        off = state_offsets.get(r['State'], (6, 6))
        ax3.annotate(r['State'], (r['Avg Discount %'], r['Margin %']), xytext=off, textcoords='offset points',
                     fontsize=9, color=col, fontweight='bold')
        
    ax3.set_xlabel("Average State Discount %", fontsize=10, color=TEXT_MUTED)
    ax3.set_ylabel("Profit Margin %", fontsize=10, color=TEXT_MUTED)
    ax3.grid(color=CARD_BORDER, linestyle=':', alpha=0.6)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color(CARD_BORDER)
    ax3.spines['bottom'].set_color(CARD_BORDER)

    out_path = 'dashboard/dashboard_screenshots/04_geographic_expansion.png'
    plt.savefig(out_path, dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# SUB-DASHBOARD 05: CUSTOMER DEEP DIVE
# ==============================================================================
def create_customer_dashboard(df):
    fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG_COLOR, dpi=150)
    draw_header(fig, "Customer Economics & Segment Value Distribution",
                "Analyzing Customer Lifetime Value (CLV), segment contribution, and identifying high-revenue unprofitable accounts.")

    # Top Left: Segment Performance
    ax1 = fig.add_axes([0.04, 0.50, 0.43, 0.34], facecolor=CARD_BG)
    ax1.set_title("Customer Segment Revenue & Profit Distribution", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    seg = df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values(by='Sales', ascending=False)
    s_pos = np.arange(len(seg))
    w = 0.35
    
    ax1.bar(s_pos - w/2, seg['Sales']/1000, w, label='Sales ($K)', color=ACCENT_BLUE, alpha=0.9)
    ax1.bar(s_pos + w/2, seg['Profit']/1000, w, label='Profit ($K)', color=ACCENT_GREEN, alpha=0.9)
    ax1.set_xticks(s_pos)
    ax1.set_xticklabels(seg.index, fontsize=10.5, fontweight='semibold')
    ax1.set_ylabel("Amount ($ Thousands)", fontsize=10, color=TEXT_MUTED)
    ax1.grid(axis='y', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax1.legend(loc='upper right', frameon=False, fontsize=9.5)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(CARD_BORDER)
    ax1.spines['bottom'].set_color(CARD_BORDER)
    
    for idx, v in enumerate(seg['Sales']/1000):
        m = (seg['Profit'].iloc[idx] / seg['Sales'].iloc[idx]) * 100
        ax1.annotate(f"Margin: {m:.1f}%", (idx, seg['Sales'].iloc[idx]/1000), xytext=(0, 6),
                     textcoords="offset points", ha='center', fontsize=9.5, color=ACCENT_CYAN, fontweight='bold')

    # Top Right: Top 5 Customers by Profit
    ax2 = fig.add_axes([0.56, 0.50, 0.40, 0.34], facecolor=CARD_BG)
    ax2.set_title("Top 5 Most Profitable Customer Accounts (Champions)", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    top_cust = df.groupby('Customer Name').agg({'Sales': 'sum', 'Profit': 'sum', 'Order ID': 'nunique'}).sort_values(by='Profit', ascending=True).tail(5)
    y_c = np.arange(len(top_cust))
    
    bars_c = ax2.barh(y_c, top_cust['Profit'], height=0.5, color=ACCENT_GREEN, alpha=0.9)
    ax2.set_yticks(y_c)
    ax2.set_yticklabels(top_cust.index, fontsize=10, fontweight='semibold')
    ax2.set_xlabel("Net Profit ($)", fontsize=10, color=TEXT_MUTED)
    ax2.grid(axis='x', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(CARD_BORDER)
    ax2.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bars_c:
        w_val = r.get_width()
        ax2.annotate(f" ${w_val:,.0f}", (w_val + 120, r.get_y() + r.get_height()/2),
                     ha='left', va='center', fontsize=9.5, color=ACCENT_GREEN, fontweight='bold')
    ax2.set_xlim(0, 11000)

    # Bottom Right: Top 5 Unprofitable Customers
    ax3 = fig.add_axes([0.56, 0.07, 0.40, 0.33], facecolor=CARD_BG)
    ax3.set_title("Top 5 Loss-Generating Customer Accounts (Immediate Review)", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    worst_cust = df.groupby('Customer Name').agg({'Sales': 'sum', 'Profit': 'sum', 'Order ID': 'nunique'}).sort_values(by='Profit', ascending=True).head(5)
    y_w = np.arange(len(worst_cust))
    
    bars_w = ax3.barh(y_w, worst_cust['Profit'], height=0.5, color=ACCENT_RED, alpha=0.9)
    ax3.set_yticks(y_w)
    ax3.set_yticklabels(worst_cust.index, fontsize=10, fontweight='semibold')
    ax3.set_xlabel("Net Loss ($)", fontsize=10, color=TEXT_MUTED)
    ax3.grid(axis='x', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color(CARD_BORDER)
    ax3.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bars_w:
        w_val = r.get_width()
        ax3.annotate(f" ${w_val:,.0f}", (w_val - 120, r.get_y() + r.get_height()/2),
                     ha='right', va='center', fontsize=9.5, color=ACCENT_RED, fontweight='bold')
    ax3.set_xlim(-8500, 0)

    # Bottom Left: Order Frequency Distribution
    ax4 = fig.add_axes([0.04, 0.07, 0.43, 0.33], facecolor=CARD_BG)
    ax4.set_title("Customer Order Frequency Distribution (Repeat Purchase Power)", fontsize=12.5, fontweight='bold', color=TEXT_MAIN, pad=12, loc='left')
    
    orders_per_cust = df.groupby('Customer ID')['Order ID'].nunique()
    bins = [0, 2, 5, 8, 12, 20]
    labels = ['1-2 Orders\n(New/One-off)', '3-5 Orders\n(Occasional)', '6-8 Orders\n(Regular)', '9-12 Orders\n(Loyal)', '13+ Orders\n(VIPs)']
    order_brackets = pd.cut(orders_per_cust, bins=bins, labels=labels)
    counts = order_brackets.value_counts().sort_index()
    
    bars_o = ax4.bar(range(len(counts)), counts.values, color=ACCENT_PURPLE, width=0.55, alpha=0.85)
    ax4.set_xticks(range(len(counts)))
    ax4.set_xticklabels(counts.index, fontsize=9.5, fontweight='semibold')
    ax4.set_ylabel("Number of Customers", fontsize=10, color=TEXT_MUTED)
    ax4.grid(axis='y', color=CARD_BORDER, linestyle='--', alpha=0.7)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.spines['left'].set_color(CARD_BORDER)
    ax4.spines['bottom'].set_color(CARD_BORDER)
    
    for r in bars_o:
        h = r.get_height()
        ax4.annotate(f"{h}", (r.get_x() + r.get_width()/2, h), xytext=(0, 4),
                     textcoords="offset points", ha='center', fontsize=9.5, color=TEXT_MAIN, fontweight='bold')

    out_path = 'dashboard/dashboard_screenshots/05_customer_deep_dive.png'
    plt.savefig(out_path, dpi=150, facecolor=BG_COLOR, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

def main():
    print("=" * 60)
    print("RE-GENERATING POLISHED SUPERSCOPE VISUAL DASHBOARDS")
    print("=" * 60)
    df = load_data()
    
    create_executive_dashboard(df)
    create_sales_story_dashboard(df)
    create_product_analysis_dashboard(df)
    create_opportunity_analysis_dashboard(df)
    create_geographic_dashboard(df)
    create_customer_dashboard(df)
    print("All dashboards re-rendered with pixel-perfect layouts!")

if __name__ == '__main__':
    main()
