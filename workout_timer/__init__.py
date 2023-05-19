
def seconds_to_time(seconds):
    '''Convert seconds to a time string.'''
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    if hour == 0:
        return '%02d:%02d' % (min, sec)
    else:
        return '%d:%02d:%02d' % (hour, min, sec)
