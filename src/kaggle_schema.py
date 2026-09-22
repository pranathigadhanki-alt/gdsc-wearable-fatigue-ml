"""Kaggle Sleep Health and Lifestyle — column names."""

COL_PERSON_ID = "Person ID"
COL_SLEEP_DURATION = "Sleep Duration"
COL_QUALITY_OF_SLEEP = "Quality of Sleep"
COL_PHYSICAL_ACTIVITY = "Physical Activity Level"
COL_STRESS_LEVEL = "Stress Level"
COL_HEART_RATE = "Heart Rate"
COL_DAILY_STEPS = "Daily Steps"
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

# Hidden at inference — used only to build training labels
LABEL_STRAIN = "strain_high"

KAGGLE_FILENAME = "Sleep_health_and_lifestyle_dataset.csv"

# Watch-like signals the user can adjust in the app
WATCH_SIGNALS = ("sleep_duration", "heart_rate", "daily_steps", "physical_activity_level")
