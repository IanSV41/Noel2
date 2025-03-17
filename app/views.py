# primer lloc web
# @app.route són les peticions que pot atendre el servidor

from flask import Flask, render_template, url_for, request, redirect, flash, session, jsonify
import pymysql

from app import app

from app.bd import obtener_conexion
from flask_mail import Mail, Message

@app.route('/')
@app.route('/Idiomes.html')
def idiomes():

    return render_template('Idiomes.html')


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nouianschilt@gmail.com'  # Tu correo
app.config['MAIL_PASSWORD'] = 'bbtmqatecltvrzzf'


def enviar_correo():
    # Recupera los valores de la sesión
    nom = session.get('nom', '')  # Si no existe, devuelve una cadena vacía
    cognom = session.get('cognom', '')  # Si no existe, devuelve una cadena vacía
    nombrecompleto = f"{nom} {cognom}".strip()  # Concatena y elimina espacios innecesarios

    # Crea el mensaje
    msg = Message(
        "Atenció! Visitant a l'espera",  # Asunto
        sender='nouianschilt@gmail.com',  # Remitente
        recipients=['ianschilt@gmail.com']  # Destinatario(s)
    )

    # Cuerpo del mensaje con el nombre completo
    msg.body = f"La visita amb nom '{nombrecompleto}' ha arribat a les instal·lacions. Vagi a rebre-la al punt de recepció."

    # Envía el correo
    mail.send(msg)


mail = Mail(app)



@app.route('/ver_sesion')
def ver_sesion():
    return jsonify(session)


@app.route('/reset')
def reset():
    session.clear()  # Esto borra todos los datos de la sesión
    return "Sesión borrada"



@app.route('/confirmacio_cat.html')
def confirmacio_cat():
    return render_template('confirmacio_cat.html')

@app.route('/confirmacion_cast.html')
def confirmacion_cast():
    return render_template('confirmacion_cast.html')

@app.route('/confirmacio_eng.html')
def confirmacion_eng():
    return render_template('confirmacio_eng.html')

