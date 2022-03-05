from models.news import News
from models.user import User
from models.db import db
from models.raiting import Rating
from models.subject import Subject
from app import app

db.init_app(app)
app.app_context().push()

try:
    User.__table__.drop(db.engine)
    News.__table__.drop(db.engine)
    Rating.__table__.drop(db.engine)
    Subject.__table__.drop(db.engine)
except:
    pass

db.create_all()

a = User(name="Tanya", email="tanya@kataev.pro", password="12345")
b = User(name="Vita", email="vita@kataev.pro", password="12345")
c = User(name="Alonka", email="alonka@kataev.pro", password="12345", is_teacher=True)

d = News(title='Новость 1', description="Описание 1", text='ТекстТекстТекстТекстТекст', img='1.jpg')
e = News(title='Новость 2', description="Описание 2", text='ТекстТекстТекстТекстТекст', img='2.jpg')
f = News(title='Новость 3', description="Описание 3", text='ТекстТекстТекстТекстТекстl', img='3.jpg')

subj1 = Subject(name="Русский язык")
subj2 = Subject(name="Информатика")
subj3 = Subject(name="Математика")
subj4 = Subject(name="Физика")
subj5 = Subject(name="Химия")
subj6 = Subject(name="История")
subj7 = Subject(name="Технология")

db.session.add_all([a, b, c, subj1, subj2, subj3, subj4, subj5, subj6, subj7])

db.session.commit()
