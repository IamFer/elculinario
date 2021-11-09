from flask import app, render_template, request, redirect

from models import *
from utils import debug

recetas = []
ingredientesReceta = []
pasosReceta = []

ing_porcion = []

receta1 = Receta(
    id = 0,
    nombre = 'Clasico Pastel de Queso',
    autor = 'Fernando',
    dificultad = 'Complicada',
    tiempo = '63 min.',
    calorias = '321 cal.',
    costo = '73.50',
    calificacion = '4.99',
    imagen = 'https://images.unsplash.com/photo-1567190562512-6b787f7dc2aa',
    desc =  'Aqui establecimos el estándar para el mejor cheesecake.'+
            'Esta receta de la versión clásica siempre agradará a todo mundo.',
)

ingredientesReceta.append([
    ['Migajas de galletas graham', '1 ó 1/2 taza'],
    ['Azúcar granulada', '3 cucharadas y 1 taza'],
    ['Mantequilla o margarina, derretida', '1/3 taza'],
    ['Paquete de 8 oz de queso crema PHILADELPHIA Cream Cheese, ablandado', '4 paquetes (8 oz. cada uno)'],
    ['Esencia de Vainilla', '1 cucharadita'], 
    ['Huevos', '4 piezas']
])

receta1.agregar_paso("Calienta el horno a 325ºF")
receta1.agregar_paso(
    "Mezcla las migajas, 3 cdas. de azúcar y la mantequilla;"
    +" presiona esto firmemente contra el fondo de un molde con "
    +" aro desmontable (springform pan) de 9 pulgs.")
receta1.agregar_paso(
    "Bate bien el queso crema, 1 taza de azúcar y la vainilla en "
    +" un tazón grande con una batidora eléctrica. "
    +" Agrega uno por uno los huevos; después de añadir cada uno, "
    +" bate a velocidad baja sólo hasta mezclarlo."
    +" Vierte la mezcla en la base del pastel.")
receta1.agregar_paso("Hornea el cheesecake 55 min. o hasta que el centro esté casi cuajado."
    +" Pasa un cuchillo o espátula de metal por el borde del molde para despegar el pastel;"
    +" déjalo enfriar antes de quitarle el aro al molde. Refrigéralo durante 4 horas.")

pasosReceta.append(receta1.mostrar_pasos())

receta2 = Receta(
    id = 1,
    nombre = "Pasta Qui Sait Quoi",
    autor = 'Jaime',
    dificultad = 'Normal',
    tiempo = '55 min.',
    calorias = '450 cal.',
    costo = '150.00',
    calificacion = '3.99',
    imagen = 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8',
    desc =  'Aqui establecimos el estándar para la mejor Pasta.'+
            ' Esta receta de la versión clásica siempre agradará a todo mundo.'
)

ingredientesReceta.append([
    ['Agua', '1 taza'],
    ['Leche Evaporada CARNATION® CLAVEL®', '1 lata'],
    ['Queso crema', '2 Paquetes (190 g c/u)'],
    ['Sal con cebolla en polvo', '1, 1/2 Cucharadita'],
    ['Pasta tornillo, cocida y escurrida', '400 Gramos'],
    ['Perejil fresco picado ', '1/4 Taza']
])

receta2.agregar_paso(
    "Licúa la Leche Evaporada CARNATION® CLAVEL® con el agua, el queso crema y la sal con cebolla en polvo; "
    +" cocina a fuego bajo por 15 minutos o hasta que espese ligeramente, mueve constantemente para evitar que se pegue; "
    +" retira del fuego.")
receta2.agregar_paso(
    "Sirve la pasta caliente, baña con la salsa de queso y espolvorea con perejil picado.")
receta2.agregar_paso(
    "Recuerda que 1 envase de Leche Evaporada CARNATION® CLAVEL® de 360 g es equivalente a 1 lata de 360 g, "
    +" con la cremosidad de siempre.")
receta2.agregar_paso("Utiliza leche descremada en lugar de leche entera para reducir tu consumo de grasa.")

pasosReceta.append(receta2.mostrar_pasos())

recetas.append(receta1)
recetas.append(receta2)

def inicio():
    return render_template('Inicio.html', recetas = recetas)

def receta(id):
    id = min([len(recetas)-1, int(id)])

    return render_template('VerReceta.html', recetas = recetas[id], ingredientesProporcion = ingredientesReceta[id], pasos = pasosReceta[id])

def crearReceta():
    if request.method == 'GET':
        return render_template('CrearReceta.html')

    datos = request.form

    receta_aux = Receta(
        id = len(recetas),
        nombre = datos['platillo'],
        autor = datos['autor'],
        dificultad = datos['dificultad'],
        tiempo = datos['tiempo'] + ' min.',
        calorias = datos['calorias'] + ' cal.',
        costo = datos['costo'],
        calificacion = '5.00',
        imagen = datos['imagen'],
        desc =  datos['desc'],
    )

    i = 1
    while i < len(datos):
        if f"ingrediente{i}" in datos and f"porcion{i}" in datos:
            ing_porcion.clear()
            ing_porcion.append(datos[f'ingrediente{i}'])
            ing_porcion.append(datos[f'porcion{i}'])
           
            receta_aux.agregar_ingrediente(ing_porcion[:])

        if f"paso{i}" in datos:
            receta_aux.agregar_paso(datos[f'paso{i}'])
            
        if f"ingrediente{i}" not in datos and f"porcion{i}" not in datos and f"paso{i}" not in datos:
            break

        i += 1

        pasosReceta.append(receta_aux.mostrar_pasos())
        ingredientesReceta.append(receta_aux.mostrar_ingredientes())
        continue

    recetas.append(receta_aux)

    return redirect(f'/Receta/{receta_aux.id}')
