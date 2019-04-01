from storage.author import Author, AuthorNotFound
from wiring import Wiring


wiring = Wiring()
"""
cardPushkin = wiring.author_dao.create(
    Author(
        first_name="Александр",
        last_name="Пушкин",
        middle_name="Сергеевич")
)

cardKing = wiring.author_dao.create(
    Author(
        first_name="Стивен",
        last_name="Кинг",
        middle_name="")
)

a = wiring.author_dao.get_by_last_name('Пушкин')
for item in a:
    print(item.first_name)

"""

# all = wiring.author_dao.get_all()
# for item in all:
#    print(item.name)

item = wiring.genre_dao.get_by_slug("child_sf")
print(item.name)