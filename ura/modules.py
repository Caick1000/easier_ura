from datetime import datetime

current_date = datetime.now().strftime("%Y/%m/%d")


def transferencias(type_transferencia):
    if type_transferencia == 'Aspect':
        transf = 'TESTE ASPECT'

    elif type_transferencia == 'Olos':
        transf = 'TESTE OLOS'

    elif type_transferencia == 'Talkeen':
        transf = 'TESTE TALKEEN'

    else:
        transf = 'TESTE NENHUM'

    return(transf)


def localizacao(context, ip, path, custom_path, gender, debug, transf):


    type_transferencia = transferencias(transf)

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
    same=>n,Set(COD_LIG=DISO)
    same=>n,NoOp(Destino atendeu a ligacao, Iniciando Ura)
    same=>n,Set(SEM_RESPOSTA=1)
    same=>n,Set(FINALIZAOK=0)
    same=>n,Set(DEBUG={debug})
    same=>n,Set(V_GENDER={gender})
    same=>n,Set(IP_FILE_GRAMMAR={ip})
    same=>n,NoOp(IP_FILE_GRAMMAR => ${{IP_FILE_GRAMMAR}})
    same=>n,Set(SOUND_DIR={path})
    same=>n,Set(SOUND_DIR_CUSTOM={custom_path})
    same=>n,Set(SOUND_DIR_NOME=nomes)
    same=>n,Set(GRAMMAR_GLOBAL_DIR=http://${{IP_FILE_GRAMMAR}}/grammar/global)
    same=>n,Set(V_IVR=${{CONTEXT}})

    same=>n,Gosub(modulo_init,s,1(${{IP_FILE_GRAMMAR}}))
    same=>n,GotoIf($[ "${{DEBUG}}" = "1" ]?interno_modulo_amd_rec_voz)
    same=>n,Set(FILE(${{gCAMI}},,,la,u)={{"origem":"dialplan","comando":"ligAtendida","linha_id":"${{LINHA_ID}}","canal":"${{CHANNEL(name)}}","retorno":"false"}})  
    same=>n,Set(FILE(${{gCAMI}},,,la,u)={{"origem":"dialplan","comando":"criaVariaveis","linha_id":"${{LINHA_ID}}","canal":"${{CHANNEL(name)}}","retorno":"false","linha_info":"ddd|fone|nome_cliente|id_tabela_disca|cod_link_int|cod_link_char|contrato|valor|cpf|idusuario","fila_info":"fila_transfer"}})

    same=>n(interno_modulo_amd_rec_voz),Gosub(modulo_amd_rec_voz,s,1(${{IP_FILE_GRAMMAR}}))

    same=>n(humano),NoOp(Executando ${{V_IVR}})

    same=>n,NoOp("COD_LIG => "${{COD_LIG}})
    same=>n,NoOp("SECE => "${{SECE}})

;==========BLOCO SETA VARIAVEIS PARA USAR NO DIALPLAN============
   same=>n,GotoIf($[ "${{DEBUG}}" = "1" ]?interno_gcami_reply)
    same=>n,Set(DDD=${{CUT(gcami_reply,|,1)}})
    same=>n,Set(FONE=${{CUT(gcami_reply,|,2)}})
    same=>n,Set(NOME=${{CUT(gcami_reply,|,3)}})
    same=>n,Set(ID_TABELA=${{CUT(gcami_reply,|,4)}})
    same=>n,Set(COD_LINK_INT=${{CUT(gcami_reply,|,5)}})
    same=>n,Set(COD_LINK_CHAR=${{CUT(gcami_reply,|,6)}})
    same=>n,Set(CONTRATO=${{CUT(gcami_reply,|,7)}})
    same=>n,Set(IDUSUARIO=${{CUT(gcami_reply,|,10)}})
    same=>n,Set(FILA_TRANSFER=${{CUT(gcami_reply,|,11)}})

    ;"Trata nome"
    same=>n(interno_gcami_reply),Set(PRI_NOME=${{CUT(NOME," ",1)}})
    same=>n,Set(PRI_NOME=${{TOLOWER(${{PRI_NOME}})}})

;==========================================LOCALIZAR RESPONSAVEL========================================
    same=>n,Gosub(modulo_localizacao,s,1(${{SOUND_DIR}},${{V_GENDER}},${{SOUND_DIR_CUSTOM}},${{GRAMMAR_GLOBAL_DIR}},${{PRI_NOME}},0))
    same=>n,NoOp("RV_ANSWER =>"${{RV_ANSWER}})
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "sim" ]?transferir)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "nao" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "ocupado" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "falecido" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "naoexiste"]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "quem" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "repetir" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "naoexiste" ]?desconhece)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "naoesta" ]?encerrar)
    same=>n,Goto(fim)
;===========================================================================================
;transferir
;===========================================================================================
    same=>n(transferir),NoOp(transferir)
    {type_transferencia}
;===========================================================================================

;===========================================================================================
;FINAL DA URA, FINALIZADOR FIXO
;===========================================================================================
    same=>n(desliga),Set(CANAL_TEMP=1)
    same=>n,GotoIf($[ "${{GRAVACAO}}" = "NAO" ]?fim)
    same=>n(stopmx),StopMixMonitor()
    same=>n(fim),Hangup()

;----------------------------------------------------------------
; Hangup
;----------------------------------------------------------------
exten => h,1,NoOp(Event Hangup)
    
    same=>n,GotoIf($[ "${{SECE}}" = "1" ]?fim)
    same=>n,ExecIf($[ "${{COD_LIG}}" = ""]?Set(COD_LIG=DISO))
    
    same=>n(naoatendido),Set(FILE(${{gEstados}},,,la,u)={{"origem":"dialplan","comando":"registraFinalizacao","tipo":"${{COD_LIG}}","linha_id":"${{LINHA_ID}}","dialstatus":"${{COD_LIG}}"}})

    same=>n(fim),NoOp(Fim)   

;----------------------------------------------------------------
; fim talkeen-localizacao
;----------------------------------------------------------------

'''.format(context=context, ip=ip, gender=gender, path=path, custom_path=custom_path, debug=debug, type_transferencia=type_transferencia, current_date=current_date)

    return(layout)