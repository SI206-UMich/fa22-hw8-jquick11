import matplotlib.pyplot as plt
import os
import sqlite3
import unittest


def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """

    answer = []

    path = os.path.dirname(os.path.abspath(__file__))
    cur = sqlite3.connect(path + '/' + db_filename).cursor()

    cur.execute("""SELECT name, category_id, building_id, rating FROM restaurants""")
    restaurants = cur.fetchall()

    for restaurant in restaurants:

        name, category_id, building_id, rating = restaurant

        cur.execute("""SELECT category FROM categories WHERE id=:id""", {"id": category_id})
        category = cur.fetchone()[0]

        cur.execute("""SELECT building FROM buildings WHERE id=:id""", {"id": building_id})
        building = cur.fetchone()[0]

        dictionary = dict(zip(['name', 'category', 'building', 'rating'],
                              [name, category, building, rating]))
        answer.append(dictionary)

    return answer


def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """

    dictionary = {}

    path = os.path.dirname(os.path.abspath(__file__))
    cur = sqlite3.connect(path + '/' + db_filename).cursor()

    cur.execute("""SELECT * FROM categories""")
    categories = cur.fetchall()

    for category_id, category in categories:

        cur.execute("""SELECT COUNT() FROM restaurants WHERE category_id=:id""", {"id": category_id})
        number = cur.fetchone()[0]

        dictionary[category] = number

    sorted_dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1]))
    categories = list(sorted_dictionary.keys())
    numbers = list(sorted_dictionary.values())

    plt.figure('Part 2: Visualize the data', figsize=(12, 6))
    plt.subplots_adjust(right=0.9, left=0.2)
    plt.barh(categories, numbers)

    plt.title('Types of Restaurant on South University Ave')
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Restaurant Categories')

    plt.savefig('TypesOfRestaurant_BarChart.png')

    return dictionary


#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """

    dictionary = {}

    path = os.path.dirname(os.path.abspath(__file__))
    cur = sqlite3.connect(path + '/' + db_filename).cursor()

    cur.execute("""SELECT * FROM categories""")
    categories = cur.fetchall()

    for category_id, category in categories:
        cur.execute("""SELECT ROUND(AVG(rating), 1) FROM restaurants WHERE category_id=:id""", {"id": category_id})
        rating = cur.fetchone()[0]

        dictionary[category] = rating

    sorted_dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1]))
    categories = list(sorted_dictionary.keys())
    ratings = list(sorted_dictionary.values())

    plt.figure('Extra credit: Visualize more data', figsize=(12, 6))
    plt.subplots_adjust(right=0.9, left=0.2)
    plt.barh(categories, ratings)

    plt.title('Average Restaurant Ratings by Category')
    plt.xlabel('Ratings')
    plt.ylabel('Categories')

    plt.savefig('AverageRestaurantRatings_BarChart.png')

    best_restaurant = max(dictionary, key=dictionary.get)

    return best_restaurant, dictionary[best_restaurant]


#Try calling your functions here
def main():

    list_restaurants = get_restaurant_data(DB_FILE)
    occurrences = barchart_restaurant_categories(DB_FILE)
    best_restaurant = highest_rated_category(DB_FILE)

    plt.show()

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)



if __name__ == '__main__':

    DB_FILE = 'South_U_Restaurants.db'
    main()
    unittest.main(verbosity=2)
