

LANGUAGE_CHOICES =( 
    ("1", "English"), 
    ("2", "Spanish"), 
    ("3", "French"), 
    ("4", "German"),
    ("5", "Italian"),
    ("6", "Russian"),
    )


def from_label_to_value(request,field):
    
    if field == 'speaks':
        labels = request.user.profile.speaks
    else:
        labels = request.user.profile.is_learning

    if labels is not None:
        # French, German
        values = [value for value, label in LANGUAGE_CHOICES if label in labels]
        # ['3','4']
        values = [int(i) for i in values]
    else:
        values = ''

    return values


def sort(elements,results,l_s=False,l_l=False):
    if len(elements)>1:
        for e in range(len(elements)):
            if e == 0:
                continue

            if l_s:
                results = results.filter(speaks__icontains=elements[e])
            if l_l:
                results = results.filter(is_learning__icontains=elements[e])
    
    return results