from database.connection import get_db_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id
        
        # If the article is new (i.e., id is None), insert it into the database
        if self._id is None and title is not None:
            self.insert_article()
        elif self._id is not None:
            self.fetch_article_data()

    def insert_article(self):
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute an SQL INSERT query to insert the article into the articles table
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       (self._title, self._content, self._author_id, self._magazine_id))

        # Get the last inserted row ID and assign it to the id attribute
        self._id = cursor.lastrowid

        # Commit the transaction and close the database connection
        conn.commit()
        conn.close()

    # Define a property for the title attribute
    @property
    def title(self):
        # If the title is not already set, fetch the article data (this happens if the article was fetched from the database)
        if not hasattr(self, '_title') and self._id is not None:
            self.fetch_article_data()
        return self._title

    # Define a setter method for the title property
    @title.setter
    def title(self, value):
        if self._id is not None:
            raise ValueError("Title cannot be changed after the article is created")
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value
        else:
            raise ValueError("Title must be a string and between 5 and 50 characters")

    # Define a property for the content attribute
    @property
    def content(self):
        if not hasattr(self, '_content'):
            self.fetch_article_data()
        return self._content

    # Define a setter method for the content property
    @content.setter
    def content(self, value):
        if self._id is not None:
            raise ValueError("Content cannot be changed after the article is created")
        if isinstance(value, str):
            self._content = value
        else:
            raise ValueError("Content must be a string")

    # Fetch article-related data from the database (title, content, author, magazine)
    def fetch_article_data(self):
        if self._id is None:
            raise ValueError("Article ID is required to fetch data")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT title, content, author_id, magazine_id FROM articles WHERE id = ?
        ''', (self._id,))
        result = cursor.fetchone()

        if result:
            self._title = result[0]
            self._content = result[1]
            self._author_id = result[2]
            self._magazine_id = result[3]
        else:
            raise ValueError("Article not found in the database")

        conn.close()

    def __repr__(self):
        return f'<Article {self.title}>'
