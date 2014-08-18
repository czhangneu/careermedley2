from application.models import Position
print Position.query.whoosh_search('post').all()
print '*' * 100
softwares = Position.query.whoosh_search('software').all()
for pos in softwares:
    print pos.jobtitle, pos.state, pos.city
print '*' * 100
pythons = Position.query.whoosh_search('python').all()
for pos in pythons:
    print pos.jobtitle, pos.state, pos.city
print '*' * 100
mls = Position.query.whoosh_search('machine learning').all()
for pos in mls:
    print pos.jobtitle, pos.state, pos.city
print '*' * 100