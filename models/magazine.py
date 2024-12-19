# Import the get_db_connection function from the database.connection module
from database.connection import get_db_connection

# Define the Magazine class
class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self._id = id
        if name:
            self.name = name  # Set name using the setter
        if category:
            self.category = category  # Set category using the setter

    # Define a property for the id attribute
    @property
    def id(self):
        return self._id
    
    # Define a property for the name attribute
    @property
    def name(self):
        return self._name
    
    # Define a setter method for the name property
    @name.setter
    def name(self, value):
        # Check if the value is a string
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        # Check if the length of the name is between 2 and 16 characters
        if not (1 <= len(value) <= 20):  # Changed to 1-20 characters
          raise ValueError("Name must be between 1 and 20 characters")
        # Set the name attribute
        self._name = value

    # Define a property for the category attribute
    @property
    def category(self):
        return self._category
    
    # Define a setter method for the category property
    @category.setter
    def category(self, value):
        # Check if the value is a string
        if not isinstance(value, str):
            raise ValueError("Category must be a string")
        # Check if the length of the category is greater than 0
        if len(value) <= 0:
            raise ValueError("Category must be longer than 0 characters")
        # Set the category attribute
        self._category = value
        # Update the category in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (value, self._id))
        conn.commit()
        conn.close()

    # Define a method to fetch articles associated with the magazine
    def articles(self):
        # Import the Article class
        from models.article import Article
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        # Execute an SQL SELECT query to fetch articles belonging to the magazine
        cursor.execute('''
            SELECT * FROM articles WHERE magazine_id = ?
        ''', (self._id,))
        # Fetch all rows returned by the query
        articles = cursor.fetchall()
        # Close the database connection
        conn.close()
        # Return a list of Article instances created from the fetched articles
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]
    
    # Define a method to fetch contributors (authors) for the magazine
    def contributors(self):
        # Import the Author class
        from models.author import Author
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        # Execute an SQL SELECT query to fetch distinct authors contributing to the magazine
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self._id,))
        # Fetch all rows returned by the query
        authors = cursor.fetchall()
        # Close the database connection
        conn.close()
        # Return a list of Author instances created from the fetched authors
        return [Author(author['id'], author['name']) for author in authors]

    # Define a method to fetch titles of articles associated with the magazine
    def article_titles(self):
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        # Execute an SQL SELECT query to fetch titles of articles belonging to the magazine
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self._id,))
        # Fetch all rows returned by the query and extract titles
        titles = [row['title'] for row in cursor.fetchall()]
        # Close the database connection
        conn.close()
        # Return the list of article titles
        return titles
    
    # Define a method to fetch authors who contributed more than two articles to the magazine
    def contributing_authors(self):
        # Import the Author class
        from models.author import Author
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        # Execute an SQL SELECT query to fetch authors with more than two articles contributed to the magazine
        cursor.execute('''
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self._id,))
        # Fetch all rows returned by the query
        authors = cursor.fetchall()
        # Close the database connection
        conn.close()
        # Return a list of Author instances created from the fetched authors
        return [Author(author['id'], author['name']) for author in authors]

    # Define the string representation (__repr__) method for Magazine instances
    def __repr__(self):
        return f'<Magazine {self.name}>'
