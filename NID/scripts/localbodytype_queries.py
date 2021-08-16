from address.models import *

def run():
<<<<<<< HEAD
    LocalBodyCategory(id=102, name="Metropolitan City").save()
    LocalBodyCategory(id=103, name="Sub-MetropolitanCity").save()
    LocalBodyCategory(id=105, name="Municipality").save()
=======
    LocalBodyCategory(id=102, name="Metropolitan City", new_old=1).save()
    LocalBodyCategory(id=103, name="Sub-MetropolitanCity", new_old=1).save()
    LocalBodyCategory(id=105, name="Municipality", new_old=1).save()
>>>>>>> 8c5a1cc02a373617ea50b091b5edb8ce7a7b0d15
    LocalBodyCategory(id=119, name="Rural Municipality", new_old=1).save()
    LocalBodyCategory(id=107, name="Village Development Comittee", new_old=0).save()
