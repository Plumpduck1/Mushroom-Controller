humidity = 92
co2 = 800
temperature = 21.5

fan_on = False
mister_on = False

auto_mode = True


def update_environment():
    global humidity, co2

    if mister_on:
        humidity += 0.5
    else:
        humidity -= 0.2

    if fan_on:
        co2 -= 50
        humidity -= 0.3
    else:
        co2 += 20

    humidity = max(70, min(100, humidity))
    co2 = max(400, min(2000, co2))