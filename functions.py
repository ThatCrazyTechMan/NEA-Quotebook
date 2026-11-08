
import databaseConnector
from sqlalchemy import text



async def getQuoteFromAuthor(author):
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote WHERE author = :author"
    stmt = text(sql_query)
    POM_quotes_results = session.execute(stmt, {"author": author})
    quotes_from_pom = POM_quotes_results.all()
    return quotes_from_pom


async def getRandomAuthor():
    session = databaseConnector.get_session()
    sql_query = "SELECT AUTHOR FROM quote ORDER BY RANDOM() LIMIT 1"
    stmt = text(sql_query)
    POM_result = session.execute(stmt)
    person_of_month = POM_result.first().author
    return person_of_month


async def getRandomQuote():
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote ORDER BY RANDOM() LIMIT 1"
    stmt = text(sql_query)
    rand_quote_result = session.execute(stmt)
    rand_quote = rand_quote_result.first()
    return rand_quote

async def appendToQuote(author, quote, date, context, user_id):
    session = databaseConnector.get_session()
    sql_query = "INSERT INTO quote(author, content, date, context, user_id) VALUES(:author, :content, :date, :context, :user_id) RETURNING id"
    stmt = text(sql_query)
    result = session.execute(stmt, {"author": author, "content": quote, "date": date, "context": context, "user_id": user_id})
    new_id=result.scalar_one()
    session.commit()

    return new_id

async def quoteExists(content, author):
       session = databaseConnector.get_session()
       sql_query = "SELECT COUNT(*) FROM quote WHERE content = :content AND author = :author"
       stmt = text(sql_query)
       result = session.execute(stmt, {"author": author, "content": content})
       result = result.scalar_one()
       session.commit()
       print(result)
       if result != 0:
           return True
       else:
           return False


async def searchQuotes(search):
    session = databaseConnector.get_session()
    search = f"%{search}%"
    sql_query = "SELECT * FROM quote WHERE content ILIKE :search OR author ILIKE :search"
    stmt = text(sql_query)
    result = session.execute(stmt, {"search": search})
    session.commit()
    return result.all()

async def getRelated(quote):
    session = databaseConnector.get_session()
    sql_query = "SELECT content FROM quote WHERE author = :author AND id <> :id"
    stmt = text(sql_query)
    relateds_result = session.execute(stmt, {"author": quote.author, "id": quote.id})
    relateds = relateds_result.all()
    return relateds


async def getQuote(quote_id):
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote WHERE id = :id"
    stmt = text(sql_query)
    db_result = session.execute(stmt, {"id": quote_id})
    quote = db_result.first()
    return quote

async def getQuoteFromAuthor(author):
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote WHERE author = :author"
    stmt = text(sql_query)
    POM_quotes_results = session.execute(stmt, {"author": author})
    quotes_from_pom = POM_quotes_results.all()
    return quotes_from_pom


async def getRandomAuthor():
    session = databaseConnector.get_session()
    sql_query = "SELECT AUTHOR FROM quote ORDER BY RANDOM() LIMIT 1"
    stmt = text(sql_query)
    POM_result = session.execute(stmt)
    person_of_month = POM_result.first().author
    return person_of_month


async def getUsernameFromID(user_id):
    session = databaseConnector.get_session()
    sql_query = "SELECT username FROM users WHERE user_id = :user_id"
    stmt = text(sql_query)
    username_result = session.execute(stmt, {"user_id": user_id})
    username = username_result.scalar_one()
    return username

async def getUser_IDFromUsername(username):
    session = databaseConnector.get_session()
    sql_query = "SELECT user_id FROM users WHERE username = :username"
    stmt = text(sql_query)
    user_id_result = session.execute(stmt, {"username": username})
    user_id = user_id_result.scalar_one()
    return user_id



async def getRandomQuote():
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote ORDER BY RANDOM() LIMIT 1"
    stmt = text(sql_query)
    rand_quote_result = session.execute(stmt)
    rand_quote = rand_quote_result.first()
    return rand_quote

async def getAllQuotes():
    session = databaseConnector.get_session()
    sql_query = "SELECT * FROM quote"
    stmt = text(sql_query)
    quotes_result = session.execute(stmt)
    quote = quotes_result.all()
    return quote