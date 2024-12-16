# Import the get_db_connection function from the database.connection module
from database.connection import get_db_connection

# Define the Author class
class Author:
    def __init__(self, id=None, name=None):
        self._id = id  # Directly set _id
        if id is not None:
            self._name = None  # Placeholder for name, will be fetched if needed
        if name is not None:
            self.name = name  # Set name through the setter if provided
    
    # Define a property for the id attribute
    @property
    def id(self):
        return self._id

    # Define a property for the name attribute
    @property
    def name(self):
        if not hasattr(self, '_name'):
            # Fetch the name from the database if it has not been set
            self._fetch_name_from_db()
        return self._name

    # Define a setter method for the name property
    @name.setter
    def name(self, value):
        # Check if the value is a string and has a valid length
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) == 0:
            raise ValueError("Name must be longer than 0 characters")
        # Set the name attribute
        self._name = value
    
    def _fetch_name_from_db(self):
        """Helper function to fetch the author's name from the database."""
        if self._id is None:
            raise ValueError("Author ID is required to fetch name")
        
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute the query to fetch the name from the database
        cursor.execute('SELECT name FROM authors WHERE id = ?', (self._id,))
        result = cursor.fetchone()
        
        if result:
            self._name = result[0]
        else:
            raise ValueError(f"Author with ID {self._id} not found in database")
        
        conn.close()

    # Define a method to fetch articles associated with the author
    def articles(self):
        # Import the Article class
        from models.article import Article
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute an SQL SELECT query to fetch articles written by the author
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self._id,))
        # Fetch all rows returned by the query
        articles = cursor.fetchall()
        conn.close()
        
        # Return a list of Article instances created from the fetched articles
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]
    
    # Define a method to fetch magazines associated with the author
    def magazines(self):
        # Import the Magazine class
        from models.magazine import Magazine
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute an SQL SELECT query to fetch distinct magazines where the author has published articles
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self._id,))
        
        # Fetch all rows returned by the query
        magazines = cursor.fetchall()
        conn.close()
        
        # Return a list of Magazine instances created from the fetched magazines
        return [Magazine(magazine['id'], magazine['name'], magazine['category']) for magazine in magazines]

    # Define the string representation (__repr__) method for Author instances
    def __repr__(self):
        return f'<Author {self.name}>'
