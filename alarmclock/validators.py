from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger('validator')

artist_value = None

def validate_days(sender, instance, **kwargs):

    days = instance.day
    logger.debug("validator days len = %s", len(days))
    logger.debug("validator days instance = %s", days)
    if len(instance.day) > 1:
        for i in range(0,len(days)):
            logger.debug("daily == %s",i)
            logger.debug("dailys == %s", days[i])
            if days[i] == 'DAILY':
                logger.error("There is a daily and other day")
                return "You can't choose daily and another day"
            else:
                logger.debug("no issue with the days")



def validate_artist(value):

    logger.debug("artist value : %s", value)
    global artist_value
    artist_value = value
    return value

def validate_playlist(value):

    logger.debug("validate playlist value : %s", value)
    logger.debug("validate artist value : %s", artist_value)

#    return value


    if artist_value == None and value == 0:
        logger.error("Either Artist or Playlist has to be chosen")
        raise ValidationError("Either Artist or Playlist has to be chosen")
    else:
        logger.debug("valid")
        return value
