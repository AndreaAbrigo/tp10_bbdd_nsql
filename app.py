# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request, render_template
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import json
from db import bbdd

app = Flask(__name__)

#### CARGA DE LOS USUARIOS, LAS ARMAS Y LAS MONEDAS 
@app.route('/cargarDatos')
def cargarDatos():
    altaUsuarios()
    cargarArmas()
    cargarMonedas()
    resultado = bbdd.buscarUsuarios()
    for e in resultado:
        if (e['usuario']=="Darth vader"):
            usuario=e['usuario']
            privada=e['privada']
            publica=e['publica']
    return render_template("inicioD.html", usuario=usuario, privada=privada, publica=publica)


def connect_db():
    conn = BigchainDB('https://test.ipdb.io')
    return conn

@app.route('/')
def todo():
    return render_template("todo.html")


## USUARIOS
@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
    resultado = bbdd.buscarUsuarios()
    for e in resultado:
        if (e['usuario']==nombre):
            nombre_usuario=e['usuario']
            clave_privada=e['privada']
            clave_publica=e['publica']
    if (nombre=="Darth vader"):
        return render_template("inicioD.html", usuario=nombre_usuario, privada=clave_privada, publica=clave_publica)
    else:
        return render_template("inicio.html", usuario=nombre_usuario, privada=clave_privada, publica=clave_publica)

@app.route('/altaUsuarios')
def altaUsuarios():
    darth_vader = generate_keypair()
    bbdd.insertarUsuario("Darth vader", darth_vader[0], darth_vader[1])
    boba_fett = generate_keypair()
    bbdd.insertarUsuario("Boba fett", boba_fett[0], boba_fett[1])
    greedo = generate_keypair()
    bbdd.insertarUsuario("Greedo", greedo[0], greedo[1])
    din_djarin = generate_keypair()
    bbdd.insertarUsuario("Din D jarin", din_djarin[0], din_djarin[1])
    return render_template("todo.html")


### ARMAS

@app.route('/cargarArmas')
def cargarArmas():
    conexion = connect_db()
    resultado = bbdd.buscarUsuarios()
    for e in resultado:
        if (e['usuario']=="Darth vader"):
            usuario=e['usuario']
            privada=e['privada']
            publica=e['publica']

    arma = {
        'data':{
            'nombre': "Rifle bláster EL-16",
            'cantidad': 10,
            'costo': 3
        }   
    }
    tx = conexion.transactions.prepare(
        operation='CREATE',
        signers=publica,
        recipients=[([publica],10)],
        asset=arma
    )
    firma_tx = conexion.transactions.fulfill(tx, private_keys=privada)
    sent_tx = conexion.transactions.send_commit(firma_tx)
    activo=conexion.assets.get(search="Rifle bláster EL-16")
    id=sent_tx['id']
    bbdd.insertarArma(id, usuario, privada, publica, "Rifle bláster EL-16", 10, 3)

    arma = {
        'data':{
            'nombre': "Bláster pesado T-21",
            'cantidad': 5,
            'costo': 2
        }   
    }
    tx = conexion.transactions.prepare(
        operation='CREATE',
        signers=publica,
        recipients=[([publica], 5)],
        asset=arma
    )
    firma_tx = conexion.transactions.fulfill(tx, private_keys=privada)
    sent_tx = conexion.transactions.send_commit(firma_tx)
    activo=conexion.assets.get(search="Bláster pesado T-21")
    id=sent_tx['id']
    bbdd.insertarArma(id, usuario, privada, publica, "Bláster pesado T-21", 5, 2)

    arma = {
        'data':{
            'nombre': "Rifles pesados RT-97C",
            'cantidad': 15,
            'costo': 4
        }   
    }
    tx = conexion.transactions.prepare(
        operation='CREATE',
        signers=publica,
        recipients=[([publica], 15)],
        asset=arma
    )
    firma_tx = conexion.transactions.fulfill(tx, private_keys=privada)
    sent_tx = conexion.transactions.send_commit(firma_tx)
    activo=conexion.assets.get(search="Rifles pesados RT-97C")
    id=sent_tx['id']
    bbdd.insertarArma(id, usuario, privada, publica, "Rifles pesados RT-97C", 15, 4)

    return render_template("inicioD.html", usuario=usuario, privada=privada, publica=publica)

