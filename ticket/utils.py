def searching(model, search_string, *args, **kwargs):
    '''
    usage e.g.:
        t = searching(ModelName, search_string, 'Foo', 'Bar', **kwargs)
        tmp = ModelName.objects.none()
            for i in t:
                tmp = i | tmp #merge Querysets
    :param model: Django Modelobject
    :param search_string: self explaning
    :param args: datatypes that should be excluded
    :param kwargs: can contain exlude or exact as key with a list of values containing the field name/-s
    :return: list of querysets gte 1
    '''
    types = [field.get_internal_type() for field in model._meta.get_fields()]
    names = [f.name for f in [field for field in model._meta.get_fields()]]
    field_name_dict = dict(zip(names, types))
    excat_fields = []

    if kwargs:
        if 'exclude' in kwargs:
            field_name_dict = remove_items_dict(field_name_dict, kwargs['exclude'])
        elif 'exact' in kwargs:
            excat_fields = kwargs['exact']
        else:
            # to use following e.g. in function call:
            # data = {'exclude': liste['foo', ]}
            # searching(modelname, searchstring, kwargs=data)
            if 'exclude' in kwargs['kwargs']:
                field_name_dict = remove_items_dict(field_name_dict, kwargs['kwargs']['exclude'])
            elif 'exact' in kwargs:
                excat_fields = kwargs['exact']

    if args:
        field_name_dict = remove_items_dict(field_name_dict, args)

    tmp = model.objects.all()
    liste = []

    for key, value in field_name_dict.items():
        if value != 'ForeignKey':
            if key in excat_fields:
                filter = f'{key}__iexact'
                if len(tmp.filter(**{filter: search_string})) > 0:
                    liste.append(tmp.filter(**{filter: search_string}))
            else:
                filter = f'{key}__icontains'
                if len(tmp.filter(**{filter: search_string})) > 0:
                    liste.append(tmp.filter(**{filter: search_string}))
        else:
            filter = f'{key}__pk__iexact'
            if len(tmp.filter(**{filter: search_string})) > 0:
                liste.append(tmp.filter(**{filter: search_string}))
            else:
                filter = f'{key}__name__icontains'
                if len(tmp.filter(**{filter: search_string})) > 0:
                    liste.append(tmp.filter(**{filter: search_string}))
    return liste


def remove_items_dict(dictionary, keys):
    '''
    Remove items from dictonary
    :param dictionary:
    :param keys:
    :return:
    '''
    return {key: value for key, value in dictionary.items() if key not in keys and value not in keys}