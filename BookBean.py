import os
from BookPicker import BookPicker
from Book import Book
from Config.python_definitions import ROOT_DIR

class BookBean:
    def get_history(file_name):
        """
        Reads the history from the passed file and returns it as a list of books
        """
        file = open(os.path.join(ROOT_DIR, 'Database', file_name), "r")
        bookhistory = []
        in_history = False #boolean to check if we're in the history portion of the file yet
        for line in file:
            if in_history:
                print(line)
                line = line.strip()
                print(line)
                (title,listowner,selection,pick) = line.split(";")
                book = Book(title,listowner,selection,pick)
                bookhistory.append(book)
            else:
                if line == "History:\n":
                    in_history = True
        file.close()
        return bookhistory
    

    def get_next_book(file_name):
        """Returns book that was just set up"""
        file = open(os.path.join(ROOT_DIR, 'Database', file_name), "r")
        line = file.readline().strip()
        args = line.split(";")
        return Book(*args)
    
    def write_history(file_name):
        """
        Adds a new book to the history file
        """
        bookhistory = BookBean.get_history(file_name)
        new_book = BookBean.get_next_book(file_name)
        bookhistory.insert(0,new_book)
        file = open(os.path.join(ROOT_DIR, 'Database', file_name), "w+")
        file.write(new_book.title+";"+new_book.listowner+";"+new_book.selection+";"+new_book.pick+"\n")
        file.write("History:\n")
        for book in bookhistory:
            file.write(book.title+";"+book.listowner+";"+book.selection+";"+book.pick+"\n")
        file.close()

    def book_setup(file_name,book_title,order = None, out_of_order_bool = False):
        if out_of_order_bool:
            next_book = Book(book_title, "--", "--", "--")
        else:
            names = ["Jan","Nina","Sukriti"]
            if order == None:
                bookpicker = BookPicker()
                order = bookpicker.get_next_order(file_name)
            order = order.split(";")
            if set(order) == set(names):
                next_book = Book(book_title,*order)
            else:
                raise ValueError
                
        history = BookBean.get_history(file_name)
        file = open(os.path.join(ROOT_DIR, 'Database', file_name), "w+")
        file.write(next_book.title+";"+next_book.listowner+";"+next_book.selection+";"+next_book.pick+"\n")
        file.write("History:\n")
        for book in history:
            file.write(book.title+";"+book.listowner+";"+book.selection+";"+book.pick+"\n")
        file.close()
        return next_book
        