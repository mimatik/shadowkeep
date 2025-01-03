class Inventory(list):
    def of_type(self, *args):
        return Inventory(
            [item for item in self if any([isinstance(item, cls) for cls in args])]
        )
