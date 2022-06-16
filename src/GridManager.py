import sys
import numpy as np
import pandas as pd
import math
import Solid as LibSolid
import HeatSink as LibHeatSink
import HeatSpreader as LibHeatSpreader
import Liquid as LibLiquid
import HybridWick as LibHybridWick
import MicroWick as LibMicroWick
import sys

# round functions for grid edge


def round_to_grid_X(coord, grid_dim):
    tmp = round(float(coord)/grid_dim, 40)
    tmp_floor = math.floor(tmp)
    tmp_ceil = math.ceil(tmp)
    if (abs(tmp-tmp_ceil)) > 0.001:
        return tmp_floor
    else:
        return tmp_ceil


def round_to_grid_tmp(coord, grid_dim):
    tmp = round(float(coord)/grid_dim, 40)
    tmp_floor = math.floor(tmp)
    tmp_ceil = math.ceil(tmp)
    print(tmp, tmp_ceil, abs(tmp-tmp_ceil))
    if (abs(tmp-tmp_ceil)) > 0.001:
        print(f"X,FLOOR: {tmp_floor}")
        return float(tmp_floor)
    else:
        print(f"X,CEIL: {tmp_ceil}")
        return float(tmp_ceil)


def round_to_grid_Y(coord, grid_dim):
    tmp = round(float(coord)/grid_dim, 40)
    tmp_floor = math.floor(tmp)
    tmp_ceil = math.ceil(tmp)
    if (abs(tmp-tmp_ceil)) > 0.001:
        return tmp_floor
    else:
        return tmp_ceil


