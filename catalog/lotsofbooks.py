# Mock up items to populate the database for testing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Language, Base, Work

engine = create_engine('sqlite:///worldliterature.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Works in Arabic
language1 = Language(language="Arabic")
session.add(language1)
session.commit()

work1 = Work(title='Arabian Nights', 
	author='Not Known', 
	translator='James Baldwin', 
	translation_year='1700', genre='Tales',
	amazon_link='www.amazon.com/Arabian', 
	language=language1, 
	summary='balalalalalalalalalal')
session.add(work1)
session.commit()

work2 = Work(title='A', 
	author='Jaja', 
	translator='Babula', 
	translation_year='1990', 
	genre='novel', 
	amazon_link='www.amazon.com', 
	language=language1, 
	summary='balalalalalalalalalal')
session.add(work2)
session.commit()

work3 = Work(title='Aladin', 
	author='Jaja', 
	translator='Babula', 
	translation_year='1990', 
	genre='novel', 
	amazon_link='www.amazon.com', 
	language=language1, 
	summary='balalalalalalalalalal')
session.add(work3)
session.commit()


# Works in German
language2 = Language(language="German")
session.add(language2)
session.commit()

work1 = Work(title='Faustus', 
	author='Jaja', translator='Babula', 
	translation_year='1990', genre='novel', 
	amazon_link='www.amazon.com', language=language2, 
	summary='balalalalalalalalalal')
session.add(work1)
session.commit()

work2 = Work(title='Werther Sorrows', 
	author='Jaja', translator='Babula', 
	translation_year='1990', 
	genre='novel', 
	amazon_link='www.amazon.com', 
	language=language2, 
	summary='balalalalalalalalalal')
session.add(work2)
session.commit()

work3 = Work(title='Poets', 
	author='Jaja', 
	translator='Babula', 
	translation_year='1990', 
	genre='novel', 
	amazon_link='www.amazon.com', 
	language=language2, 
	summary='balalalalalalalalalal')
session.add(work3)
session.commit()


# Works in French
language3 = Language(language="French")
session.add(language3)
session.commit()

work1 = Work(title='A la Recherche du Temps Perdue', 
	author='Jaja', translator='Babula', 
	translation_year='1990', 
	genre='novel', 
	amazon_link='www.amazon.com', 
	language=language3, 
	summary='balalalalalalalalalal')
session.add(work1)

session.commit()
work2 = Work(title='Le Pere Goriot', 
	author='Jaja', translator='Babula', 
	translation_year='1990', 
	genre='novel', 
	amazon_link='www.amazon.com', 
	language=language3, 
	summary='balalalalalalalalalal')
session.add(work2)
session.commit()


# Works in Persian
language4 = Language(language="Persian")
session.add(language4)
session.commit()

work1 = Work(title='Souls', 
	author='Jaja', 
	translator='Babula', 
	translation_year='1990', 
	genre='novel', 
	amazon_link='www.amazon.com', 
	language=language4, 
	summary='balalalalalalalalalal')
session.add(work1)
session.commit()

work2 = Work(title='Shahname', 
	author='Jaja', translator='Babula', 
	translation_year='1990', genre='novel', 
	amazon_link='www.amazon.com', 
	language=language4, 
	summary='balalalalalalalalalal')
session.add(work2)
session.commit()

work3 = Work(title='Layla and Majnu', 
	author='Jaja', translator='Babula', 
	translation_year='1990', 
	genre='novel', 
	amazon_link='www.amazon.com', 
	language=language4, 
	summary='balalalalalalalalalal')
session.add(work3)
session.commit()



print "added new works!"