@app.route('/nuevoArma', methods=["POST"])
def nuevoArma():
    if request.method == 'POST':
        usuario = request.form['usuario'] 
        privada = request.form['privada']  
        publica = request.form['publica']    
    return render_template("nuevoArma.html", usuario=usuario, privada=privada, publica=publica)   

@app.route('/altaArma', methods=["POST"])
def altaArma():
    conexion = connect_db()
    if request.method == 'POST':
        usuario = request.form['usuario'] 
        privada = request.form['privada']  
        publica = request.form['publica'] 
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        costo = request.form['costo']  
    cantidad=int(cantidad) 
    arma = {
        'data':{
            'nombre':nombre,
            'cantidad':cantidad,
            'costo':costo
        }   
    }
    tx = conexion.transactions.prepare(
        operation='CREATE',
        signers=publica,
        recipients=[([publica], cantidad)],
        asset=arma
    )
    firma_tx = conexion.transactions.fulfill(tx, private_keys=privada)
    sent_tx = conexion.transactions.send_commit(firma_tx)
    activo=conexion.assets.get(search=nombre)
    id=sent_tx['id']
    resultado = bbdd.insertarArma(id, usuario, privada, publica, nombre, cantidad, costo)
    return render_template("confirmacionAlta.html", nombre=nombre, usuario=usuario)  

@app.route('/misArmas', methods=["POST"])
def misArmas():
    conexion = connect_db()
    if request.method == 'POST':
        usuario = request.form['usuario'] 
    result = bbdd.buscarUsuarios()
    for e in result:
        if (e['usuario']==usuario):
            privada=e['privada']
            publica=e['publica']
    resultado = bbdd.buscarArmas()
    ides = []
    nombres = []
    cantidades = []
    index=0
    costos=[]
    datos = []
    tam=0
    for e in resultado:
        datos=conexion.transactions.get(asset_id=e['id'])
        nom = (datos[0]['asset']['data']['nombre'])
        costo = (datos[0]['asset']['data']['costo'])
        cant=len(datos)-1
        outs=datos[cant]['outputs']
        canti=len(outs)-1
        for i in outs:
            if (i['condition']['details']['public_key']==publica):
                nombres.append(nom)
                ides.append(e['id'])
                cantidades.append(i['amount'])
                costos.append(costo)
        tam=len(nombres)
    return render_template("misArmas.html", usuario=usuario, nombres=nombres, ides=ides, cantidades=cantidades, tamanio=tam, costos=costos) 

### MONEDAS

@app.route('/cargarMonedas')
def cargarMonedas():
    conexion = connect_db()
    resultado = bbdd.buscarUsuarios()
    for e in resultado:
        if (e['usuario']=="Darth vader"):
            usuario_darth=e['usuario']
            privada_darth=e['privada']
            publica_darth=e['publica']
        if (e['usuario']=="Boba fett"):
            usuario_boba=e['usuario']
            privada_boba=e['privada']
            publica_boba=e['publica']
        if (e['usuario']=="Greedo"):
            usuario_greedo=e['usuario']
            privada_greedo=e['privada']
            publica_greedo=e['publica']
        if (e['usuario']=="Din D jarin"):
            usuario_din=e['usuario']
            privada_din=e['privada']
            publica_din=e['publica']
    moneda = {
        'data':{
            'nombre': "Galactic Coin",
            'cantidad': 20
        }   
    }

    tx = conexion.transactions.prepare(
        operation='CREATE',
        signers=publica_darth,
        recipients=[([publica_darth],6)],
        asset=moneda
    )
    firma_tx = conexion.transactions.fulfill(tx, private_keys=privada_darth)
    sent_tx = conexion.transactions.send_commit(firma_tx)
    id=sent_tx['id']
    bbdd.insertarMoneda(id, usuario_darth, privada_darth, publica_darth, "Galactic Coin", 6)

    ## 5 a Boba Fett
    tx = conexion.transactions.prepare(
        operation='CREATE',
        signers=publica_darth,
        recipients=[([publica_boba],5)],
        asset=moneda
    )
    firma_tx = conexion.transactions.fulfill(tx, private_keys=privada_darth)
    sent_tx = conexion.transactions.send_commit(firma_tx)
    id=sent_tx['id']
    bbdd.insertarMoneda(id, usuario_darth, privada_darth, publica_darth, "Galactic Coin", 5)

    ## 3 a Greedo
    tx = conexion.transactions.prepare(
        operation='CREATE',
        signers=publica_darth,
        recipients=[([publica_greedo],3)],
        asset=moneda
    )
    firma_tx = conexion.transactions.fulfill(tx, private_keys=privada_darth)
    sent_tx = conexion.transactions.send_commit(firma_tx)
    id=sent_tx['id']
    bbdd.insertarMoneda(id, usuario_darth, privada_darth, publica_darth, "Galactic Coin", 3)

    ## 8 a Din Djarin
    tx = conexion.transactions.prepare(
        operation='CREATE',
        signers=publica_darth,
        recipients=[([publica_din],8)],
        asset=moneda
    )
    firma_tx = conexion.transactions.fulfill(tx, private_keys=privada_darth)
    sent_tx = conexion.transactions.send_commit(firma_tx)
    id=sent_tx['id']
    bbdd.insertarMoneda(id, usuario_darth, privada_darth, publica_darth, "Galactic Coin", 8)
    return render_template("inicioD.html", usuario=usuario_darth, privada=privada_darth, publica=publica_darth)

