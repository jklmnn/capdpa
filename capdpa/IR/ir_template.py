from copy import deepcopy

class UnspecifiedTemplate: pass

class Template(object):

    def __init__(self, entity, typenames):
        self.entity = entity
        self.typenames = typenames

    def __eq__(self, other):
        return self.__repr__() == repr(other)

    def __ne__(self, other):
        return not self.__eq__(other)


    def __repr__(self):
        return "Template(entity={}, typenames={})".format(
                self.entity, self.typenames)

    def __replace(self, entity, resolves):
        if hasattr(entity, "children"):
            for c in entity.children:
                if c in resolves.keys():
                    c = resolves[c]
                self.__replace(c, resolves)
        if hasattr(entity, "parameters"):
            for c in entity.parameters:
                if c in resolves.keys():
                    c = resolves[c]
                self.__replace(c, resolves)
        if hasattr(entity, "ctype"):
            if entity.ctype in resolves.keys():
                entity.ctype = resolves[entity.ctype]
        if hasattr(entity, "return_type"):
            if entity.return_type in resolves.keys():
                entity.return_type = resolves[entity.return_type]

    def instantiate(self, args):
        resolves = {t[0]:t[1] for t in zip(self.typenames, args)}
        entity = deepcopy(self.entity)
        self.__replace(entity, resolves)
        entity.name += "_T_" + "_".join(["_".join(a.name.name) for a in args])
        return entity

    def postfix(self):
        return "_T_{}".format(
                "_".join([arg.name for arg in self.arguments]))

class Template_Argument(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.__repr__() == repr(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Template_Argument(name={})".format(
                self.name)

    def __hash__(self):
        return hash(self.__repr__())

