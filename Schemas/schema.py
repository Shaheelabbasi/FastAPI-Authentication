def ind_serial(user):
    return {
        "id":str(user["_id"]),
        "name":user["username"],
         "email":user["email"]
    }

def list_serial(users):
    return [ind_serial(user) for user in users]


# scehmas for sending user responses 
