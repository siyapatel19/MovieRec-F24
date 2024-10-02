## Scraping for Letterboxd using BeautifulSoup and requests

# imports used
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# Method to scrape a given users username and get information about the users ratings
def scrap_letterboxd(username: str):
    # Given the username, create the letterboxd url so we can scrap the movies
    url = "https://letterboxd.com/" + username.strip() + "/films/page/1/"

    # Initialize the regular expressions which will scan the soup file
    # for all of the movie names and star ratings.
    regex_movie_name_slug = re.compile(r'data-film-slug="([^"]+)"')
    regex_movie_ratings = re.compile(r"rated-(\d+)")

    # Make the soup to pull everything off the persons letterboxd webpage.
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    print(soup)
    # Now find everything from only the actual movie section of the webpage, not the other info
    film_html = soup.find_all("li", class_=re.compile(r"poster-container"))
    # print(film_html)
    # Not, using regex, we get all the movie names and ratings from the HTML file.
    # This automatically creates a list
    movie_names_slug = re.findall(regex_movie_name_slug, str(film_html))
    movie_ratings = re.findall(regex_movie_ratings, str(film_html))

    # Return the results
    return movie_names_slug, movie_ratings


# Method to scrape a giving letterboxd username and return a dataframe with the movie names and the star ratings.
def scrape_and_make_dataframe(username: str) -> pd.DataFrame:
    # Scrap the movies and ratings from the given letterboxd username
    (movie_names_slug, movie_rating) = scrap_letterboxd(username)

    # Convert the ratings from string to integer using list comprehension
    int_movie_ratings = [int(i.split()[0]) for i in movie_rating]

    # Make a list of size (movie_name) for the usernames, Not necessary just included it
    username_list = [username] * len(movie_names_slug)

    # movie_name = ["Longlegs", "Challengers", "The Fall Guy", "Dune: Part Two", "Oppenheimer",
    #               "Barbie", "The Batman", "Spider-Man: No Way Home", "Dune"]

    # Return the results as a Pandas dataframe
    # return pd.DataFrame(
    #     {"username": username_list[:9], "Movie_name": movie_name, "Movie_name_slug": movie_names_slug[:9], "star_rating": int_movie_ratings[:9]}
    # )
    return pd.DataFrame(
        {"username": username_list, "Movie_name_slug": movie_names_slug, "star_rating": int_movie_ratings}
    )

# Sample use
username = input("Please type your letterboxd username : ")
print(f"Now scraping : {username}")
df = scrape_and_make_dataframe(username.strip())
# df.to_csv("./data/sample_user_data.csv")
print(df)
