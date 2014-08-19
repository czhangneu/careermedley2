from glassdoor import get
# *****************************************************************************
def extract_fields(response):
    satisfaction, ceo, meta, salary = None, None, None, None
    for key, value in response.iteritems():
        if key == 'satisfaction':
            satisfaction = value
        elif key == 'ceo':
            ceo = value
        elif key == 'meta':
            meta = value
        elif key == 'salary':
            salary = value
    return (satisfaction, ceo, meta, salary)
# *****************************************************************************
def extract_satisfaction(satisfaction):
    numRatings, score = None, None
    for key, value in satisfaction.iteritems():
        if key == 'ratings':
            numRatings = value
        elif key == 'score':
            score = value
    return (numRatings, score)
# *****************************************************************************
def extract_ceo(ceo):
    numCEOReviews, approvalRate, name, avatarLink = None, None, None, None
    for key, value in ceo.iteritems():
        if key == 'reviews':
            numCEOReviews = value
        elif key == '%approval':
            approvalRate = value
        elif key == 'name':
            name = value
        elif key == 'avatar':
            avatarLink = value
    return (numCEOReviews, approvalRate, name, avatarLink)
# *****************************************************************************
def main():
    response = get('dropbox')
    print response
    print '-' * 100
    for key, value in response.iteritems():
       print "(%s: %s)" % (key, value)
    print '-' * 100
    (satisfaction, ceo, meta, salary) = extract_fields(response)
    (numRatings, score) = extract_satisfaction(satisfaction)
    (numCEOReviews, approvalRate, name, avatarLink) = extract_ceo(ceo)
    print "numRatings: %d, score: %d" % (numRatings, score)
    print "numCEOReviews: %d, approvalRate: %d, name: %s" % (numCEOReviews, approvalRate, name)

if __name__ == '__main__':
    main()