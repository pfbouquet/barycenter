from math import log


def get_best_time(bar_list):

    return min([bar_list[i]['time'] for i in range(len(bar_list))])


def get_best_rate(bar_list):

    return max([bar_list[i]['rate'] * min(log(bar_list[i]['number_of_ratings']), log(200)) for i in range(len(bar_list))])


def get_score(best_rate, min_time, rate, time, price):

    note_time = max(0, 1 - (time - min_time) / 30)
    note_ratings = rate / best_rate
    note_price = get_price_score(price)

    return note_time + note_ratings + note_price


def get_price_score(price):

    if len(price) == 1:
        return 1
    elif len(price) == 2:
        return 0.75
    elif len(price) == 3:
        return 0.5
    else:
        return 0.25