@app.route('/confirmacio_fr.html')
def confirmacion_fr():
    return render_template('confirmacio_fr.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    # Recuperar todas las respuestas de la sesión
    respuestas = {
        # Respuestas de la página 1
        'nom': session.get('nom', ''),
        'cognom': session.get('cognom', ''),
        'DNI': session.get('DNI', ''),
        'num_tel': session.get('num_tel', ''),
        'email': session.get('email', ''),
        'cotxe': session.get('cotxe', ''),
        'matricula': session.get('matricula', ''),
        'emisari_empresa': session.get('emisari_empresa', ''),
        'empresa': session.get('empresa', ''),

        # Respuestas de la página 2
        'rao': session.get('rao', ''),
        'persona': session.get('persona', ''),
        'saps': session.get('saps', ''),
        'ubi': session.get('ubi', ''),
        'planta': ', '.join(session.get('planta', [])),  # Unir las plantas en una cadena
        'entrada': session.get('entrada', ''),

        # Respuestas de la página 3
        'diarrea_i_o_vomits': session.get('diarrea_i_o_vomits', 'no'),
        'ferides_a_la_pell': session.get('ferides_a_la_pell', 'no'),
        'malalties_a_la_pell': session.get('malalties_a_la_pell', 'no'),
        'malalties_al_nas_gola_orelles_geniva_boca': session.get('malalties_al_nas_gola_orelles_geniva_boca', 'no'),
        'bronquitis': session.get('bronquitis', 'no'),
        'febre_tifoidea': session.get('febre_tifoidea', 'no'),
        'salmonella': session.get('salmonella', 'no'),
        'hepatitis': session.get('hepatitis', 'no'),
        'al·lergies': session.get('al·lergies', 'no'),
        'tipus_al·lergies': session.get('tipus_al·lergies', ''),
        'ulleres_lentilles': session.get('ulleres_lentilles', 'no'),
        'altres_plantes': session.get('altres_plantes', 'no'),
        'resposta_plantes': session.get('resposta_plantes', ''),
        'viatges': session.get('viatges', 'no'),
        'resposta_viatges': session.get('resposta_viatges', ''),
        'COVID': ', '.join(session.get('COVID', [])),  # Unir las opciones de COVID en una cadena
        'accepto': session.get('accepto', 'no')  # Nuevo campo
    }

    # Obtener la conexión con la base de datos
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Consulta SQL para insertar los datos
            query = """
            INSERT INTO respuestas (
                nom, cognom, DNI, num_tel, email, cotxe, matricula, emisari_empresa, empresa,
                rao, persona, saps, ubi, planta, entrada,
                diarrea_i_o_vomits, ferides_a_la_pell, malalties_a_la_pell, malalties_al_nas_gola_orelles_geniva_boca,
                bronquitis, febre_tifoidea, salmonella, hepatitis, al·lergies, tipus_al·lergies,
                ulleres_lentilles, altres_plantes, resposta_plantes, viatges, resposta_viatges, COVID, accepto
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            # Ejecutar la consulta con los valores de las respuestas
            cursor.execute(query, (
                respuestas['nom'],
                respuestas['cognom'],
                respuestas['DNI'],
                respuestas['num_tel'],
                respuestas['email'],
                respuestas['cotxe'],
                respuestas['matricula'],
                respuestas['emisari_empresa'],
                respuestas['empresa'],
                respuestas['rao'],
                respuestas['persona'],
                respuestas['saps'],
                respuestas['ubi'],
                respuestas['planta'],
                respuestas['entrada'],
                respuestas['diarrea_i_o_vomits'],
                respuestas['ferides_a_la_pell'],
                respuestas['malalties_a_la_pell'],
                respuestas['malalties_al_nas_gola_orelles_geniva_boca'],
                respuestas['bronquitis'],
                respuestas['febre_tifoidea'],
                respuestas['salmonella'],
                respuestas['hepatitis'],
                respuestas['al·lergies'],
                respuestas['tipus_al·lergies'],
                respuestas['ulleres_lentilles'],
                respuestas['altres_plantes'],
                respuestas['resposta_plantes'],
                respuestas['viatges'],
                respuestas['resposta_viatges'],
                respuestas['COVID'],
                respuestas['accepto']  # Nuevo campo
            ))

            # Confirmar la transacción
            conexion.commit()
            #session.clear()
            enviar_correo()

        # Redirigir al usuario a 'pag4cat.html' después de guardar los datos
        return jsonify({"status": "success", "message": "Datos guardados correctamente"})


    except Exception as e:
        print(f"Error al guardar en MySQL: {e}")
        conexion.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        conexion.close()









@app.route('/introcast.html')
def introcast():
    return render_template('introcast.html')

@app.route('/introcat.html')
def introcat():
    return render_template('introcat.html')


@app.route('/introeng.html')
def introeng():
    return render_template('introeng.html')

@app.route('/introfr.html')
def introfr():
    return render_template('introfr.html')


@app.route('/pag1cast.html')
def pag1cast():
    return render_template('pag1cast.html')

@app.route('/pag1cat.html')
def pag1cat():
    return render_template('pag1cat.html')

@app.route('/guardar_pag1', methods=['POST'])
def guardar_pag1():
    data = request.get_json()  # Recibe los datos enviados en formato JSON

    # Guarda cada dato en la sesión tal como llega.
    session['nom'] = data.get('nom', '')
    session['cognom'] = data.get('cognom', '')
    session['DNI'] = data.get('DNI', '')
    session['num_tel'] = data.get('num_tel', '')
    session['email'] = data.get('email', '')
    session['cotxe'] = data.get('cotxe', '')
    session['matricula'] = data.get('matricula', '')
    session['emisari_empresa'] = data.get('emisari_empresa', '')
    session['empresa'] = data.get('empresa', '')

    # Devuelve una respuesta JSON para indicar que se guardó correctamente.
    return jsonify({'status': 'success'})




@app.route('/pag1eng.html')
def pag1eng():
    return render_template('pag1eng.html')

@app.route('/pag1fr.html')
def pag1fr():
    return render_template('pag1fr.html')

@app.route('/pag2cast.html')
def pag2cast():
    return render_template('pag2cast.html')


@app.route('/pag2cat.html')
def pag2cat():
    return render_template('pag2cat.html')

@app.route('/guardar_pag2', methods=['POST'])
def guardar_pag2():
    data = request.get_json()  # Recibe los datos en formato JSON

    # Guardar cada campo en la sesión
    session['rao'] = data.get('rao', '')
    session['motiu'] = data.get('motiu', '')
    session['persona'] = data.get('persona', '')
    session['saps'] = data.get('saps', '')
    session['ubi'] = data.get('ubi', '')
    session['planta'] = data.get('planta', [])  # Lista de plantas seleccionadas
    session['entrada'] = data.get('entrada', '')

    return jsonify({'status': 'success'})


@app.route('/pag2eng.html')
def pag2eng():
    return render_template('pag2eng.html')

@app.route('/pag2fr.html')
def pag2fr():
    return render_template('pag2fr.html')

@app.route('/pag3cast.html')
def pag3cast():
    return render_template('pag3cast.html')

@app.route('/pag3salcast.html')
def pag3salcast():
    return render_template('pag3salcast.html')

@app.route('/pag3cat.html')
def pag3cat():
    return render_template('pag3cat.html')

@app.route('/guardar_pag3', methods=['POST'])
def guardar_pag3():
    data = request.json  # Recibe los datos en formato JSON

    # Guardar el campo 'accepto' en la sesión
    session['accepto'] = data.get('accepto', 'no')  # Si no se envía, por defecto es 'no'

    # Actualizar la sesión con los demás datos recibidos
    session.update(data)

    return jsonify({"status": "success"})


@app.route('/pag3salcat.html')
def pag3salcat():
    return render_template('pag3salcat.html')

@app.route('/pag3eng.html')
def pag3eng():
    return render_template('pag3eng.html')

@app.route('/pag3saleng.html')
def pag3saleng():
    return render_template('pag3saleng.html')

@app.route('/pag3fr.html')
def pag3fr():
    return render_template('pag3fr.html')

@app.route('/pag3salfr.html')
def pag3salfr():
    return render_template('pag3salfr.html')

@app.route('/pag4cast.html')
def pag4cast():
    return render_template('pag4cast.html')

@app.route('/pag4cat.html')
def pag4cat():
    return render_template('pag4cat.html')

@app.route('/pag4eng.html')
def pag4eng():
    return render_template('pag4eng.html')

@app.route('/pag4fr.html')
def pag4fr():
    return render_template('pag4fr.html')

@app.route('/salutcast.html')
def salutcast():
    return render_template('salutcast.html')

@app.route('/salutcat.html')
def salutcat():
    return render_template('salutcat.html')

@app.route('/guardar_pagsalut', methods=['POST'])
def guardar_pagsalut():
    data = request.get_json()  # Recibe los datos en formato JSON

    # Guardar cada campo en la sesión
    session['diarrea_i_o_vomits'] = data.get('diarrea_i_o_vomits', 'no')
    session['ferides_a_la_pell'] = data.get('ferides_a_la_pell', 'no')
    session['malalties_a_la_pell'] = data.get('malalties_a_la_pell', 'no')
    session['malalties_al_nas_gola_orelles_geniva_boca'] = data.get('malalties_al_nas_gola_orelles_geniva_boca', 'no')
    session['bronquitis'] = data.get('bronquitis', 'no')
    session['febre_tifoidea'] = data.get('febre_tifoidea', 'no')
    session['salmonella'] = data.get('salmonella', 'no')
    session['hepatitis'] = data.get('hepatitis', 'no')
    session['al·lergies'] = data.get('al·lergies', 'no')
    session['tipus_al·lergies'] = data.get('tipus_al·lergies', '')
    session['ulleres_lentilles'] = data.get('ulleres_lentilles', 'no')
    session['altres_plantes'] = data.get('altres_plantes', 'no')
    session['resposta_plantes'] = data.get('resposta_plantes', '')
    session['viatges'] = data.get('viatges', 'no')
    session['resposta_viatges'] = data.get('resposta_viatges', '')
    session['COVID'] = data.get('COVID', [])

    return jsonify({'status': 'success'})


@app.route('/saluteng.html')
def saluteng():
    return render_template('saluteng.html')
@app.route('/salutfr.html')
def salutfr():
    return render_template('salutfr.html')