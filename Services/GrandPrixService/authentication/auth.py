from firebase_admin import auth
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
        
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        if not uid:
            return False, -1

        return True, uid
    
    def GetUserId(self, email):
        try:
            ret =  auth.get_user_by_email(email)
            #print(ret)
            return ret.uid
        except:
            return None

    def GetUser(self, uid):
        try:
            ret =  auth.get_user(uid)
            #print(ret)
            return {'display_name' : ret.display_name, 'photo_url' : ret.photo_url, 'email' : ret.email, 'emailVerified' : ret.email_verified }
        except:
            return {'display_name' : 'Unknown', 'photo_url' : '', 'email' : '', 'emailVerified' : False}

    def GetAuthorizedUsers(self, db, uid, sharedState):
        doc_ref = db.collection(constants.User(sharedState)).document(uid)
        doc = doc_ref.get()

        if doc.exists:
            user = doc.to_dict()
            return user['AuthorizedUserIds']

        return []