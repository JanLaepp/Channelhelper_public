class BookPicker:
    def __init__(self):
        self.jan_list = [0,0]
        self.nina_list = [0,0]
        self.sukriti_list = [0,0]
    
    def get_last_book_in_order(self, history):
        for book in history:
            if book.listowner != "--":
                return book

    def get_next_order(self,file_name):
        """get next order for book determination as string: <name1>;<name2>;<name3>"""
        from BookBean import BookBean as bean
        history = bean.get_history(file_name)
        last_book = self.get_last_book_in_order(history)
        next_list_owner = ""
        next_selection = ""
        next_pick = ""
        print("Last listowner")
        print(last_book.listowner)
        if last_book.listowner == "Jan":
            print("last listowner was jan")
            next_list_owner = "Nina"
            print("next: " + next_list_owner)
        elif last_book.listowner == "Nina":
            next_list_owner = "Sukriti"
        elif last_book.listowner == "Sukriti":
            next_list_owner = "Jan"

        for book in history:
            if book.listowner == "Jan":
                if book.selection == "Nina":
                    self.jan_list[0] += 1
                else:
                    self.jan_list[1] += 1
            if book.listowner == "Nina":
                if book.selection == "Jan":
                    self.nina_list[0] += 1
                else:
                    self.nina_list[1] += 1
            if book.listowner == "Sukriti":
                if book.selection == "Jan":
                    self.sukriti_list[0] += 1
                else:
                    self.sukriti_list[1] += 1
        
        print("next: " + next_list_owner)
        if next_list_owner == "Jan":
            minimum = min(self.jan_list)
            next = self.jan_list.index(minimum)
            if next == 0:
                next_selection = "Nina"
                next_pick = "Sukriti"
            else:
                next_selection = "Sukriti"
                next_pick = "Nina"
        if next_list_owner == "Nina":
            print("new listowner nina")
            minimum = min(self.jan_list)
            next = self.jan_list.index(minimum)
            if next == 0:
                next_selection = "Jan"
                next_pick = "Sukriti"
            else:
                next_selection = "Sukriti"
                next_pick = "Jan"
        if next_list_owner == "Sukriti":
            minimum = min(self.jan_list)
            next = self.jan_list.index(minimum)
            if next == 0:
                next_selection = "Jan"
                next_pick = "Nina"
            else:
                next_selection = "Nina"
                next_pick = "Jan"

        return next_list_owner+";"+next_selection+";"+next_pick