#!/usr/bin/python3
"""Main Console for Techie Mate"""
import cmd
from models import storage
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.message import Message
from models.roadmap import Roadmap
from models.course import Course
from models.vendor import Vendor


class TechieMateCommand(cmd.Cmd):
    """ Contains the functionality for the TechieMate console"""
    prompt = "(TechieMate) "
    allowed_classes = ["BaseModel",
                       "User",
                       "Message",
                       "Roadmap",
                       "Course",
                       "Vendor"]
    allowed_methods = ["all", "count", "show", "destroy", "update"]
    objects = storage.all()

    def parse(self, arg):
        """parse inputs into command args"""
        commands = split(arg)
        return commands

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """ EOF, exit program """
        print("")
        return True

    def emptyline(self):
        """ empty line, do nothing """
        pass

    def do_create(self, arg):
        """
        Usage: create <class>
        Desc: creates a new instance of <class>
            and prints out its id
        """
        commands = self.parse(arg)
        if len(commands) == 0:
            self.class_name_missing()
        elif commands[0] not in self.allowed_classes:
            self.class_not_found()
        elif len(commands) > 1:
            arg_all = commands[1:]
            ins = eval(commands[0])()
            for arg in arg_all:
                items = arg.split('=')
                key = items[0]
                value = '='.join(items[1:])
                try:
                    value = eval(value)
                except Exception:
                    value = value.replace('_', ' ').replace('"', '\"')
                    value = value.replace("'", "\'")
                if hasattr(ins, key):
                    setattr(ins, key, value)
            ins.save()
            print(ins.id)
        else:
            ins = eval(commands[0])()
            ins.save()
            print(ins.id)

    def do_show(self, arg):
        """
        Usage: show <class> <instance id>
        Desc: prints out the instance of class <class>
            and <instance id>
        """
        commands = self.parse(arg)
        if len(commands) == 0:
            self.class_name_missing()
        elif commands[0] not in self.allowed_classes:
            self.class_not_found()
        elif len(commands) == 1:
            self.instance_id_missing()
        elif "{}.{}".format(commands[0], commands[1]) not in self.objects:
            self.instance_not_found()
        else:
            print(self.objects["{}.{}".format(commands[0], commands[1])])

    def do_destroy(self, arg):
        """
        Usage: destroy <class> <instance id>
        Desc: destroys the instance of class <class>
            and <instance id>
        """
        commands = self.parse(arg)
        if len(commands) == 0:
            self.class_name_missing()
        elif commands[0] not in self.allowed_classes:
            self.class_not_found()
        elif len(commands) == 1:
            self.instance_id_missing()
        elif "{}.{}".format(commands[0], commands[1]) not in self.objects:
            self.instance_not_found()
        else:
            del self.objects["{}.{}".format(commands[0], commands[1])]
            storage.save()

    def do_all(self, arg):
        """
        Usage: all | all <class>
        Desc: prints out a list of all instances of
            all classes or certain <class>
        """
        commands = self.parse(arg)
        if len(commands) == 0:
            print([self.objects[i].__str__() for i in self.objects])
        elif len(commands) == 1 and commands[0] not in self.allowed_classes:
            self.class_not_found()
        else:
            objs = self.objects
            print([objs[i].__str__() for i in objs if f"{commands[0]}." in i])

    def do_update(self, arg):
        """
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        Desc: update instance of <id> of class <class name>
            and changes/adds {attribute name: attribute value} pair
        """
        commands = self.parse(arg)
        if len(commands) == 0:
            self.class_name_missing()
        elif commands[0] not in self.allowed_classes:
            self.class_not_found()
        elif len(commands) == 1:
            self.instance_id_missing()
        elif "{}.{}".format(commands[0], commands[1]) not in self.objects:
            self.instance_not_found()
        elif len(commands) == 2:
            self.attribute_name_missing()
        elif len(commands) == 3:
            self.attribute_value_missing()
        else:
            item = self.objects["{}.{}".format(commands[0], commands[1])]
            try:
                value = eval(commands[3])
            except Exception:
                value = commands[3]
            setattr(item, commands[2], value)
            storage.save()

    def class_name_missing(self):
        """** class name missing **"""
        print("** class name missing **")

    def class_not_found(self):
        """** class doesn't exist **"""
        print("** class doesn't exist **")

    def instance_id_missing(self):
        """** instance id missing **"""
        print("** instance id missing **")

    def instance_not_found(self):
        """** no instance found **"""
        print("** no instance found **")

    def attribute_name_missing(self):
        """** attribute name missing **"""
        print("** attribute name missing **")

    def attribute_value_missing(self):
        """** value missing **"""
        print("** value missing **")

    def default(self, arg):
        """
        handling exceptional commands
        """
        commands = self.parse(arg)
        if len(commands) == 0:
            self.emptyline()
        elif len(commands) == 1:
            class_name = commands[0].split('.')[0]
            class_cmd = commands[0].split('.')[-1].split('(')[0]
            case1 = class_name in self.allowed_classes
            case2 = class_cmd in self.allowed_methods
            case3 = '()' in commands[0].split('.')[-1]
            if case1 and case2:
                args = commands[0].split('.')[-1].split('(')[-1].split(')')[0]
                if class_cmd == "all" and case3:
                    self.do_all(class_name)
                elif class_cmd == "count" and case3:
                    o = self.objects
                    cnt = [o[i].__str__() for i in o if f"{class_name}." in i]
                    print(len(cnt))
                elif class_cmd == "show" and not case3:
                    self.do_show(f"{class_name} {args}")
                elif class_cmd == "destroy":
                    self.do_destroy(f"{class_name} {args}")
                else:
                    print(f"*** Unknown syntax: {commands[0]}")
            else:
                print(f"*** Unknown syntax: {commands[0]}")
        elif len(commands) == 3:
            class_name = commands[0].split('.')[0]
            class_cmd = commands[0].split('.')[-1].split('(')[0]
            case1 = class_name in self.allowed_classes
            case2 = class_cmd in self.allowed_methods
            if case1 and case2 and class_cmd == "update":
                id = commands[0].split('(')[-1].split(',')[0]
                attr_name = commands[1].split(',')[0]
                attr_value = commands[2].split(')')[0]
                attr_value = f'"""{attr_value}"""'
                self.do_update(f"{class_name} {id} {attr_name} {attr_value}")
            else:
                print(f"*** Unknown syntax: {commands[0]}")
        else:
            print(f"*** Unknown syntax: {commands[0]}")


if __name__ == '__main__':
    TechieMateCommand().cmdloop()
