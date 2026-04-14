"""
Models Package:

Re-exports every model + Base , so we can do from models import .....
This also ensures Base.metadata knows about ALL tables
when we call create_all().
"""

from core.database import Base          
from models.author import Author       
from models.book import Book            
from models.review import Review        
