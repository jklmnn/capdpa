
import unittest
import clang.cindex
from capdpa import *
from capdpa_test import *

class Parser(Capdpa_Test):

    def test_empty_namespace(self):
        expected = Namespace(name = "Capdpa", children = [Namespace(name = "Empty")])
        result = CXX("tests/data/test_empty_namespace.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_constants(self):
        expected = Namespace(name = "Capdpa", children = [Namespace(name = "With_constants",
            children = [
                Constant(name = "X", value = 1),
                Constant(name = "Y", value = 2),
                Constant(name = "Z", value = 3)])])
        result = CXX("tests/data/test_namespace_with_constants.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_empty_class(self):
        expected = Namespace(name = "Capdpa", children = [Class(name = "Empty")])
        result = CXX("tests/data/test_empty_class.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_class(self):
        expected = Namespace(name = "Capdpa", children = [Namespace (name = "With_class",
                children = [Class(name = "In_namespace")])])
        result = CXX("tests/data/test_namespace_with_class.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_enum(self):
        expected = Namespace(name = "Capdpa", children = [Namespace (name = "With_enum",
                children = [
                    Enum(name = "WEEKEND", children = [
                        Constant(name = "SATURDAY", value = 0),
                        Constant(name = "SUNDAY", value = 1)]),
                    Enum(name = "Constants", children = [
                        Constant(name = "ONE", value = 1),
                        Constant(name = "TWO", value = 2),
                        Constant(name = "THREE", value = 3)])])])
        result = CXX("tests/data/test_namespace_with_enum.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_constants(self):
        expected = Namespace(name = "Capdpa", children = [Class (name = "With_constants",
                children = [Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2),
                    Constant(name = "THREE", value = 3),
                    Enum(name = "NEGATIVE", children = [
                        Constant(name = "MINUS_ONE", value = -1),
                        Constant(name = "MINUS_TWO", value = -2),
                        Constant(name = "MINUS_THREE", value = -3)])])])
        result = CXX("tests/data/test_class_with_constants.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_members(self):
        expected = Namespace(name = "Capdpa", children = [Class(name = "With_members",
                children = [
                    Variable (name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                    Variable (name = "public_pointer", ctype = Type_Reference(name = Identifier(["System", "Address"]), pointer = 0)),
                    Variable (name = "public_float", ctype = Type_Reference(name = Identifier(["Capdpa", "C_float"])))])])
        result = CXX("tests/data/test_class_with_members.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_functions(self):
        expected = Namespace(name = "Capdpa", children = [Class(name = "With_functions",
                children = [
                    Function(name = "public_function", symbol = "", parameters = [
                        Variable (name = "arg1", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))]),
                    Function(name = "named_param", symbol = "", parameters = [
                        Variable (name = "param", ctype = Type_Reference(name = Identifier(["Capdpa", "int"])))],
                        return_type = Type_Reference(name = Identifier(["Capdpa", "int"]))
                        ),
                    Constructor(symbol = "")])])
        result = CXX("tests/data/test_class_with_functions.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_namespace_with_class_with_everything(self):
        expected = Namespace(name = "Capdpa", children = [Namespace(name = "With_class", children = [
            Class(name = "With_everything",
                children = [
                    Constant(name = "ONE", value = 1),
                    Constant(name = "TWO", value = 2),
                    Enum(name = "NEGATIVE", children = [
                        Constant(name = "MINUS_ONE", value = -1),
                        Constant(name = "MINUS_TWO", value = -2)]),
                    Function(name = "public_function", symbol = ""),
                    Variable(name = "public_int", ctype = Type_Reference(name = Identifier(["Capdpa", "int"]))),
                    Constructor(symbol = "")])])])
        result = CXX("tests/data/test_namespace_with_class_with_everything.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_class_with_class_type(self):
        expected = Namespace(name = "Capdpa", children = [
                Namespace (name = "With_class",
                    children = [Class(name = "In_namespace")]),
                Class(name = "Full",
                    children = [
                        Variable(name = "value", ctype = Type_Reference(name = Identifier(["Capdpa", "With_class", "In_namespace", "Class"]))),
                        Variable(name = "value_ptr", ctype = Type_Reference(name = Identifier(["Capdpa", "With_class", "In_namespace", "Class"]), pointer = 1))
                    ])])
        result = CXX("tests/data/test_class_with_class_type.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_types(self):
        expected = Namespace(name = "Capdpa", children = [
                Type_Definition(
                    name="uint8_t",
                    reference=Type_Reference(name=Identifier(name=["Capdpa", "unsigned_char"]), pointer=0)),
                Type_Definition(
                    name="int32_t",
                    reference=Type_Reference(name=Identifier(name=["Capdpa", "int"]), pointer=0)),
                Type_Definition(name="u8", reference=Type_Reference(name=Identifier(name=["uint8_t"]), pointer=0))])
        result = CXX("tests/data/test_types.h").ToIR(project="Capdpa")
        self.check(result, expected)

    def test_template_conversion(self):
        cxx = CXX("tests/data/test_with_template.h")
        cursor = list(cxx.translation_unit.cursor.get_children())[0]
        template = getattr(CXX, "_CXX__convert_template")(cxx, cursor)
        expected = Template(entity=Class(name="Container", children=[
            Variable(name="a", ctype=Template_Argument(name="A")),
            Variable(name="b", ctype=Template_Argument(name="B"))]), typenames=[
                Template_Argument(name="A"),
                Template_Argument(name="B")])

    def test_template_engine(self):
        typea = Type_Reference(name=Identifier(["typeA"]))
        typeb = Type_Reference(name=Identifier(["typeB"]))
        expected = Class(name="Container_T_typeA_typeB", children=[
            Variable(name="a", ctype=Type_Reference(name=Identifier(["typeA"]))),
            Variable(name="b", ctype=Type_Reference(name=Identifier(["typeB"])))])
        template = Template(entity=Class(name="Container", children=[
            Variable(name="a", ctype=Template_Argument(name="A")),
            Variable(name="b", ctype=Template_Argument(name="B"))]), typenames=[
                Template_Argument(name="A"),
                Template_Argument(name="B")])
        result = template.instantiate([typea, typeb])
        self.check(result, expected)
        self.check(template, Template(entity=Class(name="Container", children=[
            Variable(name="a", ctype=Template_Argument(name="A")),
            Variable(name="b", ctype=Template_Argument(name="B"))]), typenames=[
                Template_Argument(name="A"),
                Template_Argument(name="B")]))

    def test_template(self):
        expected = Namespace(name = "Capdpa", children = [
            Class(name = "Container_T_int_char", children = [
                Variable(name = "A", ctype = Type_Reference(name = Identifier(["Capdpa", "Int"]))),
                Variable(name = "B", ctype = Type_Reference(name = Identifier(["Capdpa", "Char"])))]),
            Class(name = "Container_T_int_int", children = [
                Variable(name = "A", ctype = Type_Reference(name = Identifier(["Capdpa", "Int"]))),
                Variable(name = "B", ctype = Type_Reference(name = Identifier(["Capdpa", "Int"])))]),
            Class(name = "User", children = [
                Variable(name = "cic", ctype = Type_Reference(name = Identifier(["Capdpa", "Container_T_int_char"]))),
                Variable(name = "cii", ctype = Type_Reference(name = Identifier(["Capdpa", "Container_T_int_int"]))),
                Variable(name = "cic2", ctype = Type_Reference(name = Identifier(["Capdpa", "Container_T_int_char"])))
                ])])
        result = CXX("tests/data/test_with_template.h").ToIR(project="Capdpa")
        self.check(result, expected)
