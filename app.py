from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake, Ingredient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcakes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

connect_db(app)
db.create_all()

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/ingredients')
def ingredients_page():
    """Render the ingredients management page."""
    return render_template('ingredients.html')

@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    """Get data about all cupcakes."""
    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_cupcake(id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake."""
    data = request.json
    ingredient_names = data.get('ingredients', [])
    ingredients = []
    for name in ingredient_names:
        ingredient = Ingredient.query.filter_by(name=name).first()
        if not ingredient:
            ingredient = Ingredient(name=name)
            db.session.add(ingredient)
        ingredients.append(ingredient)

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data.get('image', 'https://tinyurl.com/demo-cupcake'),
        ingredients=ingredients
    )
    db.session.add(new_cupcake)
    db.session.commit()
    return jsonify(cupcake=new_cupcake.serialize()), 201

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Update a cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    data = request.json
    ingredient_names = data.get('ingredients', [])
    ingredients = []
    for name in ingredient_names:
        ingredient = Ingredient.query.filter_by(name=name).first()
        if not ingredient:
            ingredient = Ingredient(name=name)
            db.session.add(ingredient)
        ingredients.append(ingredient)

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']
    cupcake.ingredients = ingredients

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete a cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

@app.route('/api/ingredients', methods=['GET'])
def list_ingredients():
    """Get data about all ingredients."""
    ingredients = Ingredient.query.all()
    serialized = [ingredient.serialize() for ingredient in ingredients]
    return jsonify(ingredients=serialized)

@app.route('/api/ingredients', methods=['POST'])
def create_ingredient():
    """Create a new ingredient."""
    data = request.json
    new_ingredient = Ingredient(name=data['name'])
    db.session.add(new_ingredient)
    db.session.commit()
    return jsonify(ingredient=new_ingredient.serialize()), 201

@app.route('/api/ingredients/<int:id>', methods=['PATCH'])
def update_ingredient(id):
    """Update an ingredient."""
    ingredient = Ingredient.query.get_or_404(id)
    data = request.json

    ingredient.name = data['name']

    db.session.commit()
    return jsonify(ingredient=ingredient.serialize())

@app.route('/api/ingredients/<int:id>', methods=['DELETE'])
def delete_ingredient(id):
    """Delete an ingredient."""
    ingredient = Ingredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify(message="Deleted")

@app.route('/api/cupcakes/search', methods=['GET'])
def search_cupcakes():
    """Search for cupcakes by flavor."""
    term = request.args.get('q', '')
    cupcakes = Cupcake.query.filter(Cupcake.flavor.ilike(f"%{term}%")).all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)

if __name__ == '__main__':
    app.run(debug=True)
