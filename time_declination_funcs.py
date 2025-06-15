import math

def declination_word(n, one, few, many):
    if 11 <= n % 100 <= 14:
        return many
    last_digit = n % 10
    if last_digit == 1:
        return one
    elif 2 <= last_digit <= 4:
        return few
    else:
        return many

def time_declination(n, unit):
    unit = unit.lower()
    units = {
        "месяц":   {"forms": ("месяц", "месяца", "месяцев"),   "gender": "m"},
        "день":    {"forms": ("день", "дня", "дней"),          "gender": "m"},
        "час":     {"forms": ("час", "часа", "часов"),         "gender": "m"},
        "минута":  {"forms": ("минута", "минуты", "минут"),    "gender": "f"},
        "секунда": {"forms": ("секунда", "секунды", "секунд"), "gender": "f"},
    }

    if unit not in units:
        return "Неверная единица времени"

    one, few, many = units[unit]["forms"]
    gender = units[unit]["gender"]
    word = declination_word(n, one, few, many)

    if 11 <= n % 100 <= 14:
        verb = "осталось"
    else:
        last_digit = n % 10
        if last_digit == 1:
            verb = "остался" if gender == "m" else "осталась"
        else:
            verb = "осталось"

    return f"{verb} {n} {word}"


def time_left(total_seconds):
    if total_seconds is True:
        return 'У вас безлимит'
    if total_seconds is None:
        return 'Вам доступен пробный период'
    if total_seconds < 0:
        return "Подписка закончилась"

    if total_seconds >= 86400:
        # Осталось больше или ровно 1 дня — округляем дни вверх
        days_left = math.ceil(total_seconds / 86400)
        return f"До конца подписки {time_declination(days_left, 'день')}"
    else:
        # Меньше суток — показываем часы и минуты
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        parts = []
        if hours > 0:
            parts.append(time_declination(hours, 'час'))
        if minutes > 0:
            parts.append(time_declination(minutes, 'минута'))

        if not parts:
            return time_declination(1, 'минута')  # Показываем минимум 1 минуту

        return "До конца подписки " + " и ".join(parts)

if __name__ == '__main__':
    import time

    expire = time.time() + 3 * 86400 + 23545
    print(time_left(expire))
