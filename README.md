# 📈 Real-time Stock Market Data Pipeline

> **End-to-end streaming analytics platform with Kafka, Airflow, DBT, Snowflake, and Power BI**

[![Apache Kafka](https://img.shields.io/badge/Kafka-Event%20Streaming-231F20?style=flat-square&logo=apache-kafka)](https://kafka.apache.org/)
[![Apache Airflow](https://img.shields.io/badge/Airflow-Orchestration-017CEE?style=flat-square&logo=apache-airflow)](https://airflow.apache.org/)
[![DBT](https://img.shields.io/badge/DBT-Data%20Transformation-FF694B?style=flat-square&logo=dbt)](https://www.getdbt.com/)
[![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Warehouse-29B5E8?style=flat-square&logo=snowflake)](https://www.snowflake.com/)
[![MinIO](https://img.shields.io/badge/MinIO-Object%20Storage-C72E49?style=flat-square&logo=minio)](https://min.io/)

## 🎯 Overview

A **production-grade real-time data pipeline** ingesting live stock market data from Finnhub API, processing through **Medallion Architecture (Bronze → Silver → Gold)** using DBT, and delivering actionable insights via Power BI dashboards. Built with modern data stack for scalability and reliability.

### ✨ Key Features

- **⚡ Real-time Streaming** - Kafka for low-latency data ingestion (5 major stocks: AAPL, MSFT, TSLA, GOOGL, AMZN)
- **🗄️ Object Storage** - MinIO (S3-compatible) for data lake persistence
- **🔄 Orchestration** - Apache Airflow for automated data pipeline scheduling
- **🏗️ Medallion Architecture** - Bronze (raw) → Silver (cleansed) → Gold (business-ready)
- **🛠️ DBT Transformations** - SQL-based data modeling with version control
- **☁️ Snowflake Warehouse** - Scalable cloud data warehouse with compute separation
- **📊 Power BI Integration** - DirectQuery for live dashboards (KPIs, candlestick charts, volatility analysis)

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   DATA SOURCE LAYER                          │
├──────────────────────────────────────────────────────────────┤
│  📡 Finnhub Stock API                                        │
│  • 60 API calls/minute                                       │
│  • Real-time market quotes                                   │
│  • Stocks: AAPL, MSFT, TSLA, GOOGL, AMZN                    │
└──────────────────────────────────────────────────────────────┘
                            ↓
                  🐍 Python Producer Script
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   STREAMING LAYER                            │
├──────────────────────────────────────────────────────────────┤
│  ⚡ Apache Kafka + Zookeeper                                 │
│  • Topic: stock-quotes                                       │
│  • Producer: Fetch & publish every 6 seconds                 │
│  • Consumer: Stream to MinIO storage                         │
│  🖥️ Kafdrop UI - Monitoring & topic visualization          │
└──────────────────────────────────────────────────────────────┘
                            ↓
                  🐍 Python Consumer Script
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   STORAGE LAYER (DATA LAKE)                  │
├──────────────────────────────────────────────────────────────┤
│  💾 MinIO (S3-Compatible Object Storage)                    │
│  • Bucket: bronze-transactions                               │
│  • Format: JSON (partitioned by symbol & timestamp)         │
│  • Path: {symbol}/{timestamp}.json                           │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                        │
├──────────────────────────────────────────────────────────────┤
│  🔄 Apache Airflow                                           │
│  • DAG: minio_to_snowflake                                   │
│  • Schedule: Every 1 minute (*/1 * * * *)                    │
│  • Tasks:                                                    │
│    1. Download files from MinIO bucket                       │
│    2. Stage files in Snowflake internal stage                │
│    3. COPY INTO bronze_stock_raw table                       │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   DATA WAREHOUSE (SNOWFLAKE)                 │
├──────────────────────────────────────────────────────────────┤
│  ❄️ Bronze Layer (STOCKS_DB.BRONZE)                         │
│  • Table: bronze_stock_raw (VARIANT type for JSON)          │
│  • Raw data ingestion from MinIO                             │
└──────────────────────────────────────────────────────────────┘
                            ↓
                    🛠️ DBT Transformations
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   DBT TRANSFORMATION LAYER                   │
├─────────────────────────┬────────────────────────────────────┤
│  🥉 BRONZE              │  • Parse JSON to structured columns│
│                         │  • Extract: price, high, low, etc  │
├─────────────────────────┼────────────────────────────────────┤
│  🥈 SILVER              │  • Cleanse & validate data         │
│                         │  • Round decimals, filter nulls    │
│                         │  • curated_stocks model            │
├─────────────────────────┼────────────────────────────────────┤
│  🥇 GOLD                │  • Business-ready views            │
│                         │  • kpi.sql - Latest price & change │
│                         │  • candlestick.sql - OHLC charts   │
│                         │  • treechart.sql - Volatility      │
└─────────────────────────┴────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   VISUALIZATION LAYER                        │
├──────────────────────────────────────────────────────────────┤
│  📊 Power BI Dashboards (DirectQuery)                       │
│  • KPI Cards: Current price, % change, daily movement        │
│  • Candlestick Charts: 12-period OHLC with trend lines      │
│  • Treemap: Stock volatility & relative risk analysis       │
│  • Live refresh via Snowflake connection                     │
└──────────────────────────────────────────────────────────────┘
```

## 🛠️ Technical Stack

### **Data Ingestion & Streaming**
- **⚡ Apache Kafka** - Distributed event streaming platform
- **🐘 Zookeeper** - Kafka cluster coordination
- **🖥️ Kafdrop** - Web UI for Kafka monitoring
- **🐍 Python Producer/Consumer** - Custom scripts for API → Kafka → MinIO

### **Storage & Orchestration**
- **💾 MinIO** - S3-compatible object storage (data lake)
- **🔄 Apache Airflow** - Workflow automation & scheduling
- **🐘 PostgreSQL** - Airflow metadata database

### **Data Warehouse & Transformation**
- **❄️ Snowflake** - Cloud data warehouse with compute separation
- **🛠️ DBT (Data Build Tool)** - SQL-based data transformations
- **📊 Medallion Architecture** - Bronze → Silver → Gold layers

### **Analytics & Visualization**
- **💼 Power BI** - Interactive dashboards with DirectQuery
- **📈 Advanced Charts** - Candlestick, treemap, KPI cards

## 📊 Data Models (DBT)

### **Bronze Layer** - Raw Data Extraction
```sql
-- bronze_queries.sql
-- Parse JSON VARIANT to structured columns
SELECT
    v:c::float AS current_price,
    v:h::float AS day_high,
    v:l::float AS day_low,
    v:symbol::string AS symbol,
    v:t::timestamp AS market_timestamp
FROM bronze_stock_raw
```

### **Silver Layer** - Data Cleansing
```sql
-- curated_stocks.sql
-- Round decimals, filter nulls, standardize formats
SELECT
    symbol,
    current_price,
    ROUND(day_high, 2) AS day_high,
    ROUND(change_percent, 4) AS change_percent
FROM bronze_stock_raw
WHERE current_price IS NOT NULL
```

### **Gold Layer** - Business Views

**1. KPI Dashboard** (`kpi.sql`)
- Latest price, change amount, % change per stock
- Window function for most recent record per symbol

**2. Candlestick Chart** (`candlestick.sql`)
- OHLC (Open, High, Low, Close) data
- 12-period rolling window with trend lines
- Daily aggregation with FIRST_VALUE/LAST_VALUE

**3. Volatility Treemap** (`treechart.sql`)
- Standard deviation of prices (absolute & relative)
- Average price per stock
- Risk analysis metrics

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- Snowflake account
- Finnhub API key (free tier: 60 calls/min)
- Power BI Desktop (optional for dashboards)

### Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/real-time-stock-data-pipeline.git
cd real-time-stock-data-pipeline

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Start infrastructure (Kafka, MinIO, Airflow)
cd infra/
docker-compose up -d

# 4. Initialize Airflow database
docker-compose exec airflow-scheduler airflow db init
docker-compose exec airflow-webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin123

# 5. Create Kafka topic
# Access Kafdrop UI at http://localhost:9000
# Create topic: stock-quotes (partitions: 1, replication: 1)

# 6. Start data ingestion
python infra/producer/producer.py  # Run in background
python infra/consumer/consumer.py  # Run in background

# 7. Configure Snowflake connection in Airflow DAG
# Edit: infra/Dag/minio_to_snowflake.py
# Add: SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT

# 8. Setup DBT for Snowflake
cd dbt_models/
dbt init
dbt run  # Execute all transformations

# 9. Connect Power BI
# Get Data → Snowflake
# Server: your-account.snowflakecomputing.com
# Warehouse: Stock_Wh
# Database: STOCKS_DB
# Connection: DirectQuery
```

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Kafdrop (Kafka UI) | http://localhost:9000 | None |
| MinIO Console | http://localhost:9001 | admin / password123 |
| Airflow Webserver | http://localhost:8080 | admin / admin123 |
| Snowflake | your-account.snowflakecomputing.com | Your credentials |

## 📈 Power BI Dashboard Features

### **KPI Cards**
- **Current Price** - Real-time stock value
- **Change Amount** - Absolute price movement ($)
- **Change Percent** - Relative daily change (%)

### **Candlestick Chart**
- **12-period OHLC** - Open, High, Low, Close
- **Trend Lines** - Moving average overlay
- **Time-series Analysis** - Daily market behavior

### **Volatility Treemap**
- **Stock Comparison** - Size by average price
- **Risk Metrics** - Color by volatility (STDDEV)
- **Relative Volatility** - Coefficient of variation

## 🔧 Configuration Files

### **Docker Compose Services**
- `zookeeper` - Kafka coordination (port 2181)
- `kafka` - Event streaming (ports 9092, 29092)
- `kafdrop` - Kafka UI (port 9000)
- `minio` - Object storage (ports 9001, 9002)
- `airflow-webserver` - Airflow UI (port 8080)
- `airflow-scheduler` - Task scheduling
- `postgres` - Airflow metadata (port 5432)

### **DBT Project Structure**
```
dbt_models/
├── bronze/
│   ├── bronze_queries.sql      # JSON parsing
│   └── source.yml              # Source table config
├── silver/
│   └── curated_stocks.sql      # Data cleansing
└── gold/
    ├── kpi.sql                 # Latest stock metrics
    ├── candlestick.sql         # OHLC chart data
    └── treechart.sql           # Volatility analysis
```

## 🎯 Pipeline Workflow

1. **Data Ingestion** (Every 6 seconds)
   - Producer fetches quotes from Finnhub API
   - Publishes to Kafka topic `stock-quotes`
   - Consumer reads from Kafka → writes to MinIO

2. **Data Loading** (Every 1 minute)
   - Airflow DAG triggers
   - Downloads new files from MinIO
   - Stages in Snowflake internal stage
   - COPY INTO bronze table

3. **Data Transformation** (On-demand/Scheduled)
   - DBT runs Bronze → Silver → Gold transformations
   - Creates curated views for Power BI
   - Maintains data quality & business logic

4. **Visualization** (Real-time)
   - Power BI DirectQuery refreshes automatically
   - Dashboards reflect latest Snowflake data
   - Users interact with live stock analytics

## 🌟 Advanced Features

### **Schema Evolution**
- JSON VARIANT type in Snowflake for flexible schemas
- DBT models adapt to new fields automatically
- Backward-compatible transformations

### **Data Quality**
- Null filtering in Silver layer
- Decimal rounding for consistency
- Deduplication using window functions

### **Performance Optimization**
- Partitioned MinIO storage by symbol & timestamp
- Snowflake clustering on symbol column
- DBT incremental models for large datasets

### **Monitoring & Observability**
- Kafdrop for Kafka topic health
- Airflow task logs & alerting
- Snowflake query history & performance

## 🎯 Real-world Use Cases

- **📊 Investment Analysis** - Real-time portfolio tracking
- **🤖 Algorithmic Trading** - Low-latency market data feeds
- **📈 Market Research** - Historical trend analysis
- **💼 Financial Reporting** - Executive dashboards
- **🎓 Educational Platform** - Learn data engineering with real data

## 🚀 Future Enhancements

- [ ] **🤖 ML Integration** - Price prediction models with Snowflake ML
- [ ] **📱 Mobile Alerts** - Real-time price movement notifications
- [ ] **🌍 Multi-exchange Support** - Global stock markets (NYSE, NASDAQ, LSE)
- [ ] **📊 Advanced Metrics** - RSI, MACD, Bollinger Bands
- [ ] **🔔 Anomaly Detection** - Alert on unusual price movements
- [ ] **⚡ Change Data Capture** - Incremental DBT models for efficiency
- [ ] **🔗 API Layer** - REST API for consuming transformed data

## 🤝 Contributing

Contributions welcome! Focus areas:
- **📈 Additional Stock Metrics** - Technical indicators & financial ratios
- **🔧 Pipeline Optimization** - Performance tuning & cost reduction
- **📊 Dashboard Enhancements** - New visualizations & KPIs
- **🧪 Testing** - DBT tests & data quality checks

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Real-time financial analytics with modern data engineering** 📈⚡
