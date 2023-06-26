import boto3
from health_region import active_region

class ActiveRegionHasChangedError(Exception):
    """Rasied when the active region has changed"""
    pass

class HealthClient:
    __active_region = None
    __client = None
    __session = None
    
    @staticmethod
    def client(profile):
        if not HealthClient.__active_region:
            HealthClient.__active_region = active_region()
        else:
            current_active_region = active_region()
            if current_active_region != HealthClient.__active_region:
                old_active_region = HealthClient.__active_region
                HealthClient.__active_region = current_active_region

                if HealthClient.__client:
                    HealthClient.__client = None

                raise ActiveRegionHasChangedError('Active region has changed from [' + old_active_region + '] to [' + current_active_region + ']')

        if not HealthClient.__client:
            HealthClient.__session = boto3.Session(profile_name=profile, region_name=HealthClient.__active_region)
            # HealthClient.__client = HealthClient.__session.client('health')

        # return HealthClient.__client
        return HealthClient.__session.client('health')