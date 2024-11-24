import constants

class Authorization:
    def IsUserAuthorized(self, headers) :
        extractSuccess, uid = self.ExtractUserIdFromIdToken(headers)

        user = self.GetUser(uid)

        extractSuccess = extractSuccess and user['emailVerified']

        return extractSuccess, uid

    def IsUserAuthorizedForWrite(self, headers, entityId) :
        extractSuccess, uid = self.ExtractUserIdFromIdToken(headers)

        user = self.GetUser(uid)

        extractSuccess = extractSuccess and user['emailVerified']

        return extractSuccess and uid == entityId

    def ExtractUserIdFromIdToken(self, headers) :
        if "AccessToken" not in headers: 
            return False, -1
        
        id_token = headers['AccessToken']

        if not id_token:
            return False, -1
        
        decoded_token = {}

        if(id_token == "abc"):
            decoded_token['uid'] = "123"
        elif(id_token == "def"):
            decoded_token['uid'] = "456"
        else:
            decoded_token['uid'] = None

        uid = decoded_token['uid']

        if not uid:
            return False, -1

        return True, uid
    
    def GetUserId(self, email):
        if(email == "harie.br@gmail.com"):
            return "123"
        elif(email == "def@test.com"):
            return "456"
        else:
            return None
    
    def GetUser(self, uid):
        if(uid == "123"):
            return {'display_name' : 'ABC', 'photo_url' : 'http://example.com', 'email' : 'harie.br@gmail.com', 'emailVerified' : True}
        
        if(uid == "456"):
            return {'display_name' : 'DEF', 'photo_url' : 'http://example.com', 'email' : 'def@test.com', 'emailVerified' : True}
       
        return {'display_name' : 'UnKnown', 'photo_url' : '', 'email' : '', 'emailVerified' : False}

    def GetAuthorizedUsers(self, db, uid):
        doc_ref = db.collection(constants.User(None)).document(uid)
        doc = doc_ref.get()

        if doc.exists:
            user = doc.to_dict()
            return user['AuthorizedUserIds']

        return []