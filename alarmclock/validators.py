from django.core.exceptions import ValidationError
from operator import xor
import logging

logger = logging.getLogger('validator')

#defining the global variables that will be used
artist_value = None
daily_value = None

#defining the error messages
artist_playlist_err_msg = "Either Artist or Playlist has to be chosen"


def validate_daily(value):

    logger.debug("validate_daily")
    '''
    this function will check if the values of the daily option and the days_value.
    if both have values, it will raise an exception.
    '''

    global daily_value   # using the global variable days_value
    daily_value = value
    logger.debug("daily_value : %s",daily_value)
#    logger.debug("days_counter = %s, daily_counter = %s",days_counter ,daily_counter )
#    logger.debug("xor : %s",xor(value, bool(days_value)))

    '''
    if xor(value, bool(days_value)) == False:
        logger.error("msg : %s", days_daily_err_msg)
        raise ValidationError(days_daily_err_msg)
    else:
        logger.debug("the daily_day validator passed")
        days_value = None #resetting the days_value
    '''

def validate_days(sender, instance, **kwargs):

    logger.debug("validate_days")
    global daily_value # making the days variable global

    logger.debug("daily_value at validate_days : %s",daily_value)
    days = instance.day
    logger.debug("days = %s",bool(len(days)))

    '''just to show the selected days'''
    if len(instance.day) > 1:
        for i in range(0,len(days)):
            logger.debug("daily == %s",i)
            logger.debug("dailys == %s", days[i])

    ''' using the xor because we have to have only one value True '''
    if xor(daily_value, bool(len(days))) == False:
        logger.error("msg : %s", days_daily_err_msg)
#        raise ValidationError(days_daily_err_msg)
    else:
        logger.debug("the daily_day validator passed")



def validate_artist(value):

    '''
    this function sets the artist_value as global and assigns it the value it receives from the model.
    The default value is None
    '''

    global artist_value
    logger.debug("artist value : %s and global artist_value : %s ", value, artist_value)
    artist_value = value



def reset():

    global artist_value
    artist_value = None

def validate_playlist(value):

    global artist_value
    ''' this function checks the value of the artist and the playlist '''
    logger.debug("validate playlist value : %s", value)
    logger.debug("validate artist value : %s", artist_value)


    if artist_value == None and value == 0:
        """ 
        if both are None and 0 , means neither an artist or a playlist has been chosen.
        A ValidationError will be thrown to the model -> form. 
        """
        logger.error("msg : %s", artist_playlist_err_msg)
        raise ValidationError(artist_playlist_err_msg)
    else:
        logger.debug("valid")
        artist_value = None  #resetting the artist_value

