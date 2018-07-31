#!/usr/bin/env python
from os import path, makedirs
import errno
from time import sleep
from argparse import ArgumentParser


default_path = 'D:/talkeen/shell/'
server_default_path = '/usr/local/bin/'
file_extensions = ['csv','txt']


parser = ArgumentParser(description='Automatizacao dos script de cria_lista em shell')
parser.add_argument('-e','--extension', help='A extensao do arquivo. Por exemplo: csv', required=False, default='csv')
parser.add_argument('-n','--name', help='Nome do mailing', required=True, default='mailing_sem_nome')
parser.add_argument('-p','--path', help='Diretorio de destino do arquivo', required=True, default='/usr/local/bin/')
parser.add_argument('-f','--format', help='Formato da fila. Por exemplo: 103', required=True, default='[1-9][0-9][0-9][0-9][1-9]')
args = parser.parse_args()


def number_format(num_format):
    end_format = []
    if num_format == None:
        num_format = '[1-9][0-9][0-9][0-9][1-9]'

    if num_format.isdigit():
       num_format.split()

    for i in num_format:
        end_format.append(i)

    if len(end_format) == 4:
        end_format.append('1-9')
        num_format = end_format

    elif len(end_format) == 3:
        end_format.append('0')
        end_format.append('1-9')
        num_format = end_format
        
    num_format = '[' + end_format[0] + ']' + '[' + end_format[1] + ']' + '[' + end_format[2] + ']' + '[' + end_format[3] + ']' + '[' + end_format[4] + ']'

    return num_format



def filepath_validation(file_path):
    global default_path
    global server_default_path
    if not path.exists(default_path):
        default_path = server_default_path

    if not path.exists(default_path + file_path):
        try:
            makedirs(default_path + file_path)
            print("Exporting to => ", default_path + file_path)
            sleep(1)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                print(errno.EEXIST)
                raise



def file_extension_validation(file_extension):
    if file_extension not in file_extensions:
        file_extension = 'csv'

    if '.' in file_extension[0:]:
        file_extension = file_extension.replace('.', '')

    return file_extension



def cria_lista_shell():
    file_extension = args.extension
    name_mailling = args.name
    file_path = args.path
    num_format = args.format

    filepath_validation(file_path)

    file_extension = file_extension_validation(file_extension)

    file_name = '{0}{1}/cria_lista_{2}'.format(default_path, file_path, name_mailling)

    num_formatting = number_format(num_format)

    shell = '''
    #Conteudo para Cron
    #* * * * * /usr/local/bin/cria_lista_{0}.sh > /var/log/contact/cria_lista_{0}.log 2> /var/log/contact/cria_lista_{0}.log

    #cria a lista santander parcela
    if [ `find /tmp/{2}_{0}.{1} | wc -l` -ge 1 ]
        then        
    
        for V_LISTA in `find /tmp/{2}_{0}.{1} | cut -c6-10`
            do

                        SERVICE='listawork_{0}.sql'
            
                        if ps ax | grep -v grep | grep $SERVICE > /dev/null
                            then
                                echo "$SERVICE service running, do not rerum me"
                                exit
                            else
                                echo "$SERVICE is not running run me"
                        fi

                            sed $'s/[^[:print:]\\t]//g' /tmp/${{V_LISTA}}_{0}.{1} > /tmp/${{V_LISTA}}_santander_parcela.out
                            mv /tmp/${{V_LISTA}}_{0}.out /tmp/${{V_LISTA}}_{0}.{1}

                sed -e "s/9999/$V_LISTA/" /usr/local/bin/cria_lista_{0} > /usr/local/bin/listawork_{0}.sql

                mysql --user=root --password=atlanta@121 iogurte < /usr/local/bin/listawork_{0}.sql >  /var/log/contact/listawork_{0}.log 2> /var/log/contact/listawork{0}.log

                mv /tmp/${{V_LISTA}}_{0}.{1} /tmp/${{V_LISTA}}_{0}.{1}.importado


            done

    fi
    '''.format(name_mailling, file_extension, num_formatting)

    with open (file_name + '.sh', 'w') as shell_file:
        shell_file.write(shell)



if __name__ == '__main__':
    cria_lista_shell()