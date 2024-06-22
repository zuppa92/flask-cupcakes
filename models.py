from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

cupcake_ingredients = db.Table('cupcake_ingredients',
    db.Column('cupcake_id', db.Integer, db.ForeignKey('cupcakes.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
)

class Cupcake(db.Model):
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False, default='https://tinyurl.com/demo-cupcake')

    ingredients = db.relationship('Ingredient', secondary=cupcake_ingredients, backref='cupcakes')

    def serialize(self):
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image,
            "ingredients": [ingredient.name for ingredient in self.ingredients]
        }

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

