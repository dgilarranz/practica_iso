
class Chat:
    def __init__(self, id_chat):
        self.id_chat= id_chat
        self.miembros=set()


    def addMiembro(self,contacto):
        self.miembros.add(contacto)

    def getMiembros(self):
        return self.miembros

    def getID_Chat(self):
        return self.id_chat