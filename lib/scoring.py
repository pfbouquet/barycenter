from math import log
import pandas as pd


def get_best_time(time_list):

    return min(time_list)


def get_best_rate(rate_list, number_rate_list):

    return max([rate_list[i] * min(log(number_rate_list[i]), log(200)) for i in range(len(rate_list))])


def get_score(best_rate, min_time, rate, time, price):

    note_time = max(0, 1 - (time - min_time) / 30)
    note_ratings = rate / best_rate
    note_price = get_price_score(price)

    return note_time + note_ratings + note_price


def get_price_score(price):

    if not price:
        return 0.5
    elif len(price) == 1:
        return 1
    elif len(price) == 2:
        return 0.75
    elif len(price) == 3:
        return 0.5
    else:
        return 0.25


def score_places(place_df):
    place_df.reset_index(inplace=True, drop=True)
    best_time = get_best_time(place_df.time)
    best_rate = get_best_rate(place_df.rating.tolist(), place_df.review_count.tolist())

    list_score = []

    for index, row in place_df.iterrows():
        current_rate = row['rating'] * min(log(row['review_count']), log(200))
        current_score = get_score(best_rate, best_time, current_rate, row['time'], row['price'])
        list_score.append(current_score)

    place_df['score'] = list_score

    return place_df



