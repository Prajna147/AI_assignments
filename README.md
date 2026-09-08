# AQI Simple Reflex Agent

This project calculates the Air Quality Index (AQI) from pollutant values and uses a Simple Reflex Agent to determine the air quality.

The agent uses the current pollutant readings and applies predefined CPCB rules to calculate the AQI.

## How it works

```text
Pollutant Data
      ↓
Calculate sub-indices
      ↓
Find highest sub-index
      ↓
AQI
      ↓
AQI Category
```

The pollutants used are:

* PM2.5
* PM10
* CO
* SO2
* NO2
* O3

## AQI Categories

| AQI     | Category     |
| ------- | ------------ |
| 0–50    | Good         |
| 51–100  | Satisfactory |
| 101–200 | Moderate     |
| 201–300 | Poor         |
| 301–400 | Very Poor    |
| 401–500 | Severe       |

## Dataset

The project currently uses:

```text
air_quality_historical.csv
```

The CSV contains pollutant readings for Hyderabad.

Each reading is passed to the agent, which calculates the AQI.

## Running the project

Install Pandas:

```bash
pip install pandas
```

Run the program:

```bash
python aqi_agent.py
```

## Output

The program displays:

```text
Date        : 2026-09-03
AQI value   : 250
Category    : Poor
Worst pollutant: pm2_5
```

It also shows the individual pollutant sub-indices.

## Simple Reflex Agent

The agent only uses the **current reading** to make its decision.

For example:

```text
Current PM2.5
      ↓
AQI calculation
      ↓
AQI = 250
      ↓
Poor
```

It does not use previous readings or machine learning.

## Future Work

The CSV data can later be replaced with **real-time API data**, such as pollution and weather data, while keeping the same agent logic.
