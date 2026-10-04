# SUPERSCOPE: Power BI Desktop Implementation & DAX Architecture Guide
**Elevate Labs Data Analyst Internship — Task 2: Data Visualization and Storytelling**  
*Project:* SUPERSCOPE — Retail Intelligence & Sales Story  
*Target Tool:* Microsoft Power BI Desktop (Free) / Power BI Service

---

## 1. Overview & Setup Prerequisites

This manual provides a beginner-friendly, click-by-click implementation roadmap to replicate the **SUPERSCOPE** executive intelligence dashboard directly inside **Microsoft Power BI Desktop**.

### File Location
- **Dataset File:** `data/cleaned/Superstore_Cleaned.csv` (or `data/raw/Superstore.csv`)
- **Format:** CSV UTF-8
- **Total Records:** 9,994 rows, 21 columns

---

## 2. Step 1: Loading & Transforming the Dataset

1. Open **Power BI Desktop**.
2. On the **Home** ribbon, click **Get Data** → Select **Text/CSV** → Click **Connect**.
3. Browse to your project folder and select:
   `data/cleaned/Superstore_Cleaned.csv`
4. In the preview window, confirm:
   - **File Origin:** `65001: Unicode (UTF-8)`
   - **Delimiter:** `Comma`
5. Click **Transform Data** to open **Power Query Editor**.
6. Verify Data Types in Power Query:
   - `Order Date` → **Date**
   - `Ship Date` → **Date**
   - `Sales` → **Fixed Decimal Number ($)** or **Decimal Number**
   - `Profit` → **Fixed Decimal Number ($)** or **Decimal Number**
   - `Discount` → **Percentage** (or Decimal Number)
   - `Quantity` → **Whole Number**
   - `Postal Code` → **Text** (prevent leading zero truncation)
7. On the **Home** ribbon, click **Close & Apply**.

---

## 3. Step 2: Essential DAX Measures Library

To maintain professional enterprise standards, create a dedicated measures table:
1. On the **Home** ribbon, click **Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Right-click `_Measures` in the Data pane and select **New Measure** for each of the following formulas:

### Headline Financial Measures

```dax
// 1. Total Enterprise Sales
Total Sales = SUM(Superstore_Cleaned[Sales])
```
*Format: Currency ($ English United States), 0 decimal places.*

```dax
// 2. Total Net Profit
Total Profit = SUM(Superstore_Cleaned[Profit])
```
*Format: Currency ($ English United States), 0 decimal places.*

```dax
// 3. Profit Margin Percentage
Profit Margin % = 
DIVIDE(
    [Total Profit],
    [Total Sales],
    0
)
```
*Format: Percentage (%), 2 decimal places.*

```dax
// 4. Total Unique Orders
Total Orders = DISTINCTCOUNT(Superstore_Cleaned[Order ID])
```
*Format: Whole Number, comma separated (e.g. 5,009).*

```dax
// 5. Total Active Customers
Total Customers = DISTINCTCOUNT(Superstore_Cleaned[Customer ID])
```
*Format: Whole Number (e.g. 793).*

```dax
// 6. Average Order Value (AOV)
Average Order Value = 
DIVIDE(
    [Total Sales],
    [Total Orders],
    0
)
```
*Format: Currency ($), 2 decimal places ($458.61).*

```dax
// 7. Net Profit Per Order
Profit Per Order = 
DIVIDE(
    [Total Profit],
    [Total Orders],
    0
)
```
*Format: Currency ($), 2 decimal places ($57.18).*

```dax
// 8. Discount Capital Burn (>30% Discounts)
Discount Profit Burn = 
CALCULATE(
    [Total Profit],
    Superstore_Cleaned[Discount] > 0.30
)
```
*Format: Currency ($), 0 decimal places (-$125,007).*

---

## 4. Step 3: Canvas Setup & Theme Styling

1. Click on any blank area of the report canvas.
2. In the **Visualizations** pane, select the **Format page** icon (paint roller / canvas settings).
3. Expand **Canvas settings**:
   - **Type:** `16:9` (1280 x 720 px or 1920 x 1080 px).
4. Expand **Canvas background**:
   - **Color:** Dark Navy `#0A0E1A` (or `#0F172A`).
   - **Transparency:** `0%`.
5. On the **View** ribbon, select **Themes** → Customize current theme:
   - Primary Accent: `#0EA5E9` (Electric Cyan)
   - Secondary Accent: `#10B981` (Emerald Green)
   - Negative / Loss: `#EF4444` (Crimson)
   - Text Font: `Segoe UI` (Off-white `#F8FAFC`).

---

## 5. Step 4: Click-by-Click Visual Construction

