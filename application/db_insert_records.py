# #from models import Employer
# from glassdoor_test0 import *
# employers = ['Google', 'Facebook', 'amazon.com']
# #print get('Amazon.com')
# for employer in employers:
#     response = get(employer)
#     if response:
#         (satisfaction, ceo, meta, salary) = extract_fields(response)
#         (numRatings, score) = extract_satisfaction(satisfaction)
#         print employer, numRatings, score
#     else:
#         print "employer doesn't exist"

#import time
import datetime

from application import db
from application.models import Position
from job_search import ProcessJobSearch

#from models import db

query, location = 'python', 'Boston'
getJobs = ProcessJobSearch()
jobs = getJobs.job_search(query, location)
for job in jobs:
    city, jobtitle, company, snippet, jobkey= None, None, None, None, None
    state, url, date, expired= None, None, None, None
    for key, value in job.iteritems():
        if key == 'city':
            city = value
        elif key == 'jobtitle':
            jobtitle = value
        elif key == 'company':
            company = value
        elif key == 'snippet':
            snippet = value
        elif key == 'state':
            state = value
        elif key == 'jobkey':
            jobkey = value
        elif key == 'url':
            url = value
        elif key == 'date':
            date = value
        elif key == 'expired':
            expired = value
    #print city, jobtitle, company, snippet, jobkey
    #cur_pos = Position()
    # original date format: 15 Aug 2014 06:29:22 GMT
    datestamp = date.split(',')[1].lstrip(' ').rstrip(' GMT')
    # datetime.strptime() is a convenient way to convert them to datetime instances
    print datestamp
    datestamp = datetime.datetime.strptime(datestamp, "%d %b %Y %H:%M:%S")
    #print datestamp
    #print expired, (expired == False)
    print snippet
    position = Position(jobkey, company, jobtitle, city, state,
                 snippet, datestamp, url, expired)
    positions_same_jobkeys = Position.query.filter_by(jobkey=jobkey).first()
    if positions_same_jobkeys is not None:
        pass
    else:
        db.session.add(position)
        db.session.commit()

print '-' * 100
retrieved_jobs = Position.query.all()
for job in retrieved_jobs:
    print job

from application.models import Employer
# -----------------------------------------------------
# insert multiple records for table: employer
from glassdoorapi import *

employers = ['Google', 'Facebook', 'amazon.com', 'Pivotal', 'Intuit',
             'salesforce.com', 'Qualcomm', 'Zappos', 'NetApp',
             'EMC', 'Microsoft', 'Cisco', 'Twitter', 'LinkedIn',
             'ebay', 'Palantir', 'Intel', 'Mathworks', 'Rackspace',
             'Dropbox', 'box', 'Akamai', 'Juniper', 'IBM',
             'citrix', 'Paypal', 'Factset', 'Uber', 'airbnb',
             'HP', 'evernote', 'cloudera', 'Pinterest', 'Tableau']
#print get('Amazon.com')
for employer in employers:
    response = get(employer)
    print response
    try:
        if response:
            (satisfaction, ceo, meta, salary) = extract_fields(response)
            #if isinstance(satisfaction, dict) and isinstance(ceo, dict) and isinstance(meta, dict):
            try:
                (num_ratings, score) = extract_satisfaction(satisfaction)
                (num_ceo_reviews, ceo_approval, ceo_name, avatarLink) = extract_ceo(ceo)
                print ', '.join([str(employer), str(num_ratings), str(score),
                             str(num_ceo_reviews), str(ceo_approval), str(ceo_name)])
                # insert to table: Employer
                cur_employer = Employer.query.filter_by(employer_name=employer).first()
                # to see if exists already, if exist, update corresponding field
                if cur_employer:
                    #pass
                    cur_employer.num_ratings = num_ratings
                    cur_employer.score = score
                    cur_employer.ceo_name = ceo_name
                    cur_employer.num_ceo_reviews = num_ceo_reviews
                    cur_employer.ceo_approval = ceo_approval
                else:
                    cur_employer = Employer(employer, num_ratings, score, ceo_name,
                     num_ceo_reviews, ceo_approval)
                    db.session.add(cur_employer)
            #except (RuntimeError, TypeError, NameError, ValueError, AttributeError):
            except:
                continue
        else:
            print "employer doesn't exist"
    except:
        continue
db.session.commit()

# verify insertions
print '-' * 100
retrieved_employers = Employer.query.all()
for employer in retrieved_employers:
    print employer