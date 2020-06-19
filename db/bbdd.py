from pymongo import MongoClient
import os

def connect():
    conexion = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
    return conexion

def seleccionarBaseDeDatos():
    conexion=connect()
    db = conexion.activos
    return db

def insertarUsuario(usuario, privada, publica):
    db = seleccionarBaseDeDatos()
    collection = db.usuarios
    collection.insert({
                "usuario" : usuario,
                "privada" : privada,
                "publica" : publica
            })

def buscarUsuarios():
    db = seleccionarBaseDeDatos()
    collection = db.usuarios
    resultado=collection.find()
    return resultado

def insertarArma(id, usuario, privada, publica, nombre, cantidad, costo):
    db = seleccionarBaseDeDatos()
    collection = db.armas
    collection.insert({
                "id" : id,
                "usuario" : usuario,
                "privada" : privada,
                "publica" : publica,
                "nombre" : nombre,
                "cantidad" : cantidad,
                "costo" : costo
            })

def buscarArmas():
    db = seleccionarBaseDeDatos()
    collection = db.armas
    resultado=collection.find()
    return resultado

def insertarMoneda(id, usuario, privada, publica, nombre, cantidad):
    db = seleccionarBaseDeDatos()
    collection = db.monedas
    collection.insert({
                "id" : id,
                "usuario" : usuario,
                "privada" : privada,
                "publica" : publica,
                "nombre" : nombre,
                "cantidad" : cantidad
            })

def buscarMonedas():
    db = seleccionarBaseDeDatos()
    collection = db.monedas
    resultado=collection.find()
    return resultado

def eliminarColeccion():
    db = seleccionarBaseDeDatos()
    collection = db.monedas
    collection.drop()
