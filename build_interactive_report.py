"""
SUPERSCOPE Interactive BI Web Report Generator
Builds a standalone, responsive, interactive single-file executive dashboard.
Elevate Labs Data Analyst Internship - Task 2: Data Visualization and Storytelling
"""

import json
import pandas as pd
import numpy as np

def generate_interactive_report():
    df = pd.read_csv('data/cleaned/Superstore_Cleaned.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    # Precompute summary data
    total_sales = float(df['Sales'].sum())
    total_profit = float(df['Profit'].sum())
    total_orders = int(df['Order ID'].nunique())
    total_customers = int(df['Customer ID'].nunique())
    avg_order_value = total_sales / total_orders
    profit_margin = (total_profit / total_sales) * 100
    burn_over_30 = float(df[df['Discount'] > 0.30]['Profit'].sum())
    
    # Yearly data
    yearly = df.groupby('Order Year').agg({'Sales': 'sum', 'Profit': 'sum', 'Order ID': 'nunique'}).reset_index()
    yearly_data = {
        'years': yearly['Order Year'].tolist(),
        'sales': [round(x, 2) for x in yearly['Sales']],
        'profit': [round(x, 2) for x in yearly['Profit']],
        'orders': yearly['Order ID'].tolist()
    }
    
    # Monthly time series
    monthly = df.set_index('Order Date').resample('ME').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly_data = {
        'labels': monthly['Order Date'].dt.strftime('%b %Y').tolist(),
        'sales': [round(x, 2) for x in monthly['Sales']],
        'profit': [round(x, 2) for x in monthly['Profit']]
    }
    
    # Category summary
    cat = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum', 'Quantity': 'sum'}).reset_index()
    cat_data = {
        'categories': cat['Category'].tolist(),
        'sales': [round(x, 2) for x in cat['Sales']],
        'profit': [round(x, 2) for x in cat['Profit']],
        'margin': [round((p/s)*100, 2) for p, s in zip(cat['Profit'], cat['Sales'])]
    }
    
    # Sub-Category summary
    subcat = df.groupby(['Sub-Category', 'Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Discount': 'mean'
    }).reset_index().sort_values(by='Profit', ascending=False)
    
    subcat_data = []
    for _, r in subcat.iterrows():
        subcat_data.append({
            'name': r['Sub-Category'],
            'category': r['Category'],
            'sales': round(r['Sales'], 2),
            'profit': round(r['Profit'], 2),
            'margin': round((r['Profit']/r['Sales'])*100, 2),
            'discount': round(r['Discount']*100, 2),
            'quantity': int(r['Quantity'])
        })
        
    # Regional summary
    reg = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum', 'Discount': 'mean'}).reset_index()
    reg_data = {
        'regions': reg['Region'].tolist(),
        'sales': [round(x, 2) for x in reg['Sales']],
        'profit': [round(x, 2) for x in reg['Profit']],
        'discount': [round(x*100, 2) for x in reg['Discount']],
        'margin': [round((p/s)*100, 2) for p, s in zip(reg['Profit'], reg['Sales'])]
    }
    
    # State summary
    state = df.groupby('State').agg({'Sales': 'sum', 'Profit': 'sum', 'Discount': 'mean'}).reset_index()
    state_top_profit = state.sort_values(by='Profit', ascending=False).head(5)
    state_loss = state.sort_values(by='Profit', ascending=True).head(5)
    
    state_data = {
        'top_states': state_top_profit['State'].tolist(),
        'top_profit': [round(x, 2) for x in state_top_profit['Profit']],
        'top_sales': [round(x, 2) for x in state_top_profit['Sales']],
        'loss_states': state_loss['State'].tolist(),
        'loss_profit': [round(x, 2) for x in state_loss['Profit']],
        'loss_sales': [round(x, 2) for x in state_loss['Sales']]
    }
    
    # Discount brackets
    df['Discount Bracket'] = pd.cut(
        df['Discount'],
        bins=[-0.01, 0.0, 0.15, 0.30, 0.50, 1.0],
        labels=['0% (No Discount)', '1-15% (Low)', '16-30% (Moderate)', '31-50% (High)', '51-80% (Deep)']
    )
    disc_grp = df.groupby('Discount Bracket', observed=False).agg({'Sales': 'sum', 'Profit': 'sum', 'Order ID': 'nunique'}).reset_index()
    disc_data = {
        'brackets': disc_grp['Discount Bracket'].tolist(),
        'sales': [round(x, 2) for x in disc_grp['Sales']],
        'profit': [round(x, 2) for x in disc_grp['Profit']],
        'orders': disc_grp['Order ID'].tolist(),
        'margin': [round((p/s)*100, 2) for p, s in zip(disc_grp['Profit'], disc_grp['Sales'])]
    }
    
    # Top Products
    prod = df.groupby(['Product Name', 'Category']).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    top_prod = prod.sort_values(by='Profit', ascending=False).head(5)
    loss_prod = prod.sort_values(by='Profit', ascending=True).head(5)
    
    prod_data = {
        'top_names': [n[:32] + "..." if len(n) > 32 else n for n in top_prod['Product Name']],
        'top_profit': [round(x, 2) for x in top_prod['Profit']],
        'loss_names': [n[:32] + "..." if len(n) > 32 else n for n in loss_prod['Product Name']],
        'loss_profit': [round(x, 2) for x in loss_prod['Profit']]
    }
    
    # Pre-render raw HTML template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SUPERSCOPE — Retail Intelligence & Sales Story</title>
    <!-- Chart.js for responsive client-side visual interactions -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <style>
        :root {{
            --bg-main: #0A0E1A;
            --bg-card: #131B2E;
            --bg-card-hover: #1A253D;
            --border: #22304A;
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --accent-cyan: #06B6D4;
            --accent-blue: #0EA5E9;
            --accent-green: #10B981;
            --accent-amber: #F59E0B;
            --accent-red: #EF4444;
            --accent-purple: #8B5CF6;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}
        body {{
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.5;
            padding: 24px;
        }}
        /* Header Banner */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .brand-title {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .logo-text {{
            font-size: 28px;
            font-weight: 800;
            color: var(--accent-cyan);
            letter-spacing: -0.5px;
        }}
        .brand-sub {{
            font-size: 20px;
            font-weight: 700;
            color: var(--text-main);
        }}
        .tagline {{
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 4px;
        }}
        .header-badges {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .badge {{
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border: 1px solid var(--accent-blue);
            background: rgba(14, 165, 233, 0.1);
            color: var(--accent-blue);
        }}
        .btn-print {{
            padding: 8px 18px;
            background: #1E293B;
            border: 1px solid var(--border);
            color: var(--text-main);
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-print:hover {{
            background: var(--accent-blue);
            border-color: var(--accent-blue);
        }}
        /* KPI Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 20px;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-blue);
        }}
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }}
        .kpi-blue::before {{ background: var(--accent-blue); }}
        .kpi-green::before {{ background: var(--accent-green); }}
        .kpi-purple::before {{ background: var(--accent-purple); }}
        .kpi-amber::before {{ background: var(--accent-amber); }}
        .kpi-red::before {{ background: var(--accent-red); }}
        .kpi-title {{
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        .kpi-value {{
            font-size: 26px;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 4px;
        }}
        .kpi-sub {{
            font-size: 12px;
            font-weight: 600;
        }}
        .sub-blue {{ color: var(--accent-blue); }}
        .sub-green {{ color: var(--accent-green); }}
        .sub-purple {{ color: var(--accent-purple); }}
        .sub-amber {{ color: var(--accent-amber); }}
        .sub-red {{ color: var(--accent-red); }}

        /* Tab Navigation */
        .tabs-nav {{
            display: flex;
            gap: 8px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 24px;
            overflow-x: auto;
            padding-bottom: 8px;
        }}
        .tab-btn {{
            padding: 10px 18px;
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 13.5px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}
        .tab-btn:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }}
        .tab-btn.active {{
            color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.12);
            border-bottom: 2px solid var(--accent-cyan);
        }}

        /* Tab Content Panes */
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}

        /* Chart Grid Layouts */
        .chart-grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}
        @media (max-width: 1024px) {{
            .chart-grid-2 {{
                grid-template-columns: 1fr;
            }}
        }}
        .chart-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }}
        .chart-title {{
            font-size: 15px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 6px;
        }}
        .chart-sub {{
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 16px;
        }}
        .canvas-container {{
            position: relative;
            width: 100%;
            height: 320px;
        }}

        /* Opportunity Matrix Quadrants */
        .quadrant-box {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
            margin-top: 16px;
        }}
        .q-card {{
            padding: 14px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.02);
        }}
        .q-title {{
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 4px;
        }}
        .q-desc {{
            font-size: 11.5px;
            color: var(--text-muted);
        }}

        /* Table Styling */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            margin-top: 12px;
        }}
        .data-table th {{
            text-align: left;
            padding: 10px 12px;
            background: #1A253D;
            color: var(--text-muted);
            font-weight: 700;
            border-bottom: 1px solid var(--border);
        }}
        .data-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .data-table tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}
        .positive {{ color: var(--accent-green); font-weight: 600; }}
        .negative {{ color: var(--accent-red); font-weight: 600; }}

        /* Executive Takeaways Accordion / Cards */
        .takeaway-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-left: 4px solid var(--accent-cyan);
            border-radius: 8px;
            padding: 18px 20px;
            margin-bottom: 14px;
        }}
        .takeaway-header {{
            font-size: 15px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .takeaway-body {{
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.6;
        }}
        .takeaway-flow {{
            display: flex;
            gap: 12px;
            margin-top: 10px;
            flex-wrap: wrap;
        }}
        .flow-pill {{
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 600;
        }}
        .pill-obs {{ background: rgba(14, 165, 233, 0.15); color: var(--accent-blue); }}
        .pill-why {{ background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }}
        .pill-act {{ background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }}

        @media print {{
            body {{ background: #FFFFFF; color: #000000; }}
            .btn-print, .tabs-nav {{ display: none; }}
            .kpi-card, .chart-card, .takeaway-card {{ border: 1px solid #CCCCCC; background: #FFFFFF; color: #000000; }}
            .tab-content {{ display: block !important; margin-bottom: 30px; }}
        }}
    </style>
</head>
<body>

    <!-- Header Section -->
    <header class="header">
        <div>
            <div class="brand-title">
                <span class="logo-text">SUPERSCOPE</span>
                <span class="brand-sub">| Retail Intelligence & Sales Story</span>
            </div>
            <p class="tagline">"From raw transactions to actionable business decisions." Enterprise Performance Ledger (2014 – 2017)</p>
        </div>
        <div class="header-badges">
            <span class="badge">9,994 Verified Orders</span>
            <span class="badge">4 US Geographic Territories</span>
            <button class="btn-print" onclick="window.print()">Export / Print PDF</button>
        </div>
    </header>

    <!-- Top Executive KPI Banner -->
    <section class="kpi-grid">
        <div class="kpi-card kpi-blue">
            <div class="kpi-title">Total Revenue</div>
            <div class="kpi-value">${total_sales:,.0f}</div>
            <div class="kpi-sub sub-blue">+20.4% YoY Growth (2017)</div>
        </div>
        <div class="kpi-card kpi-green">
            <div class="kpi-title">Total Net Profit</div>
            <div class="kpi-value">${total_profit:,.0f}</div>
            <div class="kpi-sub sub-green">{profit_margin:.2f}% Net Margin Realization</div>
        </div>
        <div class="kpi-card kpi-purple">
            <div class="kpi-title">Total Unique Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-sub sub-purple">{total_customers:,} Unique Enterprise Customers</div>
        </div>
        <div class="kpi-card kpi-amber">
            <div class="kpi-title">Average Order Value (AOV)</div>
            <div class="kpi-value">${avg_order_value:,.2f}</div>
            <div class="kpi-sub sub-amber">${total_profit/total_orders:,.2f} Net Profit / Order</div>
        </div>
        <div class="kpi-card kpi-red">
            <div class="kpi-title">Discount Capital Burn</div>
            <div class="kpi-value">-${abs(burn_over_30):,.0f}</div>
            <div class="kpi-sub sub-red">Eroded on Discounts > 30%</div>
        </div>
    </section>

    <!-- Storytelling Tab Navigation -->
    <nav class="tabs-nav">
        <button class="tab-btn active" onclick="switchTab('tab-exec')">1. Executive Snapshot</button>
        <button class="tab-btn" onclick="switchTab('tab-story')">2. Act 1: The Sales Trajectory</button>
        <button class="tab-btn" onclick="switchTab('tab-products')">3. Act 2: Category & Product Drivers</button>
        <button class="tab-btn" onclick="switchTab('tab-geo')">4. Act 3: Geographic Polarization</button>
        <button class="tab-btn" onclick="switchTab('tab-opp')">5. Act 4: Opportunity Radar & Discount Cliff</button>
        <button class="tab-btn" onclick="switchTab('tab-actions')">6. Executive Takeaways & Playbook</button>
    </nav>

    <!-- TAB 1: EXECUTIVE SNAPSHOT -->
    <div id="tab-exec" class="tab-content active">
        <div class="chart-grid-2">
            <div class="chart-card">
                <div class="chart-title">Annual Revenue & Net Profit Escalation (2014 – 2017)</div>
                <div class="chart-sub">Tracing enterprise growth from $484K (2014) to $733K (2017) run-rate.</div>
                <div class="canvas-container">
                    <canvas id="yearlyChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Category Revenue Contribution vs Profit Capture</div>
                <div class="chart-sub">Technology delivers 50.8% of profit; Furniture suffers an anemic 2.49% margin.</div>
                <div class="canvas-container">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="chart-card">
            <div class="chart-title">Multi-Year Enterprise Performance Summary</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Year</th>
                        <th>Gross Revenue</th>
                        <th>Net Profit</th>
                        <th>Orders</th>
                        <th>Net Margin (%)</th>
                        <th>Sales Growth (%)</th>
                        <th>Profit Growth (%)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>2014</td><td>$484,247.50</td><td class="positive">$49,543.97</td><td>969</td><td>10.23%</td><td>Baseline</td><td>Baseline</td></tr>
                    <tr><td>2015</td><td>$470,532.51</td><td class="positive">$61,618.60</td><td>1,038</td><td>13.10%</td><td>-2.83%</td><td class="positive">+24.37%</td></tr>
                    <tr><td>2016</td><td>$609,205.60</td><td class="positive">$81,795.17</td><td>1,315</td><td>13.43%</td><td class="positive">+29.47%</td><td class="positive">+32.74%</td></tr>
                    <tr><td>2017</td><td>$733,215.26</td><td class="positive">$93,439.27</td><td>1,687</td><td>12.74%</td><td class="positive">+20.36%</td><td class="positive">+14.24%</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 2: THE SALES STORY -->
    <div id="tab-story" class="tab-content">
        <div class="chart-card" style="margin-bottom: 20px;">
            <div class="chart-title">48-Month Chronological Trajectory & Seasonal Peaks (2014 – 2017)</div>
            <div class="chart-sub">All-time peak recorded in November 2017 ($97K sales). Consistent Q1 seasonal drops.</div>
            <div class="canvas-container" style="height: 380px;">
                <canvas id="monthlyChart"></canvas>
            </div>
        </div>
        <div class="chart-grid-2">
            <div class="chart-card">
                <div class="chart-title">Q4 Seasonality Revenue Spike (Calendar Month Concentration)</div>
                <div class="chart-sub">November and December generate over 33.2% of annual company revenue.</div>
                <div class="canvas-container">
                    <canvas id="seasonalityChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Fulfillment Economics by Shipping Mode</div>
                <div class="chart-sub">Standard Class carries 60% of volume (5.0 avg days delivery); Same Day achieves 0.0 days.</div>
                <div class="canvas-container">
                    <canvas id="shipChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 3: CATEGORY & PRODUCT DRIVERS -->
    <div id="tab-products" class="tab-content">
        <div class="chart-grid-2">
            <div class="chart-card">
                <div class="chart-title">Sub-Category Net Profit Ranking (14 Winners vs 3 Losers)</div>
                <div class="chart-sub">Copiers leads with $55.6K profit; Tables leaks -$17.7K due to severe freight & discounts.</div>
                <div class="canvas-container" style="height: 440px;">
                    <canvas id="subcatProfitChart"></canvas>
                </div>
            </div>
            <div>
                <div class="chart-card" style="margin-bottom: 20px;">
                    <div class="chart-title">Top 5 Product Profit Champions</div>
                    <div class="chart-sub">Led by Canon imageCLASS 2200 ($25,200 net profit).</div>
                    <div class="canvas-container" style="height: 190px;">
                        <canvas id="topProdChart"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">Top 5 Product Loss Bleeders</div>
                    <div class="chart-sub">Led by Cubify 3D Printer (-$8,880 loss due to 53% discount).</div>
                    <div class="canvas-container" style="height: 190px;">
                        <canvas id="lossProdChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 4: GEOGRAPHIC POLARIZATION -->
    <div id="tab-geo" class="tab-content">
        <div class="chart-grid-2">
            <div class="chart-card">
                <div class="chart-title">Regional Performance & Profit Margin Realization</div>
                <div class="chart-sub">West achieves 14.9% margin (10.9% discount); Central drops to 7.9% (24.0% discount).</div>
                <div class="canvas-container">
                    <canvas id="regionalChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <div class="chart-title">State-Level Profitability Polarization: Champions vs Bleeders</div>
                <div class="chart-sub">California (+76.4K) and New York (+74.0K) vs Texas (-$25.7K) and Ohio (-$17.0K).</div>
                <div class="canvas-container">
                    <canvas id="statePolarChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 5: OPPORTUNITY RADAR & DISCOUNT CLIFF -->
    <div id="tab-opp" class="tab-content">
        <div class="chart-grid-2">
            <div class="chart-card">
                <div class="chart-title">The Discount Destruction Curve: Profit Margin Inversion Above 20%</div>
                <div class="chart-sub">Full-price orders deliver +29.5% margin; discounts >50% collapse to -119.2% margin.</div>
                <div class="canvas-container">
                    <canvas id="discountCurveChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <div class="chart-title">Strategic Opportunity Radar: 4-Quadrant Sub-Category Matrix</div>
                <div class="chart-sub">Action roadmap for scaling champions and rationalizing loss-making inventory.</div>
                <div class="quadrant-box">
                    <div class="q-card" style="border-left: 4px solid var(--accent-cyan);">
                        <div class="q-title" style="color: var(--accent-cyan);">Crown Jewels (Scale & Protect)</div>
                        <div class="q-desc">Copiers ($55.6K), Phones ($44.5K), Accessories ($41.9K). High sales, stellar margins.</div>
                    </div>
                    <div class="q-card" style="border-left: 4px solid var(--accent-green);">
                        <div class="q-title" style="color: var(--accent-green);">Hidden Gems (Cross-Sell)</div>
                        <div class="q-desc">Paper (43.4% margin, $34.1K profit), Envelopes (42.3%), Labels (44.4%). Promote in checkout.</div>
                    </div>
                    <div class="q-card" style="border-left: 4px solid var(--accent-red);">
                        <div class="q-title" style="color: var(--accent-red);">Profit Drains (Renegotiate)</div>
                        <div class="q-desc">Tables (-$17.7K), Bookcases (-$3.5K), Machines. Bulky items with high discount exploitation.</div>
                    </div>
                    <div class="q-card" style="border-left: 4px solid var(--text-muted);">
                        <div class="q-title" style="color: var(--text-muted);">Question Marks (Rationalize)</div>
                        <div class="q-desc">Fasteners ($950 profit), Supplies (-$1.2K). Low velocity items to streamline.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 6: EXECUTIVE TAKEAWAYS -->
    <div id="tab-actions" class="tab-content">
        <div class="takeaway-card">
            <div class="takeaway-header">
                <span>1. Cap Promotional Discounts at 20% to Prevent $125K in Capital Dissipation</span>
            </div>
            <div class="takeaway-body">
                <div class="takeaway-flow">
                    <span class="flow-pill pill-obs">OBSERVATION: Orders discounted >30% generated -$125,007 in net losses across 965 transactions.</span>
                    <span class="flow-pill pill-why">WHY IT MATTERS: Sales reps discount to hit top-line targets, evaporating 43.6% of enterprise net profit.</span>
                    <span class="flow-pill pill-act">RECOMMENDED ACTION: Institute ERP discount authorization gates: >20% requires VP Finance approval.</span>
                </div>
            </div>
        </div>

        <div class="takeaway-card" style="border-left-color: var(--accent-amber);">
            <div class="takeaway-header">
                <span>2. Restructure Furniture Category Fulfillment to Solve the $742K Deficit</span>
            </div>
            <div class="takeaway-body">
                <div class="takeaway-flow">
                    <span class="flow-pill pill-obs">OBSERVATION: Furniture drives $742K (32.3% of sales) but delivers only 2.49% profit margin ($18.5K).</span>
                    <span class="flow-pill pill-why">WHY IT MATTERS: Bulky Tables (-$17.7K loss) and Bookcases (-$3.5K loss) tie up freight and warehouse space.</span>
                    <span class="flow-pill pill-act">RECOMMENDED ACTION: Shift to made-to-order supplier drop-shipping and pass shipping surcharges directly to clients.</span>
                </div>
            </div>
        </div>

        <div class="takeaway-card" style="border-left-color: var(--accent-green);">
            <div class="takeaway-header">
                <span>3. Scale Technology "Crown Jewels" (Copiers & IT Peripherals)</span>
            </div>
            <div class="takeaway-body">
                <div class="takeaway-flow">
                    <span class="flow-pill pill-obs">OBSERVATION: Copiers delivered $55.6K profit with a 37.2% margin; Phones achieved $330K sales and $44.5K profit.</span>
                    <span class="flow-pill pill-why">WHY IT MATTERS: B2B Technology has strong pricing power and corporate demand inelasticity.</span>
                    <span class="flow-pill pill-act">RECOMMENDED ACTION: Launch Managed Print Services and bundle hardware copiers with consumable paper/accessories.</span>
                </div>
            </div>
        </div>

        <div class="takeaway-card" style="border-left-color: var(--accent-blue);">
            <div class="takeaway-header">
                <span>4. Realize Regional Pricing Discipline in Central Territory & Texas</span>
            </div>
            <div class="takeaway-body">
                <div class="takeaway-flow">
                    <span class="flow-pill pill-obs">OBSERVATION: Texas lost -$25.7K on $170K sales due to 37.0% average discounting; Central margin is only 7.9%.</span>
                    <span class="flow-pill pill-why">WHY IT MATTERS: Excessive promotional discounting in Central territories undermines company profitability.</span>
                    <span class="flow-pill pill-act">RECOMMENDED ACTION: Realign Central sales commissions from gross revenue to Gross Margin Commission (GMC).</span>
                </div>
            </div>
        </div>

        <div class="takeaway-card" style="border-left-color: var(--accent-purple);">
            <div class="takeaway-header">
                <span>5. Unlock "Hidden Gems": Cross-Sell High-Margin Consumables</span>
            </div>
            <div class="takeaway-body">
                <div class="takeaway-flow">
                    <span class="flow-pill pill-obs">OBSERVATION: Paper delivers 43.4% margin ($34.1K profit); Envelopes and Labels both exceed 42% margin.</span>
                    <span class="flow-pill pill-why">WHY IT MATTERS: Zero price sensitivity, lightweight freight, and rapid commercial inventory turnover.</span>
                    <span class="flow-pill pill-act">RECOMMENDED ACTION: Add automated 1-click cart cross-selling and recurring B2B consumable subscriptions.</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripting & Chart.js Config -->
    <script>
        // Data injected from Python pipeline
        const yearlyData = {json.dumps(yearly_data)};
        const monthlyData = {json.dumps(monthly_data)};
        const catData = {json.dumps(cat_data)};
        const subcatData = {json.dumps(subcat_data)};
        const regData = {json.dumps(reg_data)};
        const stateData = {json.dumps(state_data)};
        const discData = {json.dumps(disc_data)};
        const prodData = {json.dumps(prod_data)};

        // Tab Switching Logic
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}

        // Chart styling defaults
        Chart.defaults.color = '#94A3B8';
        Chart.defaults.borderColor = '#22304A';
        Chart.defaults.font.family = "'Segoe UI', Roboto, sans-serif";

        // 1. Yearly Chart
        new Chart(document.getElementById('yearlyChart'), {{
            type: 'bar',
            data: {{
                labels: yearlyData.years,
                datasets: [
                    {{ label: 'Revenue ($)', data: yearlyData.sales, backgroundColor: '#0EA5E9', borderRadius: 4 }},
                    {{ label: 'Net Profit ($)', data: yearlyData.profit, backgroundColor: '#10B981', borderRadius: 4 }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ position: 'top' }} }},
                scales: {{
                    y: {{ ticks: {{ callback: v => '$' + (v/1000) + 'K' }} }}
                }}
            }}
        }});

        // 2. Category Chart
        new Chart(document.getElementById('categoryChart'), {{
            type: 'bar',
            data: {{
                labels: catData.categories,
                datasets: [
                    {{ label: 'Revenue ($)', data: catData.sales, backgroundColor: '#06B6D4', borderRadius: 4 }},
                    {{ label: 'Net Profit ($)', data: catData.profit, backgroundColor: ['#10B981', '#F59E0B', '#10B981'], borderRadius: 4 }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ position: 'top' }} }},
                scales: {{
                    y: {{ ticks: {{ callback: v => '$' + (v/1000) + 'K' }} }}
                }}
            }}
        }});

        // 3. Monthly Trajectory Chart
        new Chart(document.getElementById('monthlyChart'), {{
            type: 'line',
            data: {{
                labels: monthlyData.labels,
                datasets: [
                    {{
                        label: 'Monthly Sales ($)',
                        data: monthlyData.sales,
                        borderColor: '#0EA5E9',
                        backgroundColor: 'rgba(14, 165, 233, 0.15)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 2
                    }},
                    {{
                        label: 'Monthly Profit ($)',
                        data: monthlyData.profit,
                        borderColor: '#10B981',
                        borderWidth: 2,
                        tension: 0.2
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{ ticks: {{ callback: v => '$' + (v/1000) + 'K' }} }}
                }}
            }}
        }});

        // 4. Seasonality Chart (Months 1-12)
        const monthLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const monthSales = [94.9, 59.8, 205.0, 137.8, 155.0, 152.7, 147.2, 159.0, 307.6, 200.3, 352.5, 325.3];
        new Chart(document.getElementById('seasonalityChart'), {{
            type: 'bar',
            data: {{
                labels: monthLabels,
                datasets: [{{
                    label: 'Cumulative Sales ($K)',
                    data: monthSales,
                    backgroundColor: monthSales.map(v => v > 300 ? '#06B6D4' : '#0EA5E9'),
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ y: {{ ticks: {{ callback: v => '$' + v + 'K' }} }} }}
            }}
        }});

        // 5. Shipping Fulfillment Chart
        new Chart(document.getElementById('shipChart'), {{
            type: 'bar',
            data: {{
                labels: ['Standard Class', 'Second Class', 'First Class', 'Same Day'],
                datasets: [
                    {{ label: 'Sales ($K)', data: [1358.2, 459.2, 351.4, 128.4], backgroundColor: '#8B5CF6', borderRadius: 4 }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ y: {{ ticks: {{ callback: v => '$' + v + 'K' }} }} }}
            }}
        }});

        // 6. Subcategory Profit Chart
        const subNames = subcatData.map(d => d.name).reverse();
        const subProfits = subcatData.map(d => d.profit).reverse();
        new Chart(document.getElementById('subcatProfitChart'), {{
            type: 'bar',
            data: {{
                labels: subNames,
                datasets: [{{
                    label: 'Net Profit ($)',
                    data: subProfits,
                    backgroundColor: subProfits.map(v => v < 0 ? '#EF4444' : (v > 30000 ? '#10B981' : '#06B6D4')),
                    borderRadius: 4
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ x: {{ ticks: {{ callback: v => '$' + (v/1000) + 'K' }} }} }}
            }}
        }});

        // 7. Top & Loss Products
        new Chart(document.getElementById('topProdChart'), {{
            type: 'bar',
            data: {{
                labels: prodData.top_names.reverse(),
                datasets: [{{
                    label: 'Net Profit ($)',
                    data: prodData.top_profit.reverse(),
                    backgroundColor: '#10B981',
                    borderRadius: 4
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ x: {{ ticks: {{ callback: v => '$' + (v/1000) + 'K' }} }} }}
            }}
        }});

        new Chart(document.getElementById('lossProdChart'), {{
            type: 'bar',
            data: {{
                labels: prodData.loss_names,
                datasets: [{{
                    label: 'Net Loss ($)',
                    data: prodData.loss_profit,
                    backgroundColor: '#EF4444',
                    borderRadius: 4
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ x: {{ ticks: {{ callback: v => '$' + (v/1000) + 'K' }} }} }}
            }}
        }});

        // 8. Regional Chart
        new Chart(document.getElementById('regionalChart'), {{
            type: 'bar',
            data: {{
                labels: regData.regions,
                datasets: [
                    {{ label: 'Sales ($K)', data: regData.sales.map(v => v/1000), backgroundColor: '#0EA5E9', borderRadius: 4 }},
                    {{ label: 'Profit ($K)', data: regData.profit.map(v => v/1000), backgroundColor: '#10B981', borderRadius: 4 }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ y: {{ ticks: {{ callback: v => '$' + v + 'K' }} }} }}
            }}
        }});

        // 9. State Polarization Chart
        const stateLabels = ['California', 'New York', 'Washington', 'Michigan', 'Texas', 'Ohio', 'Pennsylvania', 'Illinois'];
        const stateProfits = [76.4, 74.0, 33.4, 24.5, -25.7, -17.0, -15.6, -12.6];
        new Chart(document.getElementById('statePolarChart'), {{
            type: 'bar',
            data: {{
                labels: stateLabels,
                datasets: [{{
                    label: 'Net Profit / Loss ($K)',
                    data: stateProfits,
                    backgroundColor: stateProfits.map(v => v > 0 ? '#10B981' : '#EF4444'),
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ y: {{ ticks: {{ callback: v => '$' + v + 'K' }} }} }}
            }}
        }});

        // 10. Discount Curve Chart
        new Chart(document.getElementById('discountCurveChart'), {{
            type: 'bar',
            data: {{
                labels: discData.brackets,
                datasets: [{{
                    label: 'Profit Margin (%)',
                    data: discData.margin,
                    backgroundColor: discData.margin.map(m => m > 15 ? '#10B981' : (m > 0 ? '#06B6D4' : '#EF4444')),
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ y: {{ ticks: {{ callback: v => v + '%' }} }} }}
            }}
        }});
    </script>
</body>
</html>"""

    with open('dashboard/exported_report/Superscope_Interactive_Report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Generated interactive report: dashboard/exported_report/Superscope_Interactive_Report.html")

if __name__ == '__main__':
    generate_interactive_report()
