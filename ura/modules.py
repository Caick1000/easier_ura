from datetime import datetime

current_date = datetime.now().strftime("%Y/%m/%d")

def header(context, ip, path, custom_path, gender):

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
    same=>n,Set(SOUND_DIR_CUSTOM={custom_path})
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
    same=>n,Set(NOME=Augusto)
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

    return(layout)



def body (path, custom_path):
    layout = '''same=>n(interno_saudacao),NoOp(interno_saudacao)
    same=>n,Set(PRI_NOME=${{CUT(NOME," ",1)}})
    same=>n,Set(PRI_NOME=${{TOLOWER(${{PRI_NOME}})}})

    same=>n,Goto(localizar_responsavel)
;===========================================================================================

;===========================================================================================
;localizar_responsavel
;===========================================================================================
    same=>n(localizar_responsavel),Playback(${path}/falar_com)

    same=>n,Gosub(modulo_play_nome,s,1(${{SOUND_DIR_NOME}},${{PRI_NOME}},f))
    same=>n(localiza_responsavel_continua),Set(RESP_INVALIDA=0)
    same=>n,Set(RV_BEFORE_SPEECH_TIMEOUT=2300)
    same=>n,Set(RV_AFTER_SPEECH_TIMEOUT=700)
    same=>n,Set(RV_INCOMPLETE_TIMEOUT=4100)
    same=>n,Set(RV_MAX_SPEECH_TIMEOUT=5000)
    same=>n,Set(RV_CONFIDENCE=0.48)
    same=>n,Set(RV_BARGEIN=1)
    same=>n,Set(RV_OPTIONS=epe=0&sw=false&b=${{RV_BARGEIN}}&nac=true&t=${{RV_MAX_SPEECH_TIMEOUT}}&nit=${{RV_BEFORE_SPEECH_TIMEOUT}}&sct=${{RV_AFTER_SPEECH_TIMEOUT}}&sint=${{RV_INCOMPLETE_TIMEOUT}}&ct=${{RV_CONFIDENCE}})
    same=>n,Gosub(modulo_rec_voz,s,1(${path},e_voce,e voce?,f,wav,${{GRAMMAR_GLOBAL_DIR}}/LOCALIZAR_CLIENTE.gram,${{RV_OPTIONS}}))
    same=>n,GotoIf( $[ "${{RV_ANSWER}}" = "" ]?encerrar)
        
    same=>n,ExecIf( $["${{RV_ANSWER}}" = "sim"]?Set(COD_LIG=SIM))
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "sim" ]?transferir)
    
    same=>n,ExecIf( $["${{RV_ANSWER}}" = "nao"]?Set(COD_LIG=NAO))
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "nao" ]?encerrar)

    same=>n,ExecIf( $["${{RV_ANSWER}}" = "ocupado"]?Set(COD_LIG=OCPD))
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "ocupado" ]?encerrar)

    same=>n,ExecIf($[ "${{RV_ANSWER}}" = "naoexiste" ]?Set(COD_LIG=NEXT))
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "naoexiste" ]?encerrar)

    same=>n,ExecIf( $["${{RV_ANSWER}}" = "naoesta"]?Set(COD_LIG=OCPD))
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "naoesta" ]?encerrar)

    same=>n,ExecIf($[ "${{RV_ANSWER}}" = "quem" ]?Playback(${path}/repetir/repetindo))
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "quem" ]?localizar_responsavel)

    same=>n,ExecIf($[ "${{RV_ANSWER}}" = "repetir" ]?Playback(${path}/repetir/repetindo))
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "repetir" ]?localizar_responsavel)

    same=>n,ExecIf($[ "${{RV_ANSWER}}" = "vouchamar" ]?Playback(${path}/certo))
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "vouchamar" ]?transferir)

    same=>n,ExecIf($[ "${{RV_ANSWER}}" = "aguardar" ]?Playback(${path}/certo))
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "aguardar" ]?transferir)

    same=>n,Goto(encerrar)
;===========================================================================================

;===========================================================================================
;encerrar
;===========================================================================================
    same=>n(encerrar),NoOp(encerrar)
    same=>n,Playback(${path}/certo)
    same=>n,Playback(${custom_path}/c_agradece_ligacao)
    same=>n(encerrar_2),Gosub(modulo_encerrar,s,1(${path}/encerrar))
    same=>n,Goto(desligar)
;==========================================================================================='''.format(path=path, custom_path=custom_path)

    return(layout)


def footer ():

    layout = '''
;===========================================================================================
; desligar
;===========================================================================================
    same=>n(desligar),Set(CANAL_TEMP=1)
    same=>n,GotoIf($[ "${{GRAVACAO}}" = "NAO" ]?desligar_fim)
    same=>n(stopmx),StopMixMonitor()
    same=>n(desligar_fim),Hangup()
;===========================================================================================
; Hangup
;===========================================================================================
exten => h,1,NoOp(Event Hangup)
    same=>n,DumpChan()
    same=>n,GotoIf($[ "${{SECE}}" = "1" ]?fim)
    same=>n,ExecIf($[ "${{COD_LIG}}" = ""]?Set(COD_LIG=DISO))
  
    same=>n(naoatendido),Set(FILE(${{gEstados}},,,la,u)={"origem":"dialplan","comando":"registraFinalizacao","tipo":"${{COD_LIG}}","linha_id":"${{LINHA_ID}}","dialstatus":"${{COD_LIG}}"}})

    same=>n(fim),NoOp(Fim)   
;===========================================================================================
; fim talkeen-IVR
;==========================================================================================='''

    return(layout)