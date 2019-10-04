import csv
import pandas as pd
import random
from collections import defaultdict
def getpopular():
    dict=defaultdict(int)
    sum=0
    with open('ratings.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(csvFile)
        for row in reader:
            sum+=float(row[2])
            dict[row[1]]=sum#dict is dictionary of movieid ans  sum of ratings
    #print(dict)#sum of ratings
    l=sorted(dict.items(),key=lambda x:x[1],reverse=True)
#    print(l)
#    l2=l[0:50000]#0 to 100 from tuple
    #print(len(l))
    print(l)
    l1=[]
#    print(l2)
    for i in l:
        l1.append(int(i[0]))#li is list of movies with max sum rating in decreasing order
    l1=l1[0:5000]
    print(l1)
    #print(len(l1))
    csvFile.close()
    dict1=defaultdict(list)#list of movieid and its genres
    dict4={}
    #dict2={}
    #dict3=defaultdict(list)
    with open('movies.csv','r',encoding='utf-8') as csvfile1:
        reader1=csv.reader(csvfile1)
        next(csvfile1)
        for row1 in reader1:
            c=int(row1[0])
#            if c in l1:
#                print(c)
#                key=c
            value=list(row1[2].split("|"))
            dict1[c]=value#dictionary of movieid and genres
            dict4[c]=row1[1]#dictionary of movieid and moviename
        #print(dict4)

#        print(dict1)
        #print("done")

        dict3=defaultdict(list)#dictionary of genre and movieids that corresponds to that genre
        for j in l1:
            #print(j)
            lst=dict1[j]#list of all genres of a movie
            #print(lst)
            for k in lst:
                #print(k)
                #key1=k
                dict3[k].append(j)
        #print(dict3)
        #print("done")
        #print(len(l1))
        list_of_random_movies=[]
        dict5={}#dictionary of random movie ids and their title
        for movieid in dict3.values():
            list_of_random_movies.append(random.choice(movieid))
        #print(list_of_random_movies)
        #return list_of_random_movies
        #list_of_random_movie_title=[]
        for movieid in list_of_random_movies:
            #list_of_random_movie_title.append(dict4[movieid])
            dict5[movieid]=dict4[movieid]
        #print(list_of_random_movie_title)
        #print(dict5)
        return dict5
        csvfile1.close()
#






#When we run the above program
getpopular()


def deleted_nogenre():
# reading csv file
    #check which line to be executed as lot of time required
    df=pd.read_csv("movies.csv")
    df2=df[df.genres == '(no genres listed)']['movieId']

    print(df2)
    l=list(df2)
    df1=df[~df['genres'].str.contains("(no genres listed)")]
    print(df1.head())
    print(df1.head())
    print(len(l))
    df4=pd.read_csv("ratings.csv")
    print(df4.head())
    df3=df4[~df4["movieId"].isin(l)]
    print(df3.head())
    df3.to_csv('ratings2.csv',index=False,encoding="utf-8")

    df1.to_csv('movies2.csv',index=False,encoding="utf-8")
    print("done")




#deleted_nogenre()
