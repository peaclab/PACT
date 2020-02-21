class GridCell:
    def __init__(self,unit_data, length, width, thickness):
        self.length=length
        self.width=width
        self.thickness=thickness
        self.power=0
        try:
            self.unit_dict.add(unit_data)
        except:
            self.unit_data = unit_data
            print("EXCEPT BLOCK")
        return




