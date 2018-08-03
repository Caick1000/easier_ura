Steps to install the script on the server:

1 - Check the python version using 'python --version' command (no quotes)

2 - Install pip doing these commands/steps:
    1: if the version is 2.6 - 'curl https://bootstrap.pypa.io/2.6/get-pip.py -o get-pip.py'
    1: if the version is 3.3 or greater - 'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
    2: 'python get-pip.py'

    if a module is missing, just do 'pip install [module_name]'

3 - Move the script file .py to the directory /usr/local/bin

4 - Remove the .py by renaming it

4 - change permission with 'chmod 755 /usr/local/bin/shell_cria_lista'

5 - Do 'dos2unix /usr/local/bin/shell_cria_lista' to avoid extra errors


For help about how to use the command, do: 'shell_cria_lista --help'

