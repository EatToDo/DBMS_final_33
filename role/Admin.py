from .User import User
from action.adminsong.ManageSong import ManageSong
from action.adminalbum.ManageAlbum import ManageAlbums 
from action.adminartist.ManageArtist import ManageArtist
from action.adminperformance.ManagePerformance import ManagePerformance
from action.adminSnomination.ManageSNomination import  ManageSongNominations
from action.adminAnomination.ManageANomination import ManageAlbumNominations
from action.adminArtistNomination.ManageArtistNomination import ManageArtistNominations
from action.adminSongAward.ManageSongAward import ManageSongAward
from action.adminArtistAward.ManageArtistAward import ManageArtistAward
from action.adminAlbumAward.ManageAlbumAward import ManageAlbumAward
from action.adminceremony.ManageCeremony import ManageCeremony
from action.admincomment.ManageComments import ManageComments
from action.adminvote.ManageVotes import ManageVotes
class Admin(User):
    def __init__(self, userid, username, pwd, gender, bdate):
        super().__init__(userid, username, pwd, gender, bdate)
        self.user_action = super().get_available_action() + [
           ManageSong("Manage Songs"),
            ManageAlbums("Manage Albums"),
            ManageArtist("Manage Artists"),
            ManagePerformance("Manage Performances"),
            ManageSongNominations("Manage Song Nominations"),
            ManageAlbumNominations("Manage Album Nominations"),
            ManageArtistNominations("Manage Artist Nominations"),
            ManageSongAward("Manage Song Awards"),
            ManageArtistAward("Manage Artist Awards"),
            ManageAlbumAward("Manage Album Awards"),
            ManageCeremony("Manage Ceremonies"),
            ManageComments("View Comments"),
            ManageVotes("Manage Votes")
            

        ]

    def isAdmin(self):
        return True
