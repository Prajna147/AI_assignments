def get_duration_score(hours):
    if 7 <= hours <= 9:
        return 40
    elif 6 <= hours < 7 or 9 < hours <= 10:
        return 30
    elif 5 <= hours < 6 or hours > 10:
        return 20
    else:
        return 10


def get_quality_score(quality):
    if quality >= 9:
        return 30
    elif quality >= 7:
        return 24
    elif quality >= 5:
        return 18
    elif quality >= 3:
        return 12
    else:
        return 6


def get_awake_score(awakenings):
    if awakenings <= 1:
        return 20
    elif awakenings == 2:
        return 15
    elif awakenings == 3:
        return 10
    elif awakenings == 4:
        return 5
    else:
        return 0


def get_consistency_score(consistency):
    if consistency >= 9:
        return 10
    elif consistency >= 7:
        return 8
    elif consistency >= 5:
        return 6
    elif consistency >= 3:
        return 4
    else:
        return 2


sleep_hours = float(input("How many hours did you sleep? "))
sleep_quality = int(input("Rate your sleep quality from 1 to 10: "))
awakenings = int(input("How many times did you wake up during the night? "))
consistency = int(input("Rate your sleep consistency from 1 to 10: "))


duration_score = get_duration_score(sleep_hours)
quality_score = get_quality_score(sleep_quality)
awake_score = get_awake_score(awakenings)
consistency_score = get_consistency_score(consistency)


sleep_score = (
    duration_score
    + quality_score
    + awake_score
    + consistency_score
)


if sleep_score >= 90:
    sleep_type = "Deep Sleep"
elif sleep_score >= 75:
    sleep_type = "Restful Sleep"
elif sleep_score >= 60:
    sleep_type = "Light Sleep"
elif sleep_score >= 40:
    sleep_type = "Disturbed Sleep"
else:
    sleep_type = "Poor Sleep"


print("\nSleep Score:", sleep_score, "/ 100")
print("Sleep Type:", sleep_type)