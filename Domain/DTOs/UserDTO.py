class UserDTO:
    def __init__(self, id, telegramId, telegramUsername, inviteby_telegramId, joinDate):
        self.id = id
        self.telegramUsername = telegramUsername
        self.telegramId = telegramId
        self.inviteby_telegramId = inviteby_telegramId
        self.joinDate = joinDate
