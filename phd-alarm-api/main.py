import boto3
import datetime
import logging
from health_client import HealthClient

logging.basicConfig(level=logging.INFO)

def event_details(profile, event):
    event_details_response = HealthClient().client(profile).describe_event_details(eventArns=[event['arn']])
    for event_details in event_details_response['successfulSet']:
        logging.info('Details: %s, description: %s', event_details['event'], event_details['eventDescription'])    

def describe_events(profile):
    events_paginator = HealthClient().client(profile).get_paginator("describe_events")
    test = HealthClient().client(profile)
    print(test)
    # Describe events using the same default filters as the Personal Health
    # Dashboard (PHD). i.e
    #
    # Return all open or upcoming events which started in the last 7 days,
    # ordered by event lastUpdatedTime

    events_pages = events_paginator.paginate(filter={
        'startTimes': [
            {
                'from': datetime.datetime.now() - datetime.timedelta(days=7)
            }
        ],
        'eventStatusCodes': ['open', 'upcoming']
    })

    number_of_matching_events = 0
    for events_page in events_pages:
        for event in events_page['events']:
            number_of_matching_events += 1
            event_details(profile, event)

    if number_of_matching_events == 0:
        logging.info('There are no AWS Health events that match the given filters')

for profile in boto3.session.Session().available_profiles:
    if "admin" in profile:
        print(profile)
        describe_events(profile)
        print("=========================================================================")
    else:
        pass