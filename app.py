from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input for new entities
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    '''
        The following is for testing purposes.
        You can modify it to meet the requirements of your implementation.
    '''

    # Create an author and get the author_id
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid  # Use this to fetch the ID of the newly created author

    # Create a magazine and get the magazine_id
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid  # Use this to fetch the ID of the newly created magazine

    # Create an article and associate it with the author and magazine
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    # Commit the changes to the database
    conn.commit()

    # Query the database for inserted records
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    # Close the connection to the database
    conn.close()

    # Display the results by instantiating objects from the fetched data
    print("\nMagazines:")
    for magazine in magazines:
        # Instantiate a Magazine object
        magazine_obj = Magazine(magazine["id"], magazine["name"], magazine["category"])
        print(magazine_obj)

    print("\nAuthors:")
    for author in authors:
        # Instantiate an Author object
        author_obj = Author(author["id"], author["name"])
        print(author_obj)

    print("\nArticles:")
    for article in articles:
        # Instantiate an Article object
        article_obj = Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"])
        print(article_obj)

if __name__ == "__main__":
    main()
