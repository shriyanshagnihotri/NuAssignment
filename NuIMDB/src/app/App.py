import src.app.movieData_pb2 as movieData
from src.appException.AppException import AppException
from src.model.Model import Model


class App:
	appt = None
	movies = None
	model = None

	def __init__(self):
		self.model = Model()
		self.appt = movieData.IMDB()
		data = self.model.read_app('imdb')
		if data is not None:
			self.appt.ParseFromString(data)
		self.movies = self.appt.movies

	def check_name_unique(self, name):
		for m in self.movies:
			if m.name == name:
				raise AppException(
					'The movie with name:{} already exist please try to update the existing'
					.format(name))

	def get_movie(self, name):
		for m in self.movies:
			if m.name == name:
				return m
		return None

	def get_date_object(self, dor):
		da = dor.split("/")
		if len(da) != 3:
			raise AppException('Date provided is Invalid, should be in MM/DD/YYYY format')
		DOR = movieData.Date()
		DOR.month = int(da[0]) - 1
		DOR.date = int(da[1])
		DOR.year = int(da[2])
		return DOR

	def get_month_list(self):
		return movieData.Month.keys()

	def get_genre_list(self):
		return movieData.Genre.keys()

	def add_new_movie(self, name, dor=None, duration=None, 
		genre=None, actors=None, directors=None, reviews=None):
		self.check_name_unique(name)
		movie = self.movies.add()
		return self.__update_remaining(
			movie, name, dor, duration, genre, actors, directors, reviews)

	def __add_items(self, dest, s_list):
		del dest[:]
		for s in s_list:
			dest.append(s)

	def __add_items_reviews(self, dest, s_list):
		for s in s_list:
			k = dest.add()
			k.username = s['username']
			k.date.day = s['date']['day']
			k.date.month = s['date']['month']
			k.date.year = s['date']['year']
			k.rating = s['rating']
			k.comment = s['comment']


	def __update_remaining(self, movie, name, dor=None, duration=None, 
		genre=None, actors=None, directors=None, reviews=None):
		movie.name = name
		if dor is not None:
			movie.dor.day = dor['day']
			movie.dor.month = dor['month']
			movie.dor.year = dor['year']
		if duration is not None:
			movie.duration = duration
		if genre is not None:
			if set(genre).issubset(movieData.Genre.values()):
				self.__add_items(movie.genre, genre)
		if actors is not None:
			self.__add_items(movie.actors, actors)
		if directors is not None:
			self.__add_items(movie.directors, directors)
		if reviews is not None:
			self.__add_items_reviews(movie.reviews, reviews)
		self.model.write_app('imdb', self.appt.SerializeToString())
		return movie

	def update_movie(self, name, dor=None, duration=None, 
		genre=None, actors=None, directors=None, reviews=None):
		movie = self.get_movie(name)
		if movie is None:
			raise AppException('The movie with name:{} does not exist please try some exiting movie'.format(name))
		return self.__update_remaining(movie, name, dor, duration, genre, actors, directors, reviews)

	def get_list_movies(self):
		l = [str(m.name) for m in self.movies]
		return l

	def delete_movie(self, name):
		movie = self.get_movie(name)
		if movie is None:
			raise AppException(
				'The movie with name:{} does not exist please try some exiting movie'
				.format(name))
		self.movies.remove(movie)
		self.model.write_app('imdb', self.appt.SerializeToString())

	def find_movie_by_genre(self, genre):
		result = []
		for m in self.movies:
			if (set(m.genre).issubset(genre) or set(genre).issubset(m.genre)) and bool(set(m.genre)):
				result.append(m.name)
		return result

	def find_movie_by_actors(self, actors):
		result = []
		for m in self.movies:
			if set(m.actors).issubset(actors) or set(actors).issubset(m.actors):
				result.append(m.name)
		return result

	def find_movie_by_directors(self, directors):
		result = []
		for m in self.movies:
			if set(m.directors).issubset(directors) or set(directors).issubset(m.directors):
				result.append(m.name)
		return result

	def add_movie_proto(self, m):
		mov = movieData.Movie()
		mov.ParseFromString(m)
		return self.add_new_movie(mov.name, mov.dor, mov.duration, 
				mov.genre, mov.actors, mov.directors, mov.reviews)

	def update_movie_proto(self, m):
		mov = movieData.Movie()
		mov.ParseFromString(m)
		return self.update_movie(mov.name, mov.dor, mov.duration, 
				mov.genre, mov.actors, mov.directors, mov.reviews)

