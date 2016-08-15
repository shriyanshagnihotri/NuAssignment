from src.view.movieView import movieView
from src.appException.AppException import AppException
import sys

def cmd_format():
	print "cmd format is:\npython NuIMDB <add/update/find_by{genre, directors, actors}/list/delete data_in_json"

if len(sys.argv) != 3:
	print "Invalid command"
	cmd_format()
	sys.exit(-1)

def bail(a):
	return "Nothing"

a = movieView()
functions = {'add': a.perform_add, 'update': a.perform_update, 'find_by_genre':
			 a.perform_find_genre, 'find_by_director': a.perform_find_director, 
			 'find_by_actor': a.perform_find_actor, 'delete': a.perform_delete, 
			 'list_movies': a.perform_list, 'bail': bail, 
			 'get_movie': a.perform_get_movie}
op, action = functions.get(sys.argv[1], bail)(sys.argv[2])
print op, action