### Section 1: Interactive Filter Slicers (Top Banner)
1. Select the **Slicer** visual from the Visualizations pane.
2. Drag `Order Year` into **Field**.
3. Format Slicer:
   - Slicer settings → Style: **Tile** or **Dropdown**.
   - Background: `#131B2E`, Text: `#F8FAFC`.
4. Add two more slicers:
   - **Region** (West, East, Central, South)
   - **Category** (Technology, Office Supplies, Furniture)
5. Position them neatly in the top right corner.

---

### Section 2: Top KPI Metric Cards (5 Cards)
1. Select the **Card (new)** or standard **Card** visual.
2. In **Fields / Values**, drag:
   - Card 1: `[Total Sales]` → Label: "TOTAL REVENUE" ($2,297,201)
   - Card 2: `[Total Profit]` → Label: "TOTAL PROFIT" ($286,397)
   - Card 3: `[Profit Margin %]` → Label: "PROFIT MARGIN" (12.47%)
   - Card 4: `[Average Order Value]` → Label: "AVG ORDER VALUE" ($458.61)
   - Card 5: `[Discount Profit Burn]` → Label: "DISCOUNT CAPITAL BURN" (-$125,007)
3. Formatting:
   - Card background: `#131B2E`, Border: `#22304A` with 6px rounded corners.
   - Callout value font size: `24pt`, Bold, Color: `#F8FAFC`.
   - Accent bar on left edge.

---

### Section 3: Time Series Trajectory (The Sales Story)
1. Select **Line and Clustered Column Chart** (or **Line Chart**).
2. Fields:
   - **X-axis:** Drag `Order Date` (select `Year` and `Month` hierarchy, or `Order YearMonth`).
   - **Y-axis (Column):** Drag `[Total Sales]`.
   - **Line Y-axis:** Drag `[Total Profit]`.
3. Formatting:
   - Column Color: `#0EA5E9` (Cyan).
   - Line Color: `#10B981` (Emerald Green), stroke width `3px`.
   - Title: *"Monthly Revenue Trajectory & Net Profit Realization (2014 – 2017)"*.
4. Expected Result:
   - Clear visual evidence of Q4 November-December spikes ($97K in Nov 2017) and January post-holiday slumps.

---

### Section 4: Sub-Category Profit Spectrum (Horizontal Bar Chart)
1. Select **Clustered Bar Chart**.
2. Fields:
   - **Y-axis:** Drag `Sub-Category`.
   - **X-axis:** Drag `[Total Profit]`.
3. Sort:
   - Click the three dots (...) on top right of visual → **Sort axis** → select `Total Profit` → **Sort descending**.
4. Conditional Formatting for Bars:
   - Format visual → **Bars** → click `fx` next to Color.
   - Format style: **Rules**.
   - What field should we base this on? `[Total Profit]`.
   - If value `>= 0` (Number) → Color: `#10B981` (Green).
   - If value `< 0` (Number) → Color: `#EF4444` (Crimson Red).
5. Expected Result:
   - Copiers, Phones, Accessories at the top in green.
   - Tables (-$17.7K), Bookcases (-$3.5K), Supplies (-$1.2K) highlighted at the bottom in crimson red.

---

### Section 5: The Opportunity Radar (Scatter Matrix)
1. Select **Scatter Chart**.
2. Fields:
   - **Values:** Drag `Sub-Category`.
   - **X-axis:** Drag `[Total Sales]`.
   - **Y-axis:** Drag `[Total Profit]`.
   - **Size:** Drag `Quantity` (sum).
   - **Legend:** Drag `Category`.
3. Add Constant Reference Lines:
   - In Analytics pane (magnifying glass icon):
   - Add **X-axis Constant Line** at `150,000` (Median sales line).
   - Add **Y-axis Constant Line** at `15,000` (Median profit line).
4. Expected Result:
   - Quadrant 1 (Top-Right): "Crown Jewels" (Copiers, Phones, Accessories).
   - Quadrant 2 (Top-Left): "Hidden Gems" (Paper, Envelopes, Labels).
   - Quadrant 4 (Bottom-Right): "Profit Drains" (Tables, Machines, Bookcases).

---

## 6. Validation Checklist & Submission Export

Before submitting:
- [x] Verify total sales equals `$2,297,201`
- [x] Verify total profit equals `$286,397`
- [x] Verify profit margin equals `12.47%`
- [x] Test slicers: clicking "2017" updates all visuals dynamically
- [x] Click **File** → **Save As** → `dashboard/Superscope_Retail_Intelligence.pbix`
- [x] Click **File** → **Export** → **Export to PDF** → `dashboard/exported_report/Superscope_Executive_Summary.pdf`
