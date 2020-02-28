
from datetime import datetime

def create_user(self, user_datastore, db):
    user = user_datastore.create_user(email='admin@taskbook.com',
                                      first_name='Benjamin',
                                      last_name='Rosario',
                                      password='adminfl119',
                                      phone_number='(829) 359 4707',
                                      country='DO',
                                      gender='M',
                                      confirmed_at=datetime.now())
    default_role = user_datastore.find_role(role="Admin")
    user_datastore.add_role_to_user(user, default_role)
    db.commit()
