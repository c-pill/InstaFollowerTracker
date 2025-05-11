import os
import pandas as pd
import instaloader

class TrackInstaFollows:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        self.followerList = "InstaFollowerList.csv"
        self.followerUpdatesList = "InstaFollowerUpdatesList.csv"
        self.newFollowers = []
        self.lostFollowers = []
            
    def startUp(self):
        print("\nFOLLOW ME NOT - Instagram Follower Tracker")
        print("\t*too much free time")
        print("\n========================================")

    def login(self):
        #user = input("Username: ")
        username = input("Username: ")
        password = input("Password: ")
        self.loader.login(username, password)
        #print("*password doesn't appear when typed")
        #self.loader.interactive_login(username=user)
        self.profile = instaloader.Profile.from_username(self.loader.context, username=username)

    def compareFollowers(self):
        print("\nGetting follower info. This may take a minute\n")
        self.followers = [follower.username for follower in list(self.profile.get_followers())]
        if os.path.exists(self.followerList):
            oldFollowers = pd.read_csv(self.followerList)['Followers'].tolist()
            self.newFollowers = [follower for follower in self.followers if follower not in oldFollowers]
            self.lostFollowers = [follower for follower in oldFollowers if follower not in self.followers]
            self.__printFollowerUpdates()   

        self.__saveFollowerInfo()

    def __saveFollowerInfo(self):
        followerData = {
            'Followers': self.followers
        }
        updateData = {
            'New Followers': [follower for follower in self.newFollowers],
            'Lost Followers': [follower for follower in self.lostFollowers]
        }
        df = pd.DataFrame(followerData)
        df.to_csv(self.followerList, index=False)
        df = pd.DataFrame(updateData)
        df.to_csv(self.followerUpdatesList, index=False)
        print(f"List of current followers saved at {self.followerList} .")
        print(f"List of follower updates saved at {self.followerUpdatesList} .")
        print()

    def __printFollowerUpdates(self):
        if len(self.newFollowers) != 0:
            print("New Followers:")
            print("++++++++++++++")
            for follower in self.newFollowers: print(follower.username)
        if len(self.lostFollowers) != 0:
            print("\nLost Followers:")
            print("---------------")
            for follower in self.lostFollowers: print(follower.username)


tracker = TrackInstaFollows()
tracker.startUp()
tracker.login()
tracker.compareFollowers()