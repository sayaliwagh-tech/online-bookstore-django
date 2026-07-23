


from django.core.management.base import BaseCommand
from books.models import Category
from books.models import Category, Author, Book
from decimal import Decimal
from datetime import date


class Command(BaseCommand):
    help = "Seed BookVerse database"

    def handle(self, *args, **kwargs):

        categories = [
            "Programming",
            "Python",
            "Java",
            "C++",
            "SQL",
            "Data Analytics",
            "Machine Learning",
            "Artificial Intelligence",
            "Django",
            "Web Development",
            "Computer Science",
            "Self Help",
            "Finance",
            "Business",
            "Biography",
            "Fiction",
            "History",
            "Cyber Security",
        ]

        for category in categories:
            Category.objects.get_or_create(name=category)

        # self.stdout.write(
        #     self.style.SUCCESS("✅ Categories Added Successfully!")
        # )
        
        self.stdout.write(
            self.style.SUCCESS(
                "✅ Categories and Authors Added Successfully!"
            )
        )


# 
authors = [
    {
        "name": "Robert C. Martin",
        "biography": "Known as Uncle Bob, Robert C. Martin is a software engineer and author of Clean Code. He has over four decades of experience in software development and advocates writing clean, maintainable code."
    },
    {
        "name": "Eric Matthes",
        "biography": "Eric Matthes is the author of Python Crash Course, one of the world's most popular beginner-friendly Python books."
    },
    {
        "name": "Andrew Hunt",
        "biography": "Andrew Hunt is a programmer, publisher, and co-author of The Pragmatic Programmer, one of the most influential software engineering books."
    },
    {
        "name": "David Thomas",
        "biography": "David Thomas is a software developer and co-author of The Pragmatic Programmer, helping developers improve coding practices."
    },
    {
        "name": "James Clear",
        "biography": "James Clear is an author, speaker, and productivity expert best known for the bestselling book Atomic Habits."
    },
    {
        "name": "Morgan Housel",
        "biography": "Morgan Housel is a financial writer and author of The Psychology of Money, focusing on behavioral finance."
    },
    {
        "name": "Walter Isaacson",
        "biography": "Walter Isaacson is a bestselling biographer known for books on Steve Jobs, Leonardo da Vinci, and Albert Einstein."
    },
    {
        "name": "Andrew Ng",
        "biography": "Andrew Ng is an AI pioneer, educator, and founder of DeepLearning.AI, recognized for advancing machine learning education."
    },
    {
        "name": "Aurélien Géron",
        "biography": "Aurélien Géron is the author of Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow."
    },
    {
        "name": "Robert Kiyosaki",
        "biography": "Robert Kiyosaki is the author of Rich Dad Poor Dad and an entrepreneur known for financial education."
    }
]

for author in authors:
    Author.objects.get_or_create(
        name=author["name"],
        defaults={
            "biography": author["biography"]
        }
    )
    
   
# books
books = [

{
"title":"Clean Code",
"author":"Robert C. Martin",
"category":"Programming",
"description":"A practical guide to writing clean, maintainable, and efficient software.",
"price":799,
"stock":20,
"isbn":"9780132350884"
},

{
"title":"The Clean Coder",
"author":"Robert C. Martin",
"category":"Programming",
"description":"Professional practices for software developers.",
"price":699,
"stock":15,
"isbn":"9780137081073"
},

{
"title":"Python Crash Course",
"author":"Eric Matthes",
"category":"Python",
"description":"A beginner-friendly introduction to Python programming.",
"price":899,
"stock":25,
"isbn":"9781593279288"
},

{
"title":"Automate the Boring Stuff with Python",
"author":"Al Sweigart",
"category":"Python",
"description":"Learn Python by automating everyday tasks.",
"price":699,
"stock":30,
"isbn":"9781593275990"
},

{
"title":"The Pragmatic Programmer",
"author":"Andrew Hunt",
"category":"Programming",
"description":"Classic software engineering best practices.",
"price":999,
"stock":20,
"isbn":"9780201616224"
},

{
"title":"Hands-On Machine Learning",
"author":"Aurélien Géron",
"category":"Machine Learning",
"description":"Machine Learning using Scikit-Learn, Keras and TensorFlow.",
"price":1199,
"stock":15,
"isbn":"9781492032649"
},

{
"title":"The Psychology of Money",
"author":"Morgan Housel",
"category":"Finance",
"description":"Timeless lessons on wealth and behavior.",
"price":599,
"stock":40,
"isbn":"9780857197689"
},

{
"title":"Atomic Habits",
"author":"James Clear",
"category":"Self Help",
"description":"Build good habits and break bad ones.",
"price":699,
"stock":50,
"isbn":"9781847941831"
},

{
"title":"Rich Dad Poor Dad",
"author":"Robert Kiyosaki",
"category":"Finance",
"description":"Personal finance and investing lessons.",
"price":499,
"stock":35,
"isbn":"9781612680194"
},

{
"title":"Steve Jobs",
"author":"Walter Isaacson",
"category":"Biography",
"description":"Biography of Steve Jobs.",
"price":899,
"stock":12,
"isbn":"9781451648539"
},
]


# 
for book in books:

    author = Author.objects.get(name=book["author"])
    category = Category.objects.get(name=book["category"])

    Book.objects.get_or_create(

        isbn=book["isbn"],

        defaults={

            "title": book["title"],
            "author": author,
            "category": category,
            "description": book["description"],
            "price": Decimal(book["price"]),
            "stock": book["stock"],
            "publication_date": date.today(),

        }

    )