import csv
from surprise import Dataset
from surprise import Reader
from collections import defaultdict
import os



class movies:
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    ratingpath = dir_path+'\\ratings.csv'
    moviespath = dir_path+'\\movies.csv'
    file_rating = open(ratingpath, newline='', encoding='utf8')
    file_movies = open(moviespath, newline='', encoding='utf8')
    movie_id_name = {}

    def Load_dataset(self):

        #forming the dataset
        #sep = seperatoe of csv file is ','
        #skip_lines = to skip the 1st line as it contains headings
        surprise_reader = Reader(sep=',', skip_lines=1)
        dataset = Dataset.load_from_file(self.ratingpath, surprise_reader)

        #make dictionary for movie_id to movie_name
        reader = csv.reader(self.file_movies)
        next(reader)
        data = [row for row in reader]

        for movie in data:
            self.movie_id_name[int(movie[0])] = movie[1]

        #returning the dataset of ratings.csv via surprise
        self.file_movies.seek(0)
        return dataset

    def get_user_rating(self, user):

        #initializing varibles
        found=False
        user_ratings=[]

        #reading rating.csv and getting all ratings of particular user
        reader = csv.reader(self.file_rating)

        #skip the heading of csv file and bring cursor to first element
        next(reader)

        #iterrating through each row of csv file
        for row in reader:
            userid = int(row[0])
            movie_id = int(row[1])
            if(userid == user):
                rating = float(row[2])
                user_ratings.append([movie_id, rating])
                found=True
            if(found and user!=userid):
                break
        self.file_rating.seek(0)
        #returns list containg element as [movie_id , rating]
        return user_ratings

    def user_choice(self, user):
        ratings = movies.get_user_rating(self, user)
        moviesloved = []
        movieshated = []
        for movieid,rating in ratings:
            if(rating > 4.0):
                moviesloved.append(movies.movie_id_name[movieid])
            if(rating < 3.0):
                movieshated.append(movies.movie_id_name[movieid])
        return moviesloved, movieshated

    def user_movies(self, testuser):
        watched=[]
        found=False
        reader = csv.reader(self.file_rating)
        next(reader)
        for row in reader:
            userid = int(row[0])
            testuser=int(testuser)
            if (userid==testuser):
                found = True
                watched.append(row[1])
            if (found and userid!=testuser):
                break
        return watched

    def get_genres(self):

        file_movies = open(self.moviespath, newline='', encoding='utf8')
        reader = csv.reader(file_movies)

        next(reader)

        genres = defaultdict(list)
        genres_ids = {}
        total_id = 0
        #skip = True

        for row in reader:

            movie_id = int(row[0])
            movie_genres = row[2].split('|')
            gen_id_list=[]

            #assigning the ids to different genres and adding it to gen_id_list
            for genre in movie_genres:
                #if genre == '(no genres listed)':
                #    break
                if genre in genres_ids:
                    gen_id_list.append(genres_ids[genre])
                else:
                    genres_ids[genre] = total_id
                    gen_id_list.append(total_id)
                    total_id += 1
            genres[movie_id] = gen_id_list

        #forming bit equivalent vector
        for movie_id, gen_id in genres.items():
            bit = [0] * total_id
            for item in gen_id:
                bit[item] = 1
            genres[movie_id] = bit

            
        self.file_movies.seek(0)
        return genres

    def get_year(self):

        reader = csv.reader(self.file_movies)
        next(reader)

        movie_year= {}
        for row in reader:
            movie_id = row[0]
            title = row[1]
            s= ''
            if '(' in title:
                for i in range(title.find('(')+1 , title.find(')')):
                    s += title[i]
            if s.isnumeric():
                movie_year[movie_id] = s
        self.file_movies.seek(0)        
        return movie_year
