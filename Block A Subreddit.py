#-------------------------------------------------------------------------------
# Name:        Block A Subreddit
# Purpose:     This program was written to block everyone in a subreddit, it is  easy to customise
#
# Author:      Llione684
#
# Created:     05/05/2020
# Copyright:   (c) Llione684 2020
# Licence:     <GNUGPLv3>
#-------------------------------------------------------------------------------
import praw

def main():
    print("This program blocks the first top 100 posts and all comments")
    print("This is better used on smaller subreddits, the more users, the more posts and comments, the more time to block")
    blockSub = input("What subreddit would you like to block? Type out the name exactly as it shows")
    blockFunction(blockSub)

def blockFunction(blockSub):
    #Get The Subreddit
    chosenBot = praw.Reddit("bas01")
    chosenSubreddit = chosenBot.subreddit(blockSub)

    #Get submissions
    counters = 0
    countera = 0
    listOfSorters = [chosenSubreddit.hot(limit = 1000), chosenSubreddit.new(limit = 1000), chosenSubreddit.top(limit = 1000)]
    listOfSortersPrint = ["Hot", "New", "Top"]
    for x in range(len(listOfSorters)):
        print("Sorting by", listOfSortersPrint[x])
        for post in listOfSorters[x]:
            counters += 1
            print("Post:", counters)

            #Comment out this for loop to stop the program from blocking commenters
            for comment in post.comments.list():
                try:
                    comment.author.block()
                    countera += 1
                    print("Blocked", countera)
                except:
                    print("Unable to block commenter")

            #Comment out this try block if you do not want the authors to be blocked
            try:
                post.author.block()
                countera += 1
                print("Blocked Author")
            except:
                print("Unable to block author")
                try:
                    post.hide()
                    print("Post hidden")
                except:
                    print("Unable to hide post")

            #Uncomment this try block if you would like the program to hide the  post(This is done by default if the author cannot be blocked)
            #try:
                #post.hide()
                #print("Post hidden")
            #except:
                #print("Unable to hide post")
    if counters != 0 and countera != 0:
        print("Looping again")
        blockFunction()
    else:
        print("All posters have been blocked/all posts are hidden")

main()

