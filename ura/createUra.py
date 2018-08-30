from modules import header, body, footer
from main import CreateUra
# context - O contexto da ura
# ip - O ip do cliente
# path - O diretório de gravações globais
# custom_path - O diretório de gravações custom
# gender - O genêro da ura, pode ser "f" para feminino ou "m" para masculino

class Ura():

    def __init__(self, context, ip, path, custom_path, gender):
        self.context = context
        self.ip = ip
        self.path = path
        self.custom_path = custom_path
        self.gender = gender

# Criação da ura
localizacao = Ura("teste_localizacao", "192.168.1.100", "/var/lib/", "/etc/asterisk/", "f")

print(header(localizacao.context, localizacao.ip, localizacao.path, localizacao.custom_path, localizacao.gender))
print(body(localizacao.path, localizacao.custom_path))
print(footer())
