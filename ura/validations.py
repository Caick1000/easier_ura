
def remove_slash(*args):
    result = []

    for var in args:
        if var.startswith('/'):
            var = var[1:]

        if var.endswith('/'):
            var = var[:-1]
    
        result.append(var)

    return tuple(result)


# Check if a parameter is wrong or empty
def validations(gender, context, path, custom_path, debug, ip):
    gender = 'f' if gender == 'Female' else 'm' if gender == 'Male' else 'f'
    context = 'missing_context' if context == '' else context
    path = 'global/{}'.format(gender) if path == '' else path
    custom_path = path if custom_path == '' else custom_path
    debug = '0' if debug == False else '1'
    ip = 'missing_ip' if ip == '' else ip

    custom_path, path = remove_slash(custom_path, path)

    return(gender, context, path, custom_path, debug, ip)