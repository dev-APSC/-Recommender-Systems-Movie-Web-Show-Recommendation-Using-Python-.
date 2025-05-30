import pandas as pd
from tabulate import tabulate

# Dataset from https://www.datacamp.com/datalab/datasets/dataset-r-netflix-movie-data
movies = pd.read_csv('ds.csv')
genres = []

# Converts "Genre1, Genre2, Genre3" into a set
def splitGenre(g):
	g = g.split(",")

	for i in range(0, len(g)):
		g[i] = g[i].strip()

	genres.extend(g)
	return g

def joinGenre(g):
	return ", ".join(g)

def sepChunks(seq, size):
	return list(seq[i::size] for i in range(size))

movies["genre"] = movies["listed_in"].apply(splitGenre)
movies = movies.drop(["date_added", "release_year", "listed_in", "show_id", "director", "cast", "description", "rating", "country", "duration"], axis = 1)
genres = list(set(genres))

print(tabulate(sepChunks(genres, len(genres) // 3)))

def recommend_movies(choices = [], num_recommendations = 5):
	def CalcNumberOfMatchingGenre(inp):
		x = [x.lower() for x in inp]
		return len(list(set(x).intersection(choices)))

	movies["shared_genres"] = movies["genre"].apply(CalcNumberOfMatchingGenre)

	# Filter & Sort
	similar_movies = movies.sort_values(by = "shared_genres", ascending = False)
	return similar_movies.head(num_recommendations)

choices = splitGenre(input("Enter the genres you like: "))
choices = [c.lower() for c in choices]

suggestions = recommend_movies(choices, 10)
suggestions["genre"] = suggestions["genre"].apply(joinGenre)

print(tabulate(
	suggestions,
	headers=["Type", "Name", "Genre(s)", "Matches"],
	showindex=False,
	tablefmt="github",
))