@app.route('/nuevaMoneda', methods=["POST"])
def nuevaMoneda():
    if request.method == 'POST':
        usuario = request.form['usuario'] 
        privada = request.form['privada']  
        publica = request.form['publica']    
    return render_template("nuevaMoneda.html", usuario=usuario, privada=privada, publica=publica)   

@app.route('/altaMoneda', methods=["POST"])
def altaMoneda():
    conexion = connect_db()
    if request.method == 'POST':
        usuario = request.form['usuario'] 
        privada = request.form['privada']  
        publica = request.form['publica'] 
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
    cantidad=int(cantidad) 
    moneda = {
        'data':{
            'nombre':nombre,
            'cantidad':cantidad
        }   
    }
    tx = conexion.transactions.prepare(
        operation='CREATE',
        signers=publica,
        recipients=[([publica], cantidad)],
        asset=moneda
    )
    firma_tx = conexion.transactions.fulfill(tx, private_keys=privada)
    sent_tx = conexion.transactions.send_commit(firma_tx)
    activo=conexion.assets.get(search=nombre)
    id=sent_tx['id']
    resultado = bbdd.insertarMoneda(id, usuario, privada, publica, nombre, cantidad)
    return render_template("confirmacionAlta.html", nombre=nombre, usuario=usuario)   

@app.route('/misMonedas', methods=["POST"])
def misMonedas():
    conexion = connect_db()
    if request.method == 'POST':
        usuario = request.form['usuario'] 
    result = bbdd.buscarUsuarios()
    for e in result:
        if (e['usuario']==usuario):
            privada=e['privada']
            publica=e['publica']
    resultado = bbdd.buscarMonedas()
    cantidad_monedas = 0
    for e in resultado:
        datos=conexion.transactions.get(asset_id=e['id'])
        cant=len(datos)-1
        outs=datos[cant]['outputs']
        canti=len(outs)-1
        for i in outs:
            if (i['condition']['details']['public_key']==publica):
                cantidad_monedas=(cantidad_monedas+int(i['amount']))
    return render_template("misMonedas.html", usuario=usuario, monedas=cantidad_monedas) 


@app.route('/vender', methods=["POST"])
def vender():
    if request.method == 'POST':
        id = request.form['id'] 
        nombre = request.form['nombre'] 
        cantidad = request.form['cantidad'] 
    return render_template("vender.html", id=id, nombre=nombre, cantidad=cantidad) 

