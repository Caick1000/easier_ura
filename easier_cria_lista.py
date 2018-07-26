import os
import errno

file_extensions = ['csv','txt']

def filepath_validation(file_path):
    
    if not os.path.exists(file_path):
        try:
            os.makedirs('D:/talkeen/shell/'+ file_path)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def file_extension_validation(file_extension):
    if file_extension not in file_extensions:
        file_extension = 'csv'

    return file_extension


def cria_lista_shell():
    
    file_extension = input('Whats the file extension of the mailing?')
    name_mailling = input('Whats the name of the mailing?' )
    client_name = input('Whats the name/path of the client folder?')

    filepath_validation(client_name)
    file_extension = file_extension_validation(file_extension)

    file_name = 'D:/talkeen/shell/{}/cria_lista_{}'.format(client_name, name_mailling)

    shell = '''
    #Conteudo para Cron
    #* * * * * /usr/local/bin/cria_lista_{0}.sh > /var/log/contact/cria_lista_{0}.log 2> /var/log/contact/cria_lista_{0}.log

    #cria a lista santander parcela
    if [ `find /tmp/[1-9][0-9][0-9][0-9][1-9]_{0}.{1} | wc -l` -ge 1 ]
        then
    
        for V_LISTA in `find /tmp/[1-9][0-9][0-9][0-9][1-9]_{0}.{1} | cut -c6-10`
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
    '''.format(name_mailling, file_extension)

    with open (file_name + '.sh', 'w') as shell_file:
        shell_file.write(shell)

cria_lista_shell()