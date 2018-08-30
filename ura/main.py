from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from modules import header, body, footer
from datetime import datetime

current_date = datetime.now().strftime("%Y/%m/%d")
class CreateUra(GridLayout):
    
    def uraConfig(self):
        global context
        context = self.ids.context_input.text
        ip = self.ids.ip_input.text
        path =self.ids.path_input.text
        custom_path = self.ids.custom_path_input.text
        gender = self.ids.gender_input.text

        layout = ''';-----------------------------------------------------------------------------------------------------------------------------
        ;-----------------------------------------------------------------------------------------------------------------------------

        ;/*
        ;TALKEEN - {context}
        ;DATA: {current_date}
        ;*/

        ;-----------------------------------------------------------------------------------------------------------------------------
        ;-----------------------------------------------------------------------------------------------------------------------------
        [{context}]
        exten => _X!,1,Set(LINHA_ID=${{EXTEN}})

            same=>n,Set(IP_FILE_GRAMMAR={ip})
            same=>n,Set(DEBUG=0)
            same=>n,Set(GRAMMAR_GLOBAL_DIR=http://${{IP_FILE_GRAMMAR}}/grammar/global)
            same=>n,Set(V_GENDER={gender})
            same=>n,Set(SOUND_DIR={path})
            same=>n,Set(SOUND_DIR_CUSTOM={custom_path}}})
            same=>n,Set(SOUND_DIR_NOME=global/nomes)
            same=>n,Set(V_IVR=${{context}})
            same=>n,Set(CHANNEL(language)=pt)

            same=>n,Gosub(modulo_init,s,1(${{IP_FILE_GRAMMAR}}))
            same=>n,Set(COD_LIG=DISO)
            same=>n,GotoIf($[ '${{DEBUG}}' = '1' ]?humano)
            same=>n,Gosub(modulo_amd_rec_voz,s,1(${{IP_FILE_GRAMMAR}}))

            same=>n(humano),NoOp(Executando ${{V_IVR}})
            same=>n,NoOp('COD_LIG => '${{COD_LIG}})
            same=>n,NoOp('SECE => '${{SECE}})
        ;===========================================================================================
        ;coletar_variaveis
        ;===========================================================================================
            same=>n(coletar_variaveis),NoOp(coletar_variaveis);

            ;VARIAVEIS
            same=>n,Set(DDD=11)
            same=>n,Set(FONE=942201531)
            same=>n,Set(NOME=Augusto)
            same=>n,Set(COD_LINK_INT=1)
            same=>n,Set(COD_LINK_CHAR=1)
            same=>n,Set(CPF=12345678901)

        ;===========================================================================================

        ;===========================================================================================
        ;saudacao
        ;===========================================================================================
            same=>n(saudacao),NoOp(saudacao)
            same=>n,GotoIf($[ '${{DEBUG}}' = '1' ]?saudacao_inicio)
            same=>n,Set(FILE(${{gCAMI}},,,la,u)={{'origem':'dialplan','comando':'ligAtendida','linha_id':'${{LINHA_ID}}','canal':'${{CHANNEL(name)}}','retorno':'false'}})  
            same=>n,Set(FILE(${{gCAMI}},,,la,u)={{'origem':'dialplan','comando':'criaVariaveis','linha_id':'${{LINHA_ID}}','canal':'${{CHANNEL(name)}}','retorno':'false','linha_info':'ddd|fone|nome_cliente|id_tabela_disca|cod_link_int|cod_link_char|contrato|valor|cpf|idusuario','fila_info':'fila_transfer'}})
            same=>n(saudacao_inicio),Gosub(modulo_saudacao,s,1(${path}))
            same=>n,Wait(1)
            same=>n,GotoIf($[ '${{DEBUG}}' = '1' ]?interno_saudacao)
            same=>n,NoOp('gcami_reply => '${{gcami_reply}})
            same=>n,Set(DDD=${{CUT(gcami_reply,|,1)}})
            same=>n,Set(FONE=${{CUT(gcami_reply,|,2)}})
            same=>n,Set(NOME=${{CUT(gcami_reply,|,3)}})
            same=>n,Set(ID_TABELA=${{CUT(gcami_reply,|,4)}})
            same=>n,Set(COD_LINK_INT=${{CUT(gcami_reply,|,5)}})'''.format(context=context, ip=ip, gender=gender, path=path, custom_path=custom_path, current_date=current_date)


        with open('test.conf', 'w+') as f:
            f.write(layout + '\n')
                
    


class UraApp(App):
    def build(self):
        return CreateUra()

if __name__ == "__main__":
    UraApp().run()
