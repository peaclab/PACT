class Model:
    def __init__(self):
        self.lib_dict={}
        self.config_label_dict={}
        self.label_prop_dict={}
        return


    def add_lib_dict(self,lib_dict):
        self.lib_dict=lib_dict
        return

    def add_label_prop_dict(self,label_prop_dict):
        self.label_prop_dict=label_prop_dict
        return 

    def add_config_label_dict(self,config_label_dict):
        self.config_label_dict = config_label_dict
        try:
            self.label_config_dict = dict.fromkeys([(x,y) for y in config_label_dict.keys() for x in config_label_dict[y]])
        except:
            print("ERROR: config_label_dict should be a dictionary")
            sys.exit(2)
        return
