from movies import movies
from surprise import SVD
#from surprise import SVDpp
from surprise.model_selection import cross_validate
#from content_based import MyKNNAlgo


def build_anti_test_set(trainset, user):

    fill = trainset.global_mean

    inner_user_id = trainset.to_inner_uid(str(user))
    user_movies = set([i for i,_ in trainset.ur[inner_user_id]])

    test_set = [(trainset.to_raw_uid(inner_user_id), trainset.to_raw_iid(movie), fill)
                    for movie in trainset.all_items()
                    if movie not in user_movies]

    return test_set



#making object of class movies containing all necessary fuctions
m1 = movies()
print(m1.dir_path)

#import data from ratings.csv to make trainset
data = m1.Load_dataset()

#set test user
testuser = 10
def input(x):
    testuser=x
    print('likes and dislikes of user')
    loved , hated = m1.user_choice(testuser)

    print("Movies that user likes.....\n")
    for movie in loved:
        print(movie)

    print("\nMovies that user dislikes.....\n")
    for movie in hated:
        print(movie)


    #build train set, Full trainset is used
    trainset = data.build_full_trainset()

    #build test set, Function given above as list of sets (user_id, movie_id, fill = mean_of_all_rating_in_training_set)
    test_set = build_anti_test_set(trainset, testuser)

    #selecting algo of the model
    # For collabarative filtering use SVD by uncommenting line 53
    # For content based use KNN Algorithm by uncommenting line 54
    algo = SVD()
    #algo = MyKNNAlgo()

    #training the model
    print("Training The Model...\n")
    algo.fit(trainset)

    #Getting predictions as [user_id, movies_id, true_rating, predicted_rating, status_of_prediction = False/True]
    predictions = algo.test(test_set)

    #Building list of Recommended movies as list of [movie_name, predicted_rating]
    recommend = []
    for _,movie_id,_,rating,_ in predictions:
        recommend.append([movies.movie_id_name[int(movie_id)] , rating])

    #Sorting movies in descending order with respect to predicted ratings
    recommend.sort(key = lambda x: x[1], reverse=True)

    #Printing all the recommendations
    print('Recommendations are.....\n')
    number_of_recommendations = 10
    # for movie_name,_ in recommend[:number_of_recommendations]:
        # print(movie_name)d[]
    return recommend[:10]



#For using Cross Validation uncomment following
# cross_validate(algo, data, measures=['RMSE','MAE'], cv=5, verbose=True)
