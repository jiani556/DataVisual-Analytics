import csv
import json
import time
import tweepy

##Collecting and visualizing Twitter data
##use the Twitter REST API to retrieve ​friends and ​followers on Twitter.

# must use Python 2.7.x

# 1 point
def loadKeys(key_file):
    # NOTE: put  keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>

    # Load keys here and replace the empty strings in the return statement with those keys
    with open(key_file) as key:
        keys=json.load(key)
    return keys['api_key'], keys['api_secret'], keys['token'], keys['token_secret']

# 4 points
def getPrimaryFriends(api, root_user, no_of_friends):
    # NOTE: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    # Add code here to populate primary_friends
    friends_num = api.get_user(screen_name=root_user).friends_count
    if friends_num < no_of_friends:
        no_of_friends=friends_num
    primary_friends_list=tweepy.Cursor(api.friends,screen_name=root_user).items(no_of_friends)
    while True:
        try:
            friends=primary_friends_list.next()
            primary_friends.append((root_user,friends.screen_name))
        except tweepy.error.RateLimitError:
            print "waiting..."
            time.sleep(60 * 5)
            print "continue..."
            continue
        except StopIteration:
            break

    return primary_friends


# 4 points
def getNextLevelFriends(api, users_list, no_of_friends):
    # NOTE: implement the method for fetching 'no_of_friends' friends for each user in users_list
    # rtype: list containing entries in the form of a tuple (user, friend)
    next_level_friends = []
    # Add code here to populate next_level_friends
    for friends in users_list:
        friends_num = api.get_user(screen_name=friends[1]).friends_count
        if friends_num < no_of_friends:
            next_friends_list=tweepy.Cursor(api.friends,screen_name=friends[1]).items(friends_num)
        else:
            next_friends_list=tweepy.Cursor(api.friends,screen_name=friends[1]).items(no_of_friends)

        while True:
            try:
                next_friends=next_friends_list.next()
                next_level_friends.append((friends[1],next_friends.screen_name))
            except tweepy.error.RateLimitError:
                print "waiting..."
                time.sleep(60 * 5)
                print "continue..."
                continue
            except StopIteration:
                break

    return next_level_friends

# 4 points
def getNextLevelFollowers(api, users_list, no_of_followers):
    # NOTE: implement the method for fetching 'no_of_followers' followers for each user in users_list
    # rtype: list containing entries in the form of a tuple (follower, user)
    next_level_followers = []
    # Add code here to populate next_level_followers

    for friends in users_list:
        followers_num = api.get_user(screen_name=friends[1]).followers_count
        if followers_num < no_of_followers:
            next_followers_list=tweepy.Cursor(api.followers,screen_name=friends[1]).items(followers_num)
        else:
            next_followers_list=tweepy.Cursor(api.friends,screen_name=friends[1]).items(no_of_followers)

        while True:
            try:
                next_followers=next_followers_list.next()
                next_level_followers.append((next_followers.screen_name,friends[1]))
            except tweepy.error.RateLimitError:
                print "waiting..."
                time.sleep(60 * 5)
                print "continue..."
                continue
            except StopIteration:
                break

    return next_level_followers

# 3 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # NOTE:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends.
    all_edges = []
    primary_friends=getPrimaryFriends(api,root_user,no_of_neighbours)
    users_list=primary_friends
    next_level_friends=getNextLevelFriends(api,users_list,no_of_neighbours)
    next_level_followers=getNextLevelFollowers(api,users_list,no_of_neighbours)
    for i in next_level_friends:
        if i not in primary_friends:
            primary_friends.append(i)
    for i in next_level_followers:
        if i not in primary_friends:
            primary_friends.append(i)
    all_edges=primary_friends
    #Add code here to populate all_edges
    return all_edges


# 2 points
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    with open(output_file,'wb') as f:
       writer = csv.writer(f)
       for row in data:
           writer.writerow(row)
    pass

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)

    writeToFile(edges, OUTPUT_FILE_GRAPH)


if __name__ == '__main__':
    testSubmission()
