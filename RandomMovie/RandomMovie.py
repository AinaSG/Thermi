import os
import io
import datetime
import re
import requests
from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2 import Environment


class Movie():
    def __init__(self, title, sinopsis, genres, rating_percent, poster_url):
        self.title = title
        self.sinopsis = sinopsis
        self.genres = genres
        self.rating_percent = rating_percent
        self.poster_url = poster_url


class RandomMovie():

    def __init__(self):
        self.debug('RM_Init', 'New RandomMovie')

    def generate(self):
        movie = self.get_rand_movie()
        out_html = self.render_html(movie)
        out_file = io.open("./tmp/rand_movie_out.html", 'w', encoding='utf8')
        out_file.write(out_html)
        out_file.close()
        self.debug('RM_generate', 'Finished!')
        return("./tmp/rand_movie_out.html")

    def get_rand_movie(self):

        self.debug('RM_get', 'Getting Rand movie')

        movie = requests.get("https://tv-v2.api-fetch.website/random/movie")
        json_movie = movie.json()

        title = json_movie["title"]
        sinopsis = json_movie["synopsis"]
        genres = json_movie["genres"]
        rating_percent = json_movie["rating"]["percentage"]
        poster_url = "movieposter"
        
        self.debug('RM_get', 'Downloading image...')
        #Es necessari baixar la imatge per poguer ferli dittering
        poster_data = requests.get(json_movie["images"]["poster"]).content
        with open('./tmp/movieposter', 'wb') as handler:
            handler.write(poster_data)
        self.debug('RM_get', 'Creating and returning movie')
        rMovie = Movie(title, sinopsis, genres, rating_percent, poster_url)

        return rMovie
    
    def render_html(self, movie):
        self.debug('RM_pdf', 'INIT HTML creation')
        templateLoader = FileSystemLoader( searchpath="./RandomMovie")
        templateEnv = Environment( loader=templateLoader )
        TEMPLATE_FILE = "template.html"
        template = templateEnv.get_template( TEMPLATE_FILE )
        rating = self.get_stars(movie.rating_percent)
        return template.render(movie=movie,fill_st=rating["fill"], half_st=rating["half"], empt_st=rating["empt"])
        
    def get_stars(self, rating):
        result = {}
        fill = rating//10
        half = 0
        if(rating%10 >5):
            fill = fill +1
        if(rating%10<=5 and rating%10!=0):
            half = 1
        empt = 10-half-fill
        self.debug('RM_stars', 'Original Percentage: %s' %str(rating))
        self.debug('RM_stars', 'Full: %s' %str(fill))
        self.debug('RM_stars', 'Half: %s' %str(half))
        self.debug('RM_stars', 'Empt: %s' %str(empt))
        result["fill"] = fill
        result["half"] = half
        result["empt"] = empt
        return result


    def debug(self, section, log):
        date = datetime.datetime.today()
        print '[%s - %s] %s' % (date.strftime('%Y-%m-%d %H:%M:%S'),
                                section, log)
