from src.app.App import App
import src.protobuf_json as pj
from src.appException.AppException import AppException
import json

class movieView:
	app = None
	def __init__(self):
		self.app = App()

	def perform_add(self, a):
		data = json.loads(a)
		return pj.pb2json(self.app.add_new_movie(data['name'], data['dor'], 
			data['duration'], data['genre'], data['actors'], data['directors'], 
			data['reviews'])), "Movie Added"

	def perform_update(self, a):
		data = json.loads(a)
		return pj.pb2json(self.app.update_movie(data['name'], data['dor'], 
			data['duration'], data['genre'], data['actors'], data['directors'], 
			data['reviews'])), "Movie Updated"

	def perform_list(self, a):
		return json.dumps(self.app.get_list_movies()), "Movies Listed"

	def perform_delete(self, a):
		self.app.delete_movie(a)
		return "", "Movie Deleted"

	def perform_find_genre(self, a):
		return json.dumps(self.app.find_movie_by_genre(
			[int(k) for k in a.split(',') if k.strip() != ""])), "Movies Listed"

	def perform_find_actor(self, a):
		return json.dumps(self.app.find_movie_by_actors(a.split(','))), 
		"Movies Listed"

	def perform_find_director(self, a):
		return json.dumps(self.app.find_movie_by_directors(a.split(','))), 
		"Movies Listed"

	def perform_get_movie(self, a):
		return pj.pb2json(self.app.get_movie(a)), "Movie Listed"

	def perform_add_pro(self, a):
		return self.app.add_movie_proto(a), "Movie Added"

	def perform_update_pro(self, a):
		return self.app.update_movie_proto(a) , "Movie Updated"