@app.route('/confirmarVenta', methods=["POST"])
def confirmarVenta():
    if request.method == 'POST':
        id = request.form['id'] 
        comprador = request.form['comprador']
        cantidad = int(request.form['cantidad'])
    conexion = connect_db()
    resultado = bbdd.buscarUsuarios()
    for e in resultado:
        if (e['usuario']=="Darth vader"):
            usuario_vendedor=e['usuario']
            privada_vendedor=e['privada']
            publica_vendedor=e['publica']
        if (e['usuario']==comprador):
            usuario_comprador=e['usuario']
            privada_comprador=e['privada']
            publica_comprador=e['publica']
    
    #Datos armas
    datos_armas=conexion.transactions.get(asset_id=id)
    cant=(len(datos_armas)-1)
    cant=int(cant)
    amount_armas=datos_armas[cant]['outputs'][cant]['amount']
    amount_armas=int(amount_armas)
    nombreArma= datos_armas[0]['asset']['data']['nombre']
    costo = int(datos_armas[0]['asset']['data']['costo'])

    #Datos moneda
    mone = bbdd.buscarMonedas()
    datos = []  
    for e in mone:
        datos.append(conexion.transactions.get(asset_id=e['id']))
        for d in datos:
            cant=(len(d)-1)
            cant=int(cant)
            outs=d[cant]['outputs']
            clave = outs[0]['condition']['details']['public_key']
            if (clave == publica_comprador):
                cantidad_monedas= int(outs[0]['amount'])
                id_moneda = d[0]['id']
    totalCompra = int(cantidad * costo)
    datos_moneda=conexion.transactions.get(asset_id=id_moneda)

    if(cantidad<=amount_armas):
        if (totalCompra<=cantidad_monedas):
            #Venta
            resto_armas=(amount_armas-cantidad)
            output_index = 0
            output = datos_armas[0]['outputs'][output_index]
            transfer_input = {
                'fulfillment': output['condition']['details'],
                'fulfills': {
                'output_index': output_index,
                'transaction_id': datos_armas[0]['id'],
                },
            'owners_before': output['public_keys'],
            }
            transfer_asset = {'id': datos_armas[0]['id'],}
            prepared_transfer_tx = conexion.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                recipients=[([publica_comprador], cantidad), ([publica_vendedor], resto_armas)]
            )
            fulfilled_transfer_tx = conexion.transactions.fulfill(
                prepared_transfer_tx, private_keys=privada_vendedor)
            sent_transfer_tx = conexion.transactions.send_commit(fulfilled_transfer_tx)

            #Cobro
            resto_monedas=(cantidad_monedas-totalCompra)
            o_index = 0
            output = datos_moneda[0]['outputs'][o_index]
            transfer_input = {
                'fulfillment': output['condition']['details'],
                'fulfills': {
                'output_index': o_index,
                'transaction_id': datos_moneda[0]['id'],
                },
            'owners_before': output['public_keys'],
            }
            transfer_asset = {'id': datos_moneda[0]['id'],}
            prepared_transfer_tx = conexion.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                recipients=[([publica_vendedor], totalCompra), ([publica_comprador], resto_monedas)]
            )
            fulfilled_transfer_tx = conexion.transactions.fulfill(
                prepared_transfer_tx, private_keys=privada_comprador)
            sent_transfer_tx = conexion.transactions.send_commit(fulfilled_transfer_tx)

            return render_template("vendido.html", usuario=usuario_vendedor, comprador=comprador, cantidad=cantidad, nombre=nombreArma)
        else:
            return render_template("monedas_insuficientes.html", usuario=usuario_vendedor)
    else:
        return render_template("armas_insuficientes.html", usuario=usuario_vendedor)


@app.route('/comprar', methods=["POST"])
def comprar():
    if request.method == 'POST':
        usuario = request.form['usuario']
    conexion = connect_db() 
    result = bbdd.buscarUsuarios()
    for e in result:
        if (e['usuario']=="Darth vader"):
            privada=e['privada']
            publica=e['publica']
    resultado = bbdd.buscarArmas()
    ides = []
    nombres = []
    cantidades = []
    index=0
    costos=[]
    datos = []
    tam=0
    for e in resultado:
        datos=conexion.transactions.get(asset_id=e['id'])
        nom = (datos[0]['asset']['data']['nombre'])
        costo = (datos[0]['asset']['data']['costo'])
        cant=len(datos)-1
        outs=datos[cant]['outputs']
        canti=len(outs)-1
        for i in outs:
            if (i['condition']['details']['public_key']==publica):
                nombres.append(nom)
                ides.append(e['id'])
                cantidades.append(i['amount'])
                costos.append(costo)
        tam=len(nombres)
    return render_template("armasDisponibles.html", usuario=usuario, nombres=nombres, ides=ides, cantidades=cantidades, tamanio=tam, costos=costos) 