class GridManager:
    def __init__(self, config_grid):
        self.grid_dict = config_grid
        self.Lock = np.zeros(
            (int(self.grid_dict['rows']), int(self.grid_dict['cols'])))
        self.Rx = np.zeros(
            (int(self.grid_dict['rows']), int(self.grid_dict['cols'])))
        self.Ry = np.zeros(
            (int(self.grid_dict['rows']), int(self.grid_dict['cols'])))
        self.Rz = np.zeros(
            (int(self.grid_dict['rows']), int(self.grid_dict['cols'])))
        self.C = np.zeros(
            (int(self.grid_dict['rows']), int(self.grid_dict['cols'])))
        self.Conv = np.zeros(
            (int(self.grid_dict['rows']), int(self.grid_dict['cols'])))
        self.others = {}
        self.g2bmap = np.empty(
            [int(self.grid_dict['rows']), int(self.grid_dict['cols'])], dtype="<U10")
        self.vector_evaluateRC = np.vectorize(self.evaluateRC, otypes=[None])
        return

    def add_label_config_mode_dict(self, label_config_dict, defaultConfig, label_mode_dict):
        self.label_config_dict = label_config_dict
        self.label_mode_dict = label_mode_dict
        self.config = defaultConfig
        return

    def reset_label_config_dict(self):
        self.label_config_dict = self.label_config_dict.fromkeys(
            self.label_config_dict, 0)

    def createGrids(self, chipstack, label_config_dict):
        self.I = np.zeros((int(chipstack.num_ptrace_lines), int(
            self.grid_dict['rows']), int(self.grid_dict['cols'])))
        self.length = round(chipstack.length, 20)
        self.width = round(chipstack.width, 20)
        self.initTemp = chipstack.initTemp
        if (self.grid_dict['type'] == 'Uniform') and (self.grid_dict['granularity'] == 'Grid'):
            return self.createUniformGrids(chipstack, label_config_dict)
        return chipstack

    def createUniformGrids(self, chipStack, label_config_dict):
        rows = int(self.grid_dict['rows'])
        cols = int(self.grid_dict['cols'])
        print(f"chipstack length {chipStack.length}")
        print(f"chipstack width {chipStack.width}")
        # Zihao modify it to 20 decimal points
        grid_length = round(chipStack.length/cols, 40)
        self.grid_width = round(chipStack.width/rows, 40)
        self.grid_length = round(chipStack.length/cols, 40)
        grid_width = round(chipStack.width/rows, 40)
        print(rows, "x", cols, "; grid_length and width:", grid_length, grid_width)
        if (round(grid_length*cols, 20) != chipStack.length) or (round(grid_width*rows, 20) != chipStack.width):
            print("grid_length*cols:", grid_length*cols, "chipStacl.length:", chipStack.length,
                  "grid_width*rows:", grid_width*rows, "chipStack.width:", chipStack.width)
            print(
                "Unifrom grids cannot be formed. Choose a multiple of 2 or 5 as rows and columns")
        layers = chipStack.Layers_data
        a = [chipStack.Layers_data.loc[i].flp_df['X'] for i in layers.index]
        chipStack.Layers_data = chipStack.Layers_data.apply(
            self.calculate_boundary_grids, args=(grid_length, grid_width, chipStack.num_layers))
        return chipStack

    def disp(self, x, a, b):
        print(a, b, type(x))
        print("1")
        print(x.flp_df['X'])
        print("2")
        return

    # Calculate boundary grids
    def calculate_boundary_grids(self, layer_obj, grid_length, grid_width, num_layers):
        thickness = layer_obj.thickness
        rows = int(self.grid_dict['rows'])
        cols = int(self.grid_dict['cols'])
        self.Rx = np.zeros(self.Rx.shape)
        self.Ry = np.zeros(self.Ry.shape)
        self.Rz = np.zeros(self.Rz.shape)
        self.C = np.zeros(self.C.shape)
        self.I = np.zeros(self.I.shape)
        self.Lock = np.zeros(self.Lock.shape)
        self.g2bmap = np.empty(self.g2bmap.shape, dtype="<U10")
        flp_df = layer_obj.flp_df
        chip_length = (flp_df['Length (m)']+flp_df['X']).max()
        chip_width = (flp_df['Width (m)']+flp_df['Y']).max()
        label_ll = flp_df['Label'].unique()
        self.Conv = np.zeros(self.Conv.shape)
        self.power_densities = 0
        if(layer_obj.layer_num < num_layers-1) and ("HeatSink" not in label_ll):
            ####FIND BOUNDARIES###
            X_vals = np.round(flp_df['X'].values, 20)
            Y_vals = np.round(flp_df['Y'].values, 20)
            length_vals = np.round(flp_df['Length (m)'].values, 20)
            height_vals = np.round(flp_df['Width (m)'].values, 20)
            label_vals = flp_df['Label'].values
            pd_vector_shape = (length_vals * height_vals).shape[0]
            PowerDensities = flp_df['Power'].values / \
                (length_vals * height_vals)
            ptrace_df = flp_df.filter(regex='^Power', axis=1)
            ptrace_mat = ptrace_df.values
            layer_obj.add_power_densities(
                ptrace_mat / (length_vals * height_vals).reshape((pd_vector_shape, 1)))
            self.power_densities = layer_obj.power_densities

            flp_df['grid_left_x'] = flp_df.apply(
                lambda x: round_to_grid_X(x.X, grid_length), axis=1)
            flp_df['grid_bottom_y'] = flp_df.apply(lambda x: int(
                self.grid_dict['rows']) - round_to_grid_Y(x.Y, grid_width) - 1, axis=1)
            temp_x = flp_df.apply(lambda x: (round(
                float(x.X), 20)+round(float(x['Length (m)']), 20))/grid_length, axis=1).round(40)
            temp_y = flp_df.apply(lambda x: (round(
                float(x.Y), 20)+round(float(x['Width (m)']), 20))/grid_width, axis=1).round(40)
            for label, item in temp_x.items():
                if abs(math.floor(item)-item) < 0.001:
                    temp_x[label] = math.floor(item)
                elif abs(math.ceil(item)-item) < 0.001:
                    temp_x[label] = math.ceil(item)
            for label, item in temp_y.items():
                if abs(math.floor(item)-item) < 0.001:
                    temp_y[label] = math.floor(item)
                elif abs(math.ceil(item)-item) < 0.001:
                    temp_y[label] = math.ceil(item)
            flp_df['grid_right_x'] = temp_x.apply(lambda x: math.floor(
                x) if math.ceil(x) != math.floor(x) else math.ceil(x) - 1)
            flp_df['grid_top_y'] = temp_y.apply(lambda x: int(self.grid_dict['rows']) - math.ceil(
                x) if math.ceil(x) != math.floor(x) else int(self.grid_dict['rows']) - math.floor(x))

            left_x_vals = np.round(flp_df['grid_left_x'].values, 40)
            right_x_vals = np.round(flp_df['grid_right_x'].values, 40)
            top_y_vals = np.round(flp_df['grid_top_y'].values, 40)
            bottom_y_vals = np.round(flp_df['grid_bottom_y'].values, 40)
            label_config_arr = list(
                zip(label_vals, flp_df['ConfigFile'].values))
            block_counter = np.arange(left_x_vals.size)
            for (label, cfile) in self.label_config_dict.keys():
                if(label in label_ll and self.label_mode_dict[label] == 'single'):
                    if(label == 'Si'):
                        self.label_config_dict[(label, cfile)] = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['Si'])
                    elif(label == 'MicroWick'):
                        self.label_config_dict[(label, cfile)] = LibMicroWick.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['MicroWick'])
                    elif(label == 'Cu'):
                        self.label_config_dict[(label, cfile)] = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['Cu'])
                    # Add these labels for Mono3D simulation
                    elif(label == 'Diel'):
                        self.label_config_dict[(label, cfile)] = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['Diel'])
                    elif(label == 'Metal'):
                        self.label_config_dict[(label, cfile)] = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['Metal'])
                    elif(label == 'Metal7_8'):
                        self.label_config_dict[(label, cfile)] = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['Metal7_8'])
                    elif(label == 'bcb'):
                        self.label_config_dict[(label, cfile)] = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['bcb'])
                    elif(label == 'lump0'):
                        self.label_config_dict[(label, cfile)] = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['lump0'])
                    elif(label == 'lump1'):
                        self.label_config_dict[(label, cfile)] = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['lump1'])
                    elif(label == 'Liq'):
                        self.label_config_dict[(label, cfile)] = LibLiquid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['Liq'])
                    elif(label == 'NoPackage'):
                        self.label_config_dict[(label, cfile)] = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['NoPackage'])
                    elif(label == 'HeatSink'):
                        self.label_config_dict[(label, cfile)] = LibHeatSink.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['HeatSink'], chip_length, chip_width)

                    for key in self.label_config_dict[(label, cfile)].keys():
                        if key.endswith("_constant"):
                            layer_obj.update_others_constants(
                                key, self.label_config_dict[(label, cfile)][key])
                # Matrix mode
                elif(label in label_ll and self.label_mode_dict[label] == 'matrix'):
                    if(label == 'HybridWick'):
                        if (type(self.initTemp) == float):
                            grid_temperatures = np.full(
                                (rows, cols), float(self.initTemp))
                        properties = self.config._sections['HybridWick']
                        properties.update(
                            [("grid_temperatures", grid_temperatures)])
                        self.label_config_dict[(label, cfile)] = LibHybridWick.defineGridPropertiesMatrix(
                            label, grid_length, grid_width, thickness, properties)
                    if(label == 'Si'):
                        properties = self.config._sections['Si']
                        properties.update([("grid_rows", rows)])
                        properties.update([("grid_cols", cols)])
                        self.label_config_dict[(label, cfile)] = LibSi.defineGridPropertiesMatrix(
                            grid_length, grid_width, thickness, properties)

                    self.Rx += self.label_config_dict[(label, cfile)]['Rx']
                    self.Ry += self.label_config_dict[(label, cfile)]['Ry']
                    self.Rz += self.label_config_dict[(label, cfile)]['Rz']
                    self.C += self.label_config_dict[(label, cfile)
                                                     ]['Capacitance']
                    self.I += self.label_config_dict[(label, cfile)]['I']
                    self.Conv += self.label_config_dict[(label,cfile)]['Conv']
                    break

            # Vectorize thermal RC matrixs
            self.vector_evaluateRC(X_vals, Y_vals, length_vals, height_vals, PowerDensities, left_x_vals, right_x_vals, bottom_y_vals,
                                   top_y_vals, label_vals, flp_df['ConfigFile'].values, block_counter, grid_length, grid_width, layer_obj.layer_num)

            if(str(layer_obj.LateralHeatFlow) == 'True'):
                layer_obj.Rx = self.Rx
                layer_obj.Ry = self.Ry
            else:
                layer_obj.Rx = np.ones(self.Rx.shape) * math.inf
                layer_obj.Ry = np.ones(self.Rx.shape) * math.inf

            layer_obj.Rz = self.Rz
            layer_obj.C = self.C
            layer_obj.Conv = self.Conv
            layer_obj.I = self.I
            layer_obj.Lock = self.Lock
            layer_obj.g2bmap = self.g2bmap
            # Nopackge layer
            if(layer_obj.layer_num == num_layers-2) and ("NoPackage" in self.config):
                self.noPackage_grid_left_x = flp_df['grid_left_x']
                self.noPackage_grid_right_x = flp_df['grid_right_x']
                self.noPackage_grid_bottom_y = flp_df['grid_bottom_y']
                self.noPackage_grid_top_y = flp_df['grid_top_y']
                self.noPackage_Lock = self.Lock
            # Heat sink and Heat spreader layers
            if(layer_obj.layer_num == num_layers-3) and ("HeatSink" in self.config):
                self.HeatSink_grid_left_x = flp_df['grid_left_x']
                self.HeatSink_grid_right_x = flp_df['grid_right_x']
                self.HeatSink_grid_bottom_y = flp_df['grid_bottom_y']
                self.HeatSink_grid_top_y = flp_df['grid_top_y']
                self.HeatSink_Lock = self.Lock

        elif "NoPackage" in self.config:
            flp_df['grid_left_x'] = self.noPackage_grid_left_x
            flp_df['grid_right_x'] = self.noPackage_grid_right_x
            flp_df['grid_bottom_y'] = self.noPackage_grid_bottom_y
            flp_df['grid_top_y'] = self.noPackage_grid_top_y
            if(layer_obj.LateralHeatFlow or layer_obj.VerticalHeatFlow):
                for (label, cfile) in self.label_config_dict.keys():
                    if(label == 'NoPackage'):
                        NoPackage_info = LibSolid.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['NoPackage'])
                        break

            if (str(layer_obj.LateralHeatFlow) == 'True'):
                layer_obj.Rx = np.ones(self.Rx.shape) * NoPackage_info['Rx']
                layer_obj.Ry = np.ones(self.Ry.shape) * NoPackage_info['Ry']
                layer_obj.C = np.ones(self.C.shape) * \
                    NoPackage_info['Capacitance']
            else:
                layer_obj.Rx = np.ones(self.Rx.shape) * math.inf
                layer_obj.Ry = np.ones(self.Ry.shape) * math.inf
                layer_obj.C = np.ones(self.C.shape) * \
                    NoPackage_info['Capacitance']
            layer_obj.Conv = np.ones(self.Conv.shape) * NoPackage_info['Conv']

            if (str(layer_obj.VerticalHeatFlow) == 'True'):
                r_amb = 1/(float(self.config.get('NoPackage', 'htc'))
                           * grid_length*grid_width) + NoPackage_info['Rz']
            else:
                r_amb = 1/(float(self.config.get('NoPackage', 'htc'))
                           * grid_length*grid_width)

            layer_obj.Rz = np.full(
                (int(self.grid_dict['rows']), int(self.grid_dict['cols'])), r_amb)
            val, unit = self.config.get('Init', 'ambient').split()
            if (unit == 'K' or unit == 'Kelvin'):
                val = round(float(val), 6)
            elif (unit == 'C' or 'Celsius'):
                val = round(float(val), 6) + 273.15
            P_noPackage = val/r_amb
            layer_obj.I = np.full((self.I.shape), P_noPackage)
            layer_obj.Lock = self.noPackage_Lock
            layer_obj.g2bmap = np.full((rows, cols), "NoPackage")
            layer_obj.flp_df = flp_df
            layer_obj.r_amb = r_amb

        else:
            flp_df['grid_left_x'] = self.HeatSink_grid_left_x
            flp_df['grid_right_x'] = self.HeatSink_grid_right_x
            flp_df['grid_bottom_y'] = self.HeatSink_grid_bottom_y
            flp_df['grid_top_y'] = self.HeatSink_grid_top_y
            if(layer_obj.LateralHeatFlow or layer_obj.VerticalHeatFlow):
                for (label, cfile) in self.label_config_dict.keys():
                    if(label == 'HeatSink'):
                        HeatSink_info = LibHeatSink.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['HeatSink'], chip_length, chip_width)
                        HeatSpreader_info = LibHeatSpreader.defineGridProperties(
                            grid_length, grid_width, thickness, self.config._sections['HeatSink'], chip_length, chip_width)
                        break
            for key in HeatSink_info.keys():
                if key.endswith("_constant"):
                    layer_obj.update_others_constants(key, HeatSink_info[key])
            for key in HeatSpreader_info.keys():
                if key.endswith("_constant"):
                    layer_obj.update_others_constants(
                        key, HeatSpreader_info[key])
            if (str(layer_obj.LateralHeatFlow) == 'True'):
                if(layer_obj.layer_num == num_layers-1):
                    layer_obj.Rx = np.ones(self.Rx.shape) * HeatSink_info['Rx']
                    layer_obj.Ry = np.ones(self.Ry.shape) * HeatSink_info['Ry']
                    layer_obj.C = np.ones(self.C.shape) * \
                        HeatSink_info['Capacitance']
                if(layer_obj.layer_num == num_layers-2):
                    layer_obj.Rx = np.ones(
                        self.Rx.shape) * HeatSpreader_info['Rx']
                    layer_obj.Ry = np.ones(
                        self.Ry.shape) * HeatSpreader_info['Ry']
                    layer_obj.C = np.ones(self.C.shape) * \
                        HeatSpreader_info['Capacitance']
            else:
                if(layer_obj.layer_num == num_layers-1):
                    layer_obj.Rx = np.ones(self.Rx.shape) * math.inf
                    layer_obj.Ry = np.ones(self.Ry.shape) * math.inf
                    layer_obj.C = np.ones(self.C.shape) * \
                        HeatSink_info['Capacitance']
                if(layer_obj.layer_num == num_layers-2):
                    layer_obj.Rx = np.ones(self.Rx.shape) * math.inf
                    layer_obj.Ry = np.ones(self.Ry.shape) * math.inf
                    layer_obj.C = np.ones(self.C.shape) * \
                        HeatSpreader_info['Capacitance']
            layer_obj.Conv = np.ones(self.Conv.shape) * HeatSink_info['Conv']

            r_amb = 1/(1e5*grid_length*grid_width) + HeatSink_info['Rz']
            layer_obj.Rz = np.full(
                (int(self.grid_dict['rows']), int(self.grid_dict['cols'])), r_amb)
            if(layer_obj.layer_num == num_layers-2):
                layer_obj.Rz = np.ones(self.Rz.shape) * HeatSpreader_info['Rz']

            val, unit = self.config.get('Init', 'ambient').split()
            if (unit == 'K' or unit == 'Kelvin'):
                val = round(float(val), 6)
            elif (unit == 'C' or 'Celsius'):
                val = round(float(val), 6) + 273.15
            P_HeatSink = val/r_amb
            layer_obj.r_amb = r_amb
            layer_obj.I = np.full((self.I.shape), P_HeatSink)
            layer_obj.Lock = self.HeatSink_Lock
            layer_obj.g2bmap = np.full((rows, cols), "HeatSink")
            layer_obj.flp_df = flp_df

        return layer_obj

    def evaluateRC(self, X, Y, length, width, PowerDensity, leftX, rightX, bottomY, topY, label, config, block_idx, grid_length, grid_width, layer_num):
        if(self.label_mode_dict[label] == 'matrix' and PowerDensity == 0):
            self.Lock[topY:bottomY+1, leftX:rightX+1] += 1
            return

        area = grid_length * grid_width
        power = PowerDensity * area
        power_mat = self.power_densities[block_idx] * area

        power_mat_reshape = np.reshape(
            power_mat, (len(power_mat), 1, 1), order='C')
        mode = self.label_mode_dict[label]
        length_lb_o = round((leftX+1)*grid_length - X, 40)
        length_rb_o = round((X+length) - (rightX)*grid_length, 40)
        length_lt_o = length_lb_o
        length_rt_o = length_rb_o
        width_lb_o = round(
            (int(self.grid_dict['rows']) - bottomY)*grid_width - Y, 40)
        width_rb_o = width_lb_o
        width_lt_o = round((topY + 1) * grid_width -
                           (self.width - Y - width), 40)
        width_rt_o = width_lt_o
        # No overlap
        if((length_lb_o == length_rb_o == grid_length) and (width_lb_o == width_lt_o == grid_width)):
            self.I[:, topY:bottomY+1, leftX:rightX+1] += power_mat_reshape
            self.Lock[topY:bottomY+1, leftX:rightX+1] += 1
            self.g2bmap[topY:bottomY+1, leftX:rightX+1] = label
            if (mode == 'single'):
                self.Rx[topY:bottomY+1, leftX:rightX +
                        1] = self.label_config_dict[(label, config)]['Rx']
                self.Ry[topY:bottomY+1, leftX:rightX +
                        1] = self.label_config_dict[(label, config)]['Ry']
                self.Rz[topY:bottomY+1, leftX:rightX +
                        1] = self.label_config_dict[(label, config)]['Rz']
                self.C[topY:bottomY+1, leftX:rightX +
                       1] = self.label_config_dict[(label, config)]['Capacitance']
                self.Conv[topY:bottomY+1, leftX:rightX +
                          1] = self.label_config_dict[(label, config)]['Conv']

            return
        # Overlap
        else:
            lb_o = np.round(length_lb_o * width_lb_o / (area), 40)
            rb_o = np.round(length_rb_o * width_rb_o / (area), 40)
            lt_o = np.round(length_lt_o * width_lt_o / (area), 40)
            rt_o = np.round(length_rt_o * width_rt_o / (area), 40)
            left_edge_cells_o = round(length_lb_o / grid_length, 40)
            right_edge_cells_o = round(length_rb_o / grid_length, 40)
            top_edge_cells_o = round(width_lt_o / grid_width, 40)
            bottom_edge_cells_o = round(width_lb_o / grid_width, 40)
            edge_cells_o = {'lb_o': lb_o, 'rb_o': rb_o, 'lt_o': lt_o, 'rt_o': rt_o, 'left_edge_cells_o': left_edge_cells_o,
                            'right_edge_cells_o': right_edge_cells_o, 'top_edge_cells_o': top_edge_cells_o, 'bottom_edge_cells_o': bottom_edge_cells_o}

            mask = np.ones((bottomY - topY + 1, rightX - leftX + 1))
            mask[:, 0] = left_edge_cells_o
            mask[:, -1] = right_edge_cells_o
            mask[0, :] = top_edge_cells_o
            mask[-1, :] = bottom_edge_cells_o
            mask[0, 0] = lt_o
            mask[0, -1] = rt_o
            mask[-1, -1] = rb_o
            mask[-1, 0] = lb_o
            conditions = [mask >= 0.9]
            choice = [label]
            self.g2bmap[topY:bottomY+1, leftX:rightX +
                        1] = np.select(conditions, choice)

            mask_I = np.ones(
                (self.I.shape[0], bottomY - topY + 1, rightX - leftX + 1))
            mask_I[:, :, 0] = left_edge_cells_o
            mask_I[:, :, -1] = right_edge_cells_o
            mask_I[:, 0, :] = top_edge_cells_o
            mask_I[:, -1, :] = bottom_edge_cells_o
            mask_I[:, 0, 0] = lt_o
            mask_I[:, 0, -1] = rt_o
            mask_I[:, -1, -1] = rb_o
            mask_I[:, -1, 0] = lb_o

            np.set_printoptions(threshold=np.inf)
            mask_I = mask_I * power_mat_reshape
            placeholder_mat = np.zeros_like(self.I)
            placeholder_mat[:, topY:bottomY+1, leftX:rightX+1] = mask_I

            self.I += placeholder_mat
            self.Lock[topY:bottomY+1, leftX:rightX+1] += mask

            if(self.label_mode_dict[label] == 'single'):
                a = self.Rx[topY:bottomY+1, leftX:rightX+1]
                a = np.reciprocal(a, where=a != 0, out=np.zeros_like(a))
                self.Rx[topY:bottomY+1, leftX:rightX+1] = np.reciprocal(
                    a + mask * (1/self.label_config_dict[(label, config)]['Rx']))

                a = self.Ry[topY:bottomY+1, leftX:rightX+1]
                a = np.reciprocal(a, where=a != 0, out=np.zeros_like(a))
                self.Ry[topY:bottomY+1, leftX:rightX+1] = np.reciprocal(
                    a + mask * (1/self.label_config_dict[(label, config)]['Ry']))

                a = self.Rz[topY:bottomY+1, leftX:rightX+1]
                a = np.reciprocal(a, where=a != 0, out=np.zeros_like(a))
                self.Rz[topY:bottomY+1, leftX:rightX+1] = np.reciprocal(
                    a + mask * (1/self.label_config_dict[(label, config)]['Rz']))
                self.C[topY:bottomY+1, leftX:rightX+1] += mask * \
                    self.label_config_dict[(label, config)]['Capacitance']

                self.Conv[topY:bottomY+1, leftX:rightX+1] += mask * \
                    self.label_config_dict[(label, config)]['Conv']
            return
        return

    def addLibraries(self, lib_dict):
        self.lib_dict = lib_dict
        return
    # Map grid temperatures to block temperatures

    def grid2block(self, chipStack, gridTemperatures, block_mode, transient=False, transientFile=None):
        chipStack.Layers_data.apply(self.calculate_block_temperatures,
                                    args=(gridTemperatures, block_mode, transient, transientFile))
        return

    def calculate_block_temperatures(self, layer_obj, gridTemperatures, block_mode, transient, transientFile):
        layer_num = layer_obj.layer_num
        flp = layer_obj.flp_df
        if(block_mode == 'max'):
            layer_obj.flp_df['BlockTemperature'] = flp.apply(lambda x: round(np.max((gridTemperatures[layer_num])
                                                                                    [int(x.grid_top_y):int(x.grid_bottom_y)+1, int(x.grid_left_x):int(x.grid_right_x)+1]) - 273.15, 3), axis=1)
        elif(block_mode == 'min'):
            layer_obj.flp_df['BlockTemperature'] = flp.apply(lambda x: round(np.min((gridTemperatures[layer_num])
                                                                                    [int(x.grid_top_y):int(x.grid_bottom_y)+1, int(x.grid_left_x):int(x.grid_right_x)+1]) - 273.15, 3), axis=1)
        elif(block_mode == 'avg'):
            layer_obj.flp_df['BlockTemperature'] = flp.apply(lambda x: round(np.mean((gridTemperatures[layer_num])
                                                                                     [int(x.grid_top_y):int(x.grid_bottom_y)+1, int(x.grid_left_x):int(x.grid_right_x)+1]) - 273.15, 3), axis=1)
        if transient == False:
            print(f'layer number:{layer_num}')
            print(layer_obj.flp_df[['UnitName', 'BlockTemperature']])
        else:
            with(open(transientFile, "a")) as myfile:
                myfile.write(f'layer number:{layer_num}')
                pd.options.display.max_rows = 600
                myfile.write(
                    str(layer_obj.flp_df[['UnitName', 'BlockTemperature']])+'\n')
        return
