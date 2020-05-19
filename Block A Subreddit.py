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
import tkinter

class mainScreen(tkinter.Frame):
    def __init__(self, parent, *args, **kargs):
        tkinter.Frame.__init__(self, parent, *args, **kargs)
        self.parent = parent
        self.blockSub = ""
        self.subredditText = tkinter.Label(textvariable = self.blockSub, font=("ariel",25))
        self.subredditEntry = tkinter.Entry()
        self.buttonEntry = tkinter.Button(text="Submit", command=self.setSub)

        self.commenterVar = tkinter.BooleanVar()
        self.hidePostVar = tkinter.BooleanVar()
        self.authorVar = tkinter.BooleanVar()

        self.commenterBox = tkinter.Checkbutton(text="Block commenters", variable=self.commenterVar)
        self.hidePostBox = tkinter.Checkbutton(text="Hide posts", variable=self.hidePostVar)
        self.authorBox = tkinter.Checkbutton(text="Block authors", variable=self.authorVar)

        self.subredditText.grid(row = 0, padx=25)
        self.subredditEntry.grid(row = 2)
        self.buttonEntry.grid(row=2, column = 1)
        self.commenterBox.grid(row=1, column=0)
        self.hidePostBox.grid(row=1, column=1)
        self.authorBox.grid(row=1, column=2)

    def setSub(self):
        self.blockSub = self.subredditEntry.get()
        self.subredditText.configure(text = self.blockSub)
        self.update()
        blockFunction(self.blockSub, self.commenterVar, self.hidePostVar, self.authorVar)


class consoleScreen(tkinter.Frame):
    def __init__(self, parent, *args, **kargs):
        tkinter.Frame.__init__(self, parent, *args, **kargs)
        self.parent = parent
        self.consoleBox = tkinter.Listbox(parent)

        self.consoleBox.pack()

def blockFunction(blockSub, blockCommenter, hidePosts, blockAuthors):
    #Get The Subreddit
    chosenBot = praw.Reddit("bas01")
    chosenSubreddit = chosenBot.subreddit(blockSub)

    #Get submissions
    counters = 0
    countera = 0
    listOfSorters = [chosenSubreddit.hot(limit = 1000), chosenSubreddit.new(limit = 1000), chosenSubreddit.top(limit = 1000)]
    listOfSortersPrint = ["Hot", "New", "Top"]

    consoleScreenTk = tkinter.Toplevel(mainTop)
    consoleScreenFrame = tkinter.Frame(consoleScreenTk)
    consoleScreenHolder = consoleScreen(consoleScreenFrame)
    consoleScreenFrame.pack()

    for x in range(len(listOfSorters)):
        consoleScreenHolder.consoleBox.insert("end", "Sorting by "+ listOfSortersPrint[x])
        consoleScreenHolder.update()
        for post in listOfSorters[x]:
            counters += 1
            consoleScreenHolder.consoleBox.insert("end", "Post: "+ str(counters))
            consoleScreenHolder.update()
            consoleScreenHolder.consoleBox.yview("end")

            #Comment out this for loop to stop the program from blocking commenters
            if blockCommenter.get():
                for comment in post.comments.list():
                    try:
                        comment.author.block()
                        countera += 1
                        consoleScreenHolder.consoleBox.insert("end", "Blocked "+ str(countera))
                        consoleScreenHolder.update()
                        consoleScreenHolder.consoleBox.yview("end")
                    except:
                        consoleScreenHolder.consoleBox.insert("end", "Unable to block commenter")
                        consoleScreenHolder.update()
                        consoleScreenHolder.consoleBox.yview("end")
            if hidePosts.get():
                try:
                    post.hide()
                    consoleScreenHolder.consoleBox.insert("end", "Post hidden")
                    consoleScreenHolder.update()
                    consoleScreenHolder.consoleBox.yview("end")
                except:
                    consoleScreenHolder.consoleBox.insert("end", "Unable to hide post")
                    consoleScreenHolder.update()
                    consoleScreenHolder.consoleBox.yview("end")
            if blockAuthors.get():
                try:
                    post.author.block()
                    countera += 1
                    consoleScreenHolder.consoleBox.insert("end", "Blocked Author")
                    consoleScreenHolder.update()
                    consoleScreenHolder.consoleBox.yview("end")
                except:
                    consoleScreenHolder.consoleBox.insert("end", "Unable to block author")
                    consoleScreenHolder.update()
                    consoleScreenHolder.consoleBox.yview("end")

    if counters != 0 and countera != 0:
        consoleScreenHolder.consoleBox.insert("end", "Looping again")
        consoleScreenHolder.update()
        consoleScreenHolder.consoleBox.yview("end")
        blockFunction(blockSub, blockCommenter, hidePosts, blockAuthors)
    else:
        consoleScreenHolder.consoleBox.insert("end", "All posters have been blocked/all posts are hidden")
        consoleScreenHolder.update()
        consoleScreenHolder.consoleBox.yview("end")



mainTop = tkinter.Tk()
mainTop.title("Block a subreddit")
mainTopFrame = tkinter.Frame(mainTop)
mainScreen(mainTopFrame)
mainTopFrame.grid()
mainTop.mainloop()