@app.route('/seleccionarCompra', methods=["POST"])
def seleccionarCompra():
    if request.method == 'POST':
        id = request.form['id'] 
        nombre = request.form['nombre'] 
        cantidad= request.form['cantidad'] 
        costo = request.form['costo'] 
        usuario = request.form['usuario'] 
    return render_template("seleccionarCompra.html", comprador=usuario, id=id, nombre=nombre, cantidadDisponible=cantidad, costo=costo) 

@app.route('/confirmarCompra', methods=["POST"])
def confirmarCompra():
    if request.method == 'POST':
        id = request.form['id'] 
        comprador = request.form['comprador']
        cantidadDisponible = int(request.form['cantidadDisponible'])
        cantidadRequerida = int(request.form['cantidadRequerida'])
        costo = int(request.form['costo'])
        nombreArma = request.form['nombre']
    conexion = connect_db()
    resultado = bbdd.buscarUsuarios()
    for e in resultado:
        if (e['usuario']=="Darth vader"):
            usuario_vendedor=e['usuario']
            privada_vendedor=e['privada']
            publica_vendedor=e['publica']
        if (e['usuario']==comprador):
            usuario_comprador=e['usuario']
            privada_comprador=e['privada']
            publica_comprador=e['publica']

    ##Datos moneda
    mone = bbdd.buscarMonedas()
    datos = []  
    for e in mone:
        datos.append(conexion.transactions.get(asset_id=e['id']))
        for d in datos:
            cant=(len(d)-1)
            cant=int(cant)
            outs=d[cant]['outputs']
            clave = outs[0]['condition']['details']['public_key']
            if (clave == publica_comprador):
                cantidad_monedas= int(outs[0]['amount'])
                id_moneda = d[0]['id']
    
    datos_moneda=conexion.transactions.get(asset_id=id_moneda)

    totalCompra = int(cantidadRequerida * costo)
    if(cantidadRequerida<=cantidadDisponible):
        if (totalCompra<=cantidad_monedas):
            #Venta
            resto_armas=(cantidadDisponible-cantidadRequerida)
            output_index = 0
            datos_armas=conexion.transactions.get(asset_id=id)
            output = datos_armas[0]['outputs'][output_index]
            transfer_input = {
                'fulfillment': output['condition']['details'],
                'fulfills': {
                'output_index': output_index,
                'transaction_id': datos_armas[0]['id'],
                },
            'owners_before': output['public_keys'],
            }
            transfer_asset = {'id': datos_armas[0]['id'],}
            prepared_transfer_tx = conexion.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                recipients=[([publica_comprador], cantidadRequerida), ([publica_vendedor], resto_armas)]
            )
            fulfilled_transfer_tx = conexion.transactions.fulfill(
                prepared_transfer_tx, private_keys=privada_vendedor)
            sent_transfer_tx = conexion.transactions.send_commit(fulfilled_transfer_tx)

            #Cobro
            resto_monedas=(cantidad_monedas-totalCompra)
            o_index = 0
            output = datos_moneda[0]['outputs'][o_index]
            transfer_input = {
                'fulfillment': output['condition']['details'],
                'fulfills': {
                'output_index': o_index,
                'transaction_id': datos_moneda[0]['id'],
                },
            'owners_before': output['public_keys'],
            }
            transfer_asset = {'id': datos_moneda[0]['id'],}
            prepared_transfer_tx = conexion.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                recipients=[([publica_vendedor], totalCompra), ([publica_comprador], resto_monedas)]
            )
            fulfilled_transfer_tx = conexion.transactions.fulfill(
                prepared_transfer_tx, private_keys=privada_comprador)
            sent_transfer_tx = conexion.transactions.send_commit(fulfilled_transfer_tx)

            return render_template("comprado.html", usuario=comprador, cantidad=cantidadRequerida, nombre=nombreArma)
        else:
            return render_template("monedas_insuficientes.html", usuario=usuario_comprador)
    else:
        return render_template("armas_insuficientes.html", usuario=usuario_comprador)

