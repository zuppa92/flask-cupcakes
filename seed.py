from app import app
from models import db, Cupcake

db.drop_all()
db.create_all()

cupcake1 = Cupcake(flavor="chocolate", size="large", rating=5, image="https://tinyurl.com/demo-cupcake")
cupcake2 = Cupcake(flavor="vanilla", size="medium", rating=4.5, image="https://tinyurl.com/demo-cupcake2")

db.session.add_all([cupcake1, cupcake2])
db.session.commit()
