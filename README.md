# Sleep Score

## About

This is a simple Python program that calculates a sleep score based on the user's sleep information.

The program takes a few inputs, gives points for each input, and calculates the final sleep score out of 100.

## Inputs

The program asks for:

* Sleep duration in hours
* Sleep quality from 1 to 10
* Number of times the person woke up
* Sleep consistency from 1 to 10

## Scoring

### Sleep Duration

* 7–9 hours → 40 points
* 6–7 or 9–10 hours → 30 points
* 5–6 or more than 10 hours → 20 points
* Less than 5 hours → 10 points

### Sleep Quality

* 9–10 → 30 points
* 7–8 → 24 points
* 5–6 → 18 points
* 3–4 → 12 points
* 1–2 → 6 points

### Night Awakenings

* 0–1 → 20 points
* 2 → 15 points
* 3 → 10 points
* 4 → 5 points
* More than 4 → 0 points

### Sleep Consistency

* 9–10 → 10 points
* 7–8 → 8 points
* 5–6 → 6 points
* 3–4 → 4 points
* 1–2 → 2 points

## Sleep Result

The final score gives one of these results:

* 90–100 → Deep Sleep
* 75–89 → Restful Sleep
* 60–74 → Light Sleep
* 40–59 → Disturbed Sleep
* 0–39 → Poor Sleep

## Example

```text
How many hours did you sleep? 8
Rate your sleep quality from 1 to 10: 9
How many times did you wake up during the night? 1
Rate your sleep consistency from 1 to 10: 8

Sleep Score: 98 / 100
Sleep Type: Deep Sleep
```

## How to Run

Open the VS Code terminal and run:

```bash
python sleep_score.py
```

Then enter the values asked by the program.

## Files

```text
sleep_agent/
│
├── sleep_score.py
└── README.md
```
