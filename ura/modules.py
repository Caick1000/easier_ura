from datetime import datetime

current_date = datetime.now().strftime("%Y/%m/%d")


def transferencias(type_transferencia):
    if type_transferencia == 'Aspect':
        transf = '''same=>n(transferir),NoOp(transferir - Aspect)
    same=>n,Playback(${SOUND_DIR}/diversos/${V_GENDER}/aguarde_transferencia)

    same=>n,Set(NOME_UNDERLINE=${STRREPLACE(NOME," ","_")})
    same=>n,Set(NOME_CURTO=${NOME_UNDERLINE:0:29})
    same=>n,NoOp(NOME_CURTO --> ${NOME_CURTO})

    same=>n,Set(CPF=$[${CPF} +0])
    same=>n,NoOp(CPF --> ${CPF})

    same=>n,AGI(/var/lib/asterisk/agi-bin/talkeen/string2hex.php,${NUM_CONTR})
    same=>n,SIPAddHeader(User-to-User: ${V_RETORNO})

    same=>n,NoOp(V_RETORNO -----------> ${V_RETORNO})
    same=>n,NoOp(${SIP_HEADER(User-to-User)} -----------> ${SIP_HEADER(User-To-User)})
    same=>n,NoOp(${STRREPLACE(NOME," ","_")})
    
    same=>n,Set(CALLERID(name)=${NOME_CURTO}|${CPF}|${DDD}${FONE})
    same=>n,Set(CALLERID(num)=${DDD}${FONE})

    same=>n,Set(FILE(${gEstados},,,la,u)={"origem":"dialplan","comando":"entregaRemoto","linha_id":"${LINHA_ID}","destino":"${fila_transfer}"})
    same=>n,Dial(SIP/g50/${FILA_TRANSFER})

    same=>n,Goto(fim)'''

    elif type_transferencia == 'Olos':
        transf = '''same=>n(transferir),NoOp(transferir - Olos)
    same=>n,Set(COD_LIG=TRAN)
    same=>n,Playback(${SOUND_DIR}/diversos/${V_GENDER}/aguarde_transferencia)

    same=>n,Set(NOME_UNDERLINE=${STRREPLACE(NOME," ","_")})
    same=>n,NoOp(NOME_UNDERLINE --> ${NOME_UNDERLINE})

    same=>n,Set(CALLERID(name)=${NOME_UNDERLINE}|4135606784|${DDD}${FONE})
    same=>n,Set(CALLERID(num)=${DDD}${FONE})

    same=>n,Set(FILE(${gEstados},,,la,u)={"origem":"dialplan","comando":"entregaRemoto","linha_id":"${LINHA_ID}","destino":"${fila_transfer}"})
    same=>n,Dial(SIP/g39/${FILA_TRANSFER})

    same=>n,Goto(fim)'''

    elif type_transferencia == 'Talkeen':
        transf = '''same=>n(transferir),NoOp(transferir - Talkeen)
    same=>n,Set(COD_LIG=TRAN)
    ame=>n,Playback(${SOUND_DIR}/diversos/${V_GENDER}/aguarde_transferencia)

    same=>n,Set(TAM_LINHA=${LEN(${LINHA_ID})})
    same=>n,ExecIf($[${TAM_LINHA} = 1]?Set(LINHA_ID_OK=000${LINHA_ID}))
    same=>n,ExecIf($[${TAM_LINHA} = 2]?Set(LINHA_ID_OK=00${LINHA_ID}))
    same=>n,ExecIf($[${TAM_LINHA} = 3]?Set(LINHA_ID_OK=0${LINHA_ID}))
    same=>n,ExecIf($[${TAM_LINHA} = 4]?Set(LINHA_ID_OK=${LINHA_ID}))

    same=>n,Set(CALLERID(num)=${LINHA_ID_OK}${CALLERID(num)})
    same=>n,Set(CALLERID(name)=${NOME})
    ;same=>n,Queue(${FILA_TRANSFER},tc)
    same=>n,Queue(${FILA_TRANSFER},tc,,/var/lib/asterisk/sounds/talkeen/AgenteVirtual)
    same=>n,Hangup()
    same=>n,Goto(fim) '''

    else:
        transf = '''same=>n(transferir),NoOp(sem transferencia)
    same=>n,Goto(encerrar)'''

    return(transf)


def localizacao(context, ip, path, custom_path, gender, debug, transf):
    type_transferencia = transferencias(transf)

    layout = ''';-----------------------------------------------------------------------------------------------------------------------------
;-----------------------------------------------------------------------------------------------------------------------------
;
;TALKEEN - {context}
;DATA: {current_date}
; CREATED BY - CAICK
;
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

;===========================================================================================
;variaveis para o dialplan
;===========================================================================================
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

;===========================================================================================
;localizar responsavel
;===========================================================================================
    same=>n,Gosub(modulo_localizacao,s,1(${{SOUND_DIR}},${{V_GENDER}},${{SOUND_DIR_CUSTOM}},${{GRAMMAR_GLOBAL_DIR}},${{PRI_NOME}},0))
    same=>n,NoOp("RV_ANSWER =>"${{RV_ANSWER}})
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "sim" ]?transferir)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "nao" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "ocupado" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "falecido" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "naoexiste"]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "quem" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "repetir" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "naoexiste" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "naoesta" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "" ]?encerrar)
    same=>n,GotoIf($[ "${{RV_ANSWER}}" = "manha" || "${{RV_ANSWER}}" = "tarde" || "${{RV_ANSWER}}" = "noite" ]?encerrar)
    same=>n,Goto(fim)
;===========================================================================================
;transferir
;===========================================================================================
    {type_transferencia}
;===========================================================================================

;===========================================================================================
;encerrar
;===========================================================================================
    same=>n(encerrar),NoOp(encerrar)
    same=>n,Wait(1)
    same=>n,Playback(${{SOUND_DIR}}/localizacao/${{V_GENDER}}/agradece_ligacao)
    same=>n,Gosub(modulo_encerrar,s,1(${{SOUND_DIR}}/encerrar/${{V_GENDER}}))

    same=>n,Goto(desliga)
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