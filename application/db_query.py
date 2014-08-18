from application.models import Position
#accts = Account.query.all()
print '-' * 100
retrieved_jobs = Position.query.all()
for job in retrieved_jobs:
    print job