from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_character = Table(
    "favorite_character",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key = True),
    Column("character_id", ForeignKey("character.id"), primary_key = True)
)

favorite_location = Table(
    "favorite_location",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key = True),
    Column("location_id", ForeignKey("location.id"), primary_key = True)
)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    favorites_characters: Mapped[list["Character"]] = relationship("Character", secondary = favorite_character, back_populates = "favorited_by")
    favorites_locations: Mapped[list["Location"]] = relationship("Location", secondary = favorite_location, back_populates = "favorited_by")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites_characters": [character.serialize() for character in self.favorites_characters],
            "favorites_locations": [location.serialize() for location in self.favorites_locations]
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    quote: Mapped[str] = mapped_column(String(120), nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=True)

    favorited_by: Mapped[list["User"]] = relationship("User", secondary = favorite_character, back_populates = "favorites_characters")


    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "image": self.image
        }
    
class Location(db.Model):
    __tablename__ = "location"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=False)
    town: Mapped[str] = mapped_column(String(120), nullable=False)
    use: Mapped[str] = mapped_column(String(120), nullable=False)

    favorited_by: Mapped[list["User"]] = relationship("User", secondary = favorite_location, back_populates = "favorites_locations")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "town": self.town,
            "use": self.use
        }