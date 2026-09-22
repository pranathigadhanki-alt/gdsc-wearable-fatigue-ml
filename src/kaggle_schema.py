"""Kaggle Sleep Health — schema for RecoveryScope."""

COL_PERSON_ID = "Person ID"
COL_SLEEP_DURATION = "Sleep Duration"
COL_QUALITY_OF_SLEEP = "Quality of Sleep"
COL_PHYSICAL_ACTIVITY = "Physical Activity Level"
COL_STRESS_LEVEL = "Stress Level"
COL_HEART_RATE = "Heart Rate"
COL_DAILY_STEPS = "Daily Steps"
COL_SLEEP_DISORDER = "Sleep Disorder"
COL_AGE = "Age"
COL_GENDER = "Gender"

COL_PARTICIPANT = "participant_id"
COL_SLEEP_DURATION_H = "sleep_duration"
COL_QUALITY = "quality_of_sleep"
COL_ACTIVITY = "physical_activity_level"
COL_STRESS = "stress_level"
COL_HR = "heart_rate"
COL_STEPS = "daily_steps"
COL_AGE_SNAKE = "age"
COL_DISORDER = "sleep_disorder"

# Training label: next night improves (hidden quality/sleep in inference)
LABEL_RECOVERY = "better_night_tomorrow"

DISORDER_COHORT = ("Insomnia", "Sleep Apnea")

KAGGLE_FILENAME = "Sleep_health_and_lifestyle_dataset.csv"

WATCH_SIGNALS = ("sleep_duration", "heart_rate", "daily_steps", "physical_activity_level")
LAG_SIGNALS = ("lag1_sleep_duration", "lag1_heart_rate", "lag1_daily_steps", "lag1_physical_activity_level")
