from crud.crud_author import CRUDAuthor  
from crud.crud_book import CRUDBook       
from crud.crud_review import CRUDReview   

# Pre-instantiated singletons ready to use in endpoints:
author_crud = CRUDAuthor()
book_crud = CRUDBook()
review_crud = CRUDReview()