@app.route('/transferirMonedas', methods=["POST"])
def transferirMonedas():
    conexion = connect_db()
    if request.method == 'POST':
        publica = request.form['publica'] 
    resultado = bbdd.buscarMonedas()
    cantidad_monedas = 0
    for e in resultado:
        datos=conexion.transactions.get(asset_id=e['id'])
        cant=len(datos)-1
        outs=datos[cant]['outputs']
        canti=len(outs)-1
        for i in outs:
            if (i['condition']['details']['public_key']==publica):
                cantidad_monedas=(cantidad_monedas+int(i['amount']))
    return render_template("transferirMonedas.html", monedas=cantidad_monedas) 

@app.route('/confirmarTransferencia', methods=["POST"])
def confirmarTransferencia():
    conexion = connect_db()
    if request.method == 'POST':
        cantidad = int(request.form['cantidad'] )
        destinatario = request.form['destinatario'] 
        monedas= int(request.form['monedas'])
    resultado = bbdd.buscarUsuarios()
    for e in resultado:
        if (e['usuario']=="Darth vader"):
            usuario_emisor=e['usuario']
            privada_emisor=e['privada']
            publica_emisor=e['publica']
        if (e['usuario']==destinatario):
            usuario_destinatario=e['usuario']
            privada_destinatario=e['privada']
            publica_destinatario=e['publica']
    mon = []
    if (cantidad<=monedas):
        mone = bbdd.buscarMonedas()
        datos = [] 
        canti = [] 
        for e in mone:
            datos.append(conexion.transactions.get(asset_id=e['id']))
            for d in datos:
                cant=(len(d)-1)
                cant=int(cant)
                outs=d[cant]['outputs']
                clave = outs[0]['condition']['details']['public_key']
                if (clave == publica_emisor):
                    canti.append(int(outs[0]['amount']))
                    mon.append(d[0]['id'])
        id_moneda = mon[0]
        cantidad_monedas = int(canti[0])
        datos_moneda=conexion.transactions.get(asset_id=id_moneda)
        if (cantidad_monedas>=cantidad):
            resto_monedas=(cantidad_monedas-cantidad)
            o_index = 0
            output = datos_moneda[0]['outputs'][o_index]
            transfer_input = {
                'fulfillment': output['condition']['details'],
                'fulfills': {
                'output_index': o_index,
                'transaction_id': datos_moneda[0]['id'],
                },
            'owners_before': output['public_keys'],
            }
            transfer_asset = {'id': datos_moneda[0]['id'],}
            prepared_transfer_tx = conexion.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                recipients=[([publica_destinatario], cantidad), ([publica_emisor], resto_monedas)]
            )
            fulfilled_transfer_tx = conexion.transactions.fulfill(
                prepared_transfer_tx, private_keys=privada_emisor)
            sent_transfer_tx = conexion.transactions.send_commit(fulfilled_transfer_tx)

            return render_template("transferido.html", monedas=cantidad, destinatario=usuario_destinatario)
        else:
            return render_template("transfer_insuficiente.html")
    else:
        return render_template("transfer_insuficiente.html")


def transferir(id, cantidad, publica_emisor, privada_emisor, publica_receptor):
    conexion = connect_db()
    fulfilled_token_tx=conexion.transactions.get(asset_id=id)
    o_index = 0
    output = fulfilled_token_tx[0]['outputs'][o_index]
    transfer_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
            'output_index': o_index,
            'transaction_id': fulfilled_token_tx[0]['id'],
            },
        'owners_before': output['public_keys'],
    }
    transfer_asset = {'id': fulfilled_token_tx[0]['id'],}
    amount=fulfilled_token_tx[0]['outputs'][0]['amount']
    amount=int(amount)
    resto = (amount-cantidad)
    prepared_transfer_tx = conexion.transactions.prepare(
        operation='TRANSFER',
        asset=transfer_asset,
        inputs=transfer_input,
        recipients=[([publica_receptor], cantidad), ([publica_emisor], resto)])
    fulfilled_transfer_tx = conexion.transactions.fulfill(prepared_transfer_tx, private_keys=privada_emisor)
    sent_transfer_tx = conexion.transactions.send_commit(fulfilled_transfer_tx)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)