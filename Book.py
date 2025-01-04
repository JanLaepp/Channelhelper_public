class Book:
    def __init__(self,title,listowner,selection,pick):
        self.title = title
        self.listowner = listowner
        self.selection = selection
        self.pick = pick

    def get_name(self):
        return self.title
    
    def get_listowner(self):
        return self.listowner
    
    def get_selection(self):
        return self.selection
    
    def get_pick(self):
        return self.pick