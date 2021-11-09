from core import app
import resources

app.route('/')(resources.inicio)
app.route('/Receta')(resources.receta)
app.route('/Crear_Receta', methods = ["POST", "GET"])(resources.crearReceta)
app.route('/Receta/<id>')(resources.receta)
