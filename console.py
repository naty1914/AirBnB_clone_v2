#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.stdin.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.stdin.isatty():
            print('(hbnb)')

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.stdin.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        elif args not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[args]()
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.split(" ")
        c_name = new[0]
        c_id = ""
        if len(new) > 1:
            c_id = new[1]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in self.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        obj = storage.all().get(key)
        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.split(" ")
        c_name = new[0]
        c_id = ""
        if len(new) > 1:
            c_id = new[1]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in self.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        objects = storage.all()
        obj = objects.get(key)
        if obj:
            del objects[key]
            storage.save()
        else:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        objects = storage.all()
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in self.classes:
                print("** class doesn't exist **")
                return
            for k, v in objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for v in objects.values():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k in storage.all().keys():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        new = args.split(" ")
        if len(new) < 3:
            print("** class name missing **")
            return
        if len(new) < 4:
            print("** instance id missing **")
            return
        if len(new) < 5:
            print("** attribute name missing **")
            return
        if len(new) < 6:
            print("** value missing **")
            return

        c_name, c_id, att_name, att_val = new[0], new[1], new[2], new[3]
        key = c_name + "." + c_id
        objects = storage.all()
        obj = objects.get(key)
        if obj:
            att_val = att_val.strip("\"'")
            if hasattr(obj, att_name):
                setattr(obj, att_name, att_val)
                storage.save()
            else:
                print("** no instance found **")
        else:
            print("** no instance found **")

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
