
def remove_slash(*args):
    result = []

    for var in args:
        while var.startswith('/'):
            var = var[1:]

        while var.endswith('/'):
            var = var[:-1]
    
        result.append(var)

    return tuple(result)


# Check if a parameter is wrong or empty
def validations(gender, context, path, custom_path, debug, ip, ura_file_name):
    gender = 'f' if gender == 'Female' else 'm' if gender == 'Male' else 'f'
    context = 'missing_context' if context == '' else context
    path = 'global/{}'.format(gender) if path == '' else path
    custom_path = path if custom_path == '' else custom_path
    debug = '0' if debug == False else '1'
    ip = '192.168.1.99' if ip == '' else ip
    custom_path, path = remove_slash(custom_path, path)

    if ura_file_name == '' and context != 'missing_context':
        ura_file_name = context.replace('-', '_')
    
    elif ura_file_name == '' and context == 'missing_context':
        ura_file_name = 'Missing_file_name'

    if context == 'missing_context' and ura_file_name != '':
        context = ura_file_name.replace('_', '-')

    return(gender, context, path, custom_path, debug, ip, ura_file_name)