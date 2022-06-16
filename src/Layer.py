import pandas as pd
import sys


class Layer:
    def __init__(self, lcf_row, defaultConfigFile, virtual_node_locations):
        self.layer_num = lcf_row['Layer']
        self.create_flp_df(lcf_row['FloorplanFile'],
                           defaultConfigFile, virtual_node_locations)
        self.thickness = float(lcf_row['Thickness (m)'])
        self.LateralHeatFlow = lcf_row['LateralHeatFlow']
        self.VerticalHeatFlow = lcf_row['VerticalHeatFlow']
        self.append_ptraces(lcf_row['PtraceFile'])
        self.others = {}
        self.display()
        return
    # Create floorplan dataframe

    def create_flp_df(self, flp_file, defaultConfigFile, virtual_node_locations):
        flp_df = pd.read_csv(flp_file)
        self.flp_file = flp_file
        self.flp_df = flp_df.sort_values(['Y', 'X'], ascending=True)
        if (self.flp_df.iloc[0].X != 0):
            self.flp_df['X'] = self.flp_df['X'] - min(self.flp_df['X'])
        if (self.flp_df.iloc[0].Y != 0):
            self.flp_df['Y'] = self.flp_df['Y'] - min(self.flp_df['Y'])
        self.length = self.flp_df.iloc[-1].X + \
            self.flp_df.iloc[-1]['Length (m)']
        self.width = self.flp_df.iloc[-1].Y + self.flp_df.iloc[-1]['Width (m)']
        self.flp_df["ConfigFile"].fillna(defaultConfigFile, inplace=True)
        virtual_nodes = [virtual_node_locations[x]
                         for x in flp_df['Label'].unique()]
        if("center_center" in virtual_nodes):
            self.virtual_node = "center_center"
        else:
            self.virtual_node = "bottom_center"

        return
    # add ptrace lines if there is more than one power lines

    def append_ptraces(self, ptrace_file):
        self.num_ptrace_lines = 1
        if (not pd.isnull(ptrace_file)):
            ptrace_df = pd.read_csv(ptrace_file)
            units_ptrace = ptrace_df["UnitName"].values.tolist()
            units_flp = self.flp_df["UnitName"].values.tolist()
            units_ptrace.sort()
            units_flp.sort()
            if not (len(units_flp) == len(units_ptrace)):
                print(
                    f'Mismatch between number of blocks in flp file ({self.flp_file}) and ptrace file ({ptrace_file})')
                sys.exit(-1)
            if not (units_flp == units_ptrace):
                print(
                    f'Mismatch between block names in flp file ({self.flp_file}) and ptrace file ({ptrace_file})')
                sys.exit(-1)

            self.flp_df = pd.merge(
                self.flp_df, ptrace_df, on="UnitName", how='outer')
            self.num_ptrace_lines = len(ptrace_df.columns) - 1
        else:
            self.flp_df['Power'] = 0
        return

    def add_Rx(self, numpy_arr):
        self.Rx = numpy_arr

    def add_Lock(self, numpy_arr):
        self.Lock = numpy_arr

    def add_g2bmap(self, numpy_arr):
        self.g2bmap = numpy_arr

    def add_Ry(self, numpy_arr):
        self.Ry = numpy_arr

    def add_Rz(self, numpy_arr):
        self.Rz = numpy_arr

    def add_C(self, numpy_arr):
        self.C = numpy_arr

    def add_I(self, numpy_arr):
        self.I = numpy_arr

    def add_Conv(self, numpy_arr):
        self.Conv = numpy_arr

    def update_others_constants(self, key, val):
        self.others[key] = val

    def display(self):
        pass
        return

    def get_num_ptrace_lines(self):
        return self.num_ptrace_lines

    def add_power_densities(self, numpy_arr):
        self.power_densities = numpy_arr
