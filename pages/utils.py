

LANGUAGE_CHOICES =( 
    ("1", "English"), 
    ("2", "Spanish"), 
    ("3", "French"), 
    ("4", "German"), 
    )


def from_label_to_value(request,field):
    
    if field == 'speaks':
        labels = request.user.profile.speaks
    else:
        labels = request.user.profile.is_learning

    if labels is not None:
        values = [value for value, label in LANGUAGE_CHOICES if label in labels]
        values = [int(i) for i in values]
    else:
        values = ''

    return values