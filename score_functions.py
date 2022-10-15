"""Functions to calculate user score on submissions"""

import datetime
from api import prediction_using_url
from image_url_test import get_image_url


def find_names(data: list[dict]) -> set[str]:
    """Given the data from predictions, find all the scientific names from the top 3"""
    all_names = set()
    for result in data[:3]:
        all_names.add(result["scientific name"])

    return all_names


def find_current_score(init_score: int, init_time: datetime.datetime) -> int:
    """
    Takes in a score and datetime, returns a new score depending on the time elapsed
    Time reduction intervals: 3 hours
    Total hours elapsed: 168 hours
    Total reduction intervals: 56
    Maximum reduction: 50%
    Formula: init_score - (init_score // 2) * degradation_constant
    Where degradation_constant = min(1, (intervals_elapsed / 56))
    Then return the rounded score
    """
    interval_amount = 3
    total_reduction_intervals = 168 // interval_amount

    current_time = datetime.datetime.now()
    time_diff = current_time - init_time
    hours_diff = time_diff.total_seconds() / 60 / 60

    intervals_elapsed = hours_diff // interval_amount
    degradation_constant = min(intervals_elapsed / total_reduction_intervals, 1)

    current_score = init_score - (init_score // 2) * degradation_constant
    return round(current_score)


def find_image_score(img: str, correct_species: dict[str, int], init_time: datetime.datetime) -> int:
    """
    Take in an image and a mapping of correct species to their initial score
    First call get_image_url to get the image url of the image
    Then, call prediction_using_url to get the results from that image
    Then, call find_names to get all the feasible names of the plant
    Check if any of the names are a correct species
    If so, then return the current score by passing initial score into find_current_score.
    """
    image_url = get_image_url(img)
    results = prediction_using_url([image_url])
    names = find_names(results)

    for name in names:
        if name in correct_species:
            return find_current_score(correct_species[name], init_time)

    return 0


# testing the code
if __name__ == '__main__':
    img_path = 'test_pictures/palm-tree.jpg'
    challenge_scores = {
        # palm tree
        'Cocos nucifera': 3000,
        # neem tree
        'Azadirachta indica': 2000,
        'cucumber': 1000
    }
    # last week saturday, oct 8, 5pm
    init_date = datetime.datetime(2022, 10, 8, 17, 0, 0)

    print(find_image_score(img_path, challenge_scores, init_date))
