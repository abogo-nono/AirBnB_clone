import cmd, sys
from models.base_model import BaseModel

class TC(cmd.Cmd):
    prompt = "(hbnb) "
    
    def do_quit(self, line):
        """Quit command to exit the program"""
        return True
    
    
    def do_EOF(self, line):
        """EOF command to exit the program"""
        return True
    

    def do_greet(self, firstname, lastname):
        """Syntax: greet <firstname> <lastname>"""
        if firstname and lastname:
            print(f"Hello {firstname} {lastname}")
        else:
            print("Syntax: greet <firstname> <lastname>")

if __name__ == '__main__':
    TC().cmdloop()
    