# Check if a parameter is wrong or empty
def validations(gender, context, path, custom_path, debug, ip):
    gender = 'f' if gender == 'Female' else 'm' if gender == 'Male' else 'f'
    context = 'missing_context' if context == '' else context
    path = 'global/{}'.format(gender) if path == '' else path
    custom_path = path if custom_path == '' else custom_path
    debug = '0' if debug == False else '1'
    ip = 'missing_ip' if ip == '' else ip

    if custom_path[:-1] == '/' or custom_path[:-1] == '\\':
        custom_path = custom_path[:-1]

    if custom_path[0:] == '/' or custom_path[0:] == '\\':
        custom_path = custom_path[0:]

    if path[:-1] == '/' or path[:-1] == '\\':
        path = path[:-1]

    if path[0:] == '/' or path[0:] == '\\':
        path = path[0:]

    return(gender, context, path, custom_path, debug, ip)