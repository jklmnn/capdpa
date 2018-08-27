import ir
import ir_class

class Namespace(ir_class.Class):

    def __init__(self, name, namespaces=None, classes=None, constants=None, enums=None):
        self.namespaces = namespaces or []
        self.classes = classes or []
        super(Namespace, self).__init__(name      = name,
                                        constants = constants,
                                        enums     = enums)
        self.constructors = None
