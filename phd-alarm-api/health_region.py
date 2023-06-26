import dns.resolver

def active_region():
    qname = 'global.health.amazonaws.com'
    try:
        answers = dns.resolver.resolve(qname, 'CNAME')
    except Exception as e:
        raise ('Failed to resolve {}'.format(qname), e)
    if len(answers) != 1:
        raise ('Failed to get a single answer when resolving {}'.format(qname))
    name = str(answers[0].target) # health.us-east-1.amazonaws.com.
    region_name = name.split('.')[1] # Region name is the 1st in split('.') -> ['health', 'us-east-1', 'amazonaws', 'com', '']
    return region_name