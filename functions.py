
import databaseConnector
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.INFO,
                    filename='quotebook.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )



async def getQuoteFromAuthor(author):
    session = databaseConnector.get_session()
    try:
        sql_query = "SELECT * FROM quote WHERE author = :author"
        stmt = text(sql_query)
        POM_quotes_results = session.execute(stmt, {"author": author})
        quotes_from_pom = POM_quotes_results.all()
        return quotes_from_pom
    except SQLAlchemyError as e:
        logging.error(f"Error from getting quotes from author from DB: {e}")


async def getRandomAuthor():
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT AUTHOR FROM quote ORDER BY RANDOM() LIMIT 1"
        stmt = text(sql_query)
        POM_result = session.execute(stmt)
        person_of_month = POM_result.first().author
        return person_of_month
    except SQLAlchemyError as e:
        logging.error(f"Error from getting random author from DB: {e}")


async def getRandomQuote():
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT * FROM quote ORDER BY RANDOM() LIMIT 1"
        stmt = text(sql_query)
        rand_quote_result = session.execute(stmt)
        rand_quote = rand_quote_result.first()
        return rand_quote
    except SQLAlchemyError as e:
        logging.error(f"Error from getting random quote from DB: {e}")

async def appendToQuote(author, quote, quote_date, context, user_id):
    try:
        session = databaseConnector.get_session()
        sql_query = "INSERT INTO quote(author, content, quote_date, context, user_id) VALUES(:author, :content, :quote_date, :context, :user_id) RETURNING id"
        stmt = text(sql_query)
        result = session.execute(stmt, {"author": author, "content": quote, "quote_date": quote_date, "context": context, "user_id": user_id})
        new_id=result.scalar_one()
        session.commit()
        return new_id
    except SQLAlchemyError as e:
        logging.error(f"Error adding quote to DB: {e}")

async def quoteExists(content, author):
    try:
           session = databaseConnector.get_session()
           sql_query = "SELECT COUNT(*) FROM quote WHERE content = :content AND author = :author"
           stmt = text(sql_query)
           result = session.execute(stmt, {"author": author, "content": content})
           result = result.scalar_one()
           sql_query = "SELECT quote_id FROM quote WHERE content = :content AND author = :author"
           stmt = text(sql_query)
           quote_id_results = session.execute(stmt, {"author": author, "content": content})
           quote_id = quote_id_results.scalar_one()
           if result != 0:
               return True
           elif result < 1:
                logging.error(f"Duplicate quotes found, quote ID = {quote_id}")
           else:
               return False
    except SQLAlchemyError as e:
        logging.error(f"Error checking if quote exists in DB: {e}")

async def quoteExistsFromID(quote_id):
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT COUNT(*) FROM quote WHERE quote_id = :quote_id"
        stmt = text(sql_query)
        result = session.execute(stmt, {"quote_id": quote_id})
        result = result.scalar_one()
        if result != 0:
            return True
        elif result < 1:
            logging.error(f"Duplicate quotes found, quote ID = {quote_id}")
            return True
        else:
            return False
    except SQLAlchemyError as e:
        logging.error(f"Error checking if quote exists in DB: {e}")



async def searchQuotes(search):
    try:
        session = databaseConnector.get_session()
        search = f"%{search}%"
        sql_query = "SELECT * FROM quote WHERE content ILIKE :search OR author ILIKE :search"
        stmt = text(sql_query)
        result = session.execute(stmt, {"search": search})
        session.commit()
        return result.all()
    except SQLAlchemyError as e:
        logging.error(f"Error searching quotes from DB: {e}")

async def getRelated(quote):
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT content FROM quote WHERE author = :author AND id <> :id"
        stmt = text(sql_query)
        relateds_result = session.execute(stmt, {"author": quote.author, "id": quote.id})
        relateds = relateds_result.all()
        return relateds
    except SQLAlchemyError as e:
        logging.error(f"Error getting related quotes from DB: {e}")


async def getQuote(quote_id):
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT * FROM quote WHERE id = :id"
        stmt = text(sql_query)
        db_result = session.execute(stmt, {"id": quote_id})
        quote = db_result.first()
        return quote
    except SQLAlchemyError as e:
        logging.error(f"Error fetching quote with id from DB: {e}")

async def getQuoteFromAuthor(author):
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT * FROM quote WHERE author = :author"
        stmt = text(sql_query)
        POM_quotes_results = session.execute(stmt, {"author": author})
        quotes_from_pom = POM_quotes_results.all()
        return quotes_from_pom
    except SQLAlchemyError as e:
        logging.error(f"Error fetching quote with author from DB: {e}")


async def getRandomAuthor():
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT AUTHOR FROM quote ORDER BY RANDOM() LIMIT 1"
        stmt = text(sql_query)
        POM_result = session.execute(stmt)
        person_of_month = POM_result.first().author
        return person_of_month
    except SQLAlchemyError as e:
        logging.error(f"Error fetching random author from DB: {e}")


async def getUsernameFromID(user_id):
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT username FROM users WHERE user_id = :user_id"
        stmt = text(sql_query)
        username_result = session.execute(stmt, {"user_id": user_id})
        username = username_result.scalar_one()
        return username
    except SQLAlchemyError as e:
        logging.error(f"Error fetching username with ID from DB: {e}")

async def getUser_IDFromUsername(username):
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT user_id FROM users WHERE username = :username"
        stmt = text(sql_query)
        user_id_result = session.execute(stmt, {"username": username})
        user_id = user_id_result.scalar_one()
        return user_id
    except SQLAlchemyError as e:
        logging.error(f"Error fetching user ID with username from DB: {e}")



async def getRandomQuote():
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT * FROM quote ORDER BY RANDOM() LIMIT 1"
        stmt = text(sql_query)
        rand_quote_result = session.execute(stmt)
        rand_quote = rand_quote_result.first()
        return rand_quote
    except SQLAlchemyError as e:
        logging.error(f"Error fetching random quote from DB: {e}")

async def getAllQuotes():
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT * FROM quote"
        stmt = text(sql_query)
        quotes_result = session.execute(stmt)
        quote = quotes_result.all()
        return quote
    except SQLAlchemyError as e:
        logging.error(f"Error fetching all quotes from DB: {e}")



async def checkIfUserExists(username: str):
    try:
        session = databaseConnector.get_session()
        sql_query = "SELECT COUNT(*) FROM users WHERE username = :username"
        stmt = text(sql_query)
        user_result = session.execute(stmt, {"username": username})
        user_count = user_result.scalar_one()
        return user_count
    except SQLAlchemyError as e:
        logging.error(f"Error checking if user exists from DB: {e}")

async def findUserFromUsernameAndPasswordHash(password_hash: str, username: str) -> Row[*tuple[Any, ...]] | None:
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM users WHERE username = :username AND :password_hash = password_hash"
    stmt = text(sql_query)
    signin_result = session.execute(stmt, {"username": username, "password_hash": password_hash})
    user = signin_result.first()
    return user

async def removeQuote(quote_id):
    try:
        session = databaseConnector.get_session()
        sql_query = "DELETE * FROM quote WHERE quote_id = :quote_id"
        stmt = text(sql_query)
        session.execute(stmt, {"quote_id": quote_id})
        return f"Quote of ID: '{quote_id}' removed successfully!"
    except SQLAlchemyError as e:
        logging.error(f"Error removing quote from DB: {e}")
