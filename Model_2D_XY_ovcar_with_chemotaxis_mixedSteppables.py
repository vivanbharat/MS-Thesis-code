
from cc3d.core.PySteppables import *
import numpy as np
import random as rng

global Avol_NON_SEN, Avol_SEN, Ap_NON_SEN



class Model_2D_2cell_with_ExpotenSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """   
        
        # Define variables to be shared by all Steppables
        self.shared_steppable_vars["Avol_NON_SEN"] = 0
        self.shared_steppable_vars["Avol_SEN"] = 0
        self.shared_steppable_vars["Ap_NON_SEN"] = 0
        self.shared_steppable_vars["Average_cancer_neighbours"] = 0
        self.shared_steppable_vars["NON_SEN area"] = 0
        self.shared_steppable_vars["SEN area"] = 0
        self.shared_steppable_vars["Cancer cell area"] = 0
        
        self.build_wall(self.WALL)
  
        dimen = self.dim.x
        
        counter = 0
        num_cancer = 8
        factor = 0
        
        for i in range(int(dimen/20)):
            for j in range(int(dimen/20)):
                
                if (i+j)%2 == 0:
                    x = 3 + 20*i
                    y = 3 + 20*j
                    size = 14
                    cell = self.new_cell(self.SEN)
                    self.cell_field[x:x + size - 1, y:y + size - 1, 0] = cell
                    
                else:
                    x = 7 + 20*i
                    y = 7 + 20*j
                    
                    size = 7
                    
                    switch = num_cancer #rng.randint(0,1)
                    if (24 % switch == 0 and factor % (24/switch) == 0):
                        counter +=1
                        if (counter< num_cancer + 1):
                            cell = self.new_cell(self.CANCER)
                            self.cell_field[x:x + size - 1, y:y + size - 1, 0] = cell
                            
                        else:
                            cell = self.new_cell(self.NON_SEN)
                            self.cell_field[x:x + size - 1, y:y + size - 1, 0] = cell
                        
                    else:
                        cell = self.new_cell(self.NON_SEN)
                        self.cell_field[x:x + size - 1, y:y + size - 1, 0] = cell
                    
                    factor += 1
                
                
        # cell1 = self.new_cell(self.SEN)
        # self.cell_field[40:54, 40:54, 0] = cell1  
        
        # cell2 = self.new_cell(self.NON_SEN)
        # self.cell_field[20:27, 30:37, 0] = cell2     
        
        for cell in self.cell_list_by_type(self.NON_SEN):
            cell.targetVolume = rng.randint(40, 58)
            cell.lambdaVolume = rng.randint(18, 22)
            
            
        for cell in self.cell_list_by_type(self.SEN):
            cell.targetVolume = rng.randint(176, 216)
            cell.lambdaVolume = rng.randint(18, 22)
            # cell.lambdaVolume = rng.uniform(1.5, 2.0)
            # cell.targetSurface = int(((2*(cell.volume))**0.5)*3.14)
            # cell.lambdaSurface = rng.uniform(1.5, 2.0)
            
        for cell in self.cell_list_by_type(self.CANCER):    
            cell.targetVolume = rng.randint(62, 86)
            cell.lambdaVolume = rng.randint(18, 22)
            # cell.lambdaVolume = rng.randint(28, 32) 
        
        
    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        
        self.set_max_mcs(8100)
        
        #cancer_intro = 2000
        sort_time = 0
        div_time = 0
        
        
        #num_can = 10
          
        #AV_SEN_VOL = 0
        #AV_NON_SEN_VOL = 0
        #Av_pressure_non_sen = 0
        #Av_pressure_cancer = 0
        
        L_NON_SEN = len(self.cell_list_by_type(self.NON_SEN))
        L_SEN = len(self.cell_list_by_type(self.SEN))
        L_CANCER = len(self.cell_list_by_type(self.CANCER))
        
        Avol_NON_SEN = 0
        Avol_SEN = 0
        Avol_CANCER = 0
        Ap_NON_SEN = 0
        Ap_CANCER = 0
        
        
        Average_cancer_neighbours = 0
        NON_SEN_area = 0
        SEN_area = 0
        Cancer_cell_area = 0
        
        # random death of all cells with a fixed probability       
        for cell in self.cell_list:
            death_number = rng.randint(1,30000)
            if death_number == 5:             
                   cell.targetVolume = 0
                   cell.lambdaVolume = 10000
        
        
        
        # for cell in self.cell_list_by_type(self.NON_SEN):
            # Av_pressure_non_sen += cell.pressure
        
        # if L_NON_SEN != 0:
            # Av_pressure_non_sen = Av_pressure_non_sen/L_NON_SEN
        # print("Pressure NON_SEN", Av_pressure_non_sen)
        
        # if (mcs > cancer_intro):
            # for cell in self.cell_list_by_type(self.CANCER):
                # Av_pressure_cancer += cell.pressure
        # if L_CANCER != 0:    
            # Av_pressure_cancer = Av_pressure_cancer/L_CANCER
        # print("Pressure CANCER", Av_pressure_cancer)
        
        
        # if (mcs == cancer_intro):
            # for i in range(0, num_can):
                # cell = self.cell_field[rng.randint(5, self.dim.x-5), rng.randint(5, self.dim.y-5), 0]
                # if cell.type != self.SEN:
                    # cell.type = self.CANCER
                    # cell.targetVolume = rng.randint(70, 78)
                    # cell.lambdaVolume = rng.randint(28, 32) 
                    
            # for cell in self.cell_list_by_type(self.SEN):
                    # AV_SEN_VOL += cell.volume/L_SEN
                    
            # for cell in self.cell_list_by_type(self.NON_SEN):
                    # AV_NON_SEN_VOL += cell.volume/L_NON_SEN
        
        death_frac = 0.15
        common_area_frac = 0.55
        
        #if (mcs > cancer_intro):
        # for extrusion due to compression:
        # for cell in self.cell_list:
            # if cell.type == self.SEN:             
                # if cell.volume < death_frac*cell.targetVolume:
                   # cell.targetVolume = 0
                   # cell.lambdaVolume = 10000
               
            # elif cell.type == self.NON_SEN:
                # if cell.volume < death_frac*cell.targetVolume:
                    # cell.targetVolume = 0
                    # cell.lambdaVolume = 10000
           
            # elif cell.type == self.CANCER:
                # if cell.volume < death_frac*cell.targetVolume:
                    # cell.targetVolume = 0
                    # cell.lambdaVolume = 10000
                    
        
     
        # if  mcs == cancer_intro - 1:
            # secretor = self.get_field_secretor("CHEMOKINE")
            # self.shared_steppable_vars["total_amount"] = secretor.totalFieldIntegral()
        
        # secretor = self.get_field_secretor("CHEMOKINE")
        # amount = secretor.totalFieldIntegral()
        
        for cell in self.cell_list_by_type(self.NON_SEN):
            if L_NON_SEN != 0:
                Avol_NON_SEN += cell.volume/L_NON_SEN
                cell.dict['pressure'] = 2*cell.lambdaVolume*(cell.targetVolume - cell.volume)
                #Ap_NON_SEN += cell.dict['pressure']/L_NON_SEN
            if mcs > div_time:
                if cell.dict['pressure'] > 0:   #-(cell.pressure) > 0: #int(cell.dict['pressure']) > 0:
                    #print("inside positive pressure cond")
                    cell.targetVolume += rng.uniform(0.8, 1.2)*50/1000*(1 - ((cell.dict['pressure'])**8)/((cell.dict['pressure'])**8 + (75**8)))#25/500*max(0, p_ref_NON_SEN-cell.dict['pressure'])
                    
                
        if (mcs > sort_time and L_CANCER):
            for cell in self.cell_list_by_type(self.CANCER):    
                #Avol_CANCER += cell.volume/L_CANCER
                cell.dict['pressure'] = 2*cell.lambdaVolume*(cell.targetVolume - cell.volume)
                #Ap_CANCER += cell.dict['pressure']/L_CANCER
                if mcs > sort_time and cell.dict['pressure'] > 0:
                    cell.targetVolume += rng.uniform(0.8, 1.2)*75/1000*(1 - ((cell.dict['pressure'])**4)/((cell.dict['pressure'])**4 + (1500**4))) #25/200 *(amount/(self.shared_steppable_vars["total_amount"])) + 25/200*max(0, p_ref_CANCER - cell.dict['pressure'])
                    
        
        for cell in self.cell_list_by_type(self.SEN):
            Avol_SEN += cell.volume/L_SEN
            cancer_common_area = 0
            for neighbor, common_surface_area in self.get_cell_neighbor_data_list(cell):
                if neighbor and neighbor.type == self.CANCER:
                    cancer_common_area += common_surface_area
                    Average_cancer_neighbours += 1
            
            # Active clearance rule is impleted in the next three line
            # if cancer_common_area/cell.surface > common_area_frac:
                # cell.targetVolume = 0
                # cell.lambdaVolume = 10000
               
        
        for cell in self.cell_list_by_type(self.NON_SEN):
            NON_SEN_area += cell.volume
            
        for cell in self.cell_list_by_type(self.SEN):
            SEN_area += cell.volume
        
        for cell in self.cell_list_by_type(self.CANCER):               
            Cancer_cell_area += cell.volume    
            
        
                
        self.shared_steppable_vars["Avol_NON_SEN"] = Avol_NON_SEN    
        self.shared_steppable_vars["Avol_SEN"] = Avol_SEN
        self.shared_steppable_vars["Ap_NON_SEN"] = Ap_NON_SEN
        self.shared_steppable_vars["Average_cancer_neighbours"] = Average_cancer_neighbours
        self.shared_steppable_vars["Cancer cell area"] = Cancer_cell_area
        self.shared_steppable_vars["NON_SEN area"] = NON_SEN_area
        self.shared_steppable_vars["SEN area"] = SEN_area
        
        print("pressure using method", Ap_NON_SEN)

    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """

class CellMotilitySteppable(SteppableBasePy):
    
    def __init__(self, frequency=50):

        SteppableBasePy.__init__(self,frequency)
    
    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        
        for cell in self.cell_list:
            
            theta = rng.uniform(0, 2*np.pi)
            bias = np.array((np.cos(theta), np.sin(theta), 0)) # because dealing with numpy arrays is much more easier
            cell.dict['bias'] = bias
            cell.dict['angle'] = theta
            

            cell.lambdaVecX = -30 * cell.dict['bias'][0]  # force component pointing along X axis - towards positive X's
            cell.lambdaVecY = -30 * cell.dict['bias'][1]  # force component pointing along Y axis - towards negative Y's
            cell.lambdaVecZ = 0.0  # force component pointing along Z axis
            
            
    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        
        alpha = 0.5

        for cell in self.cell_list:
            # Make sure CenterOfMass plugin is loaded
            # READ ONLY ACCESS
            xCOM = cell.xCOM
            yCOM = cell.yCOM
            zCOM = cell.zCOM
            
            # access/modification of a dictionary attached to cell - make sure to declare in main script that
            # you will use such attribute
            cell.dict['velocity'] = np.array((cell.xCOM - cell.xCOMPrev, cell.yCOM - cell.yCOMPrev, 0))           
            v_norm = cell.dict['velocity'][:] / np.linalg.norm(cell.dict['velocity'])
            
            cell.dict['bias'][:] = alpha * cell.dict['bias'][:] + (1 - alpha) * v_norm[:]
            
            cell.lambdaVecX = -20 * cell.dict['bias'][0]  # force component pointing along X axis - towards positive X's
            cell.lambdaVecY = -20 * cell.dict['bias'][1]  # force component pointing along Y axis - towards negative Y's
            cell.lambdaVecZ = 0.0  # force component pointing along Z axis
    

class GrowthandMitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.NON_SEN):
            if cell.volume > rng.randint(78, 118):
                cells_to_divide.append(cell)
        
        for cell in self.cell_list_by_type(self.CANCER):
            if cell.volume > rng.randint(128, 168):
                cells_to_divide.append(cell)

        for cell in cells_to_divide:

            self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()            

        # # for more control of what gets copied from parent to child use cloneAttributes function
        # # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        # if self.parent_cell.type==1:
            # self.child_cell.type=2
        # else:
            # self.child_cell.type=1

        
class PlottingSteppable(SteppableBasePy):
    
    def __init__(self, frequency=250):
        SteppableBasePy.__init__(self, frequency)
        

    def start(self):
        
        # Implementing all the plots here 
        
        
        self.plot_cancer_neighbours = self.add_new_plot_window(title='Number of SEN-CANCER contacts',
                                                 x_axis_title='MonteCarlo Step (MCS)',
                                                 y_axis_title='Number of contacts', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        
        self.plot_cancer_neighbours.add_plot("Contacts", style='Lines', color='red', size=3)

        
        self.plot_coculture_area = self.add_new_plot_window(title='Monolayer and cancer cell area',
                                                 x_axis_title='MonteCarlo Step (MCS)',
                                                 y_axis_title='Area', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        
        self.plot_coculture_area.add_plot("Cancer cell area", style='Lines', color='green', size=3)
        self.plot_coculture_area.add_plot("SEN area", style='Lines', color='red', size=3)
        self.plot_coculture_area.add_plot("NON_SEN area", style='Lines', color='pink', size=3)        
        
      
      
        # self.plot_win = self.add_new_plot_window(title='Volume ratio SEN:NON_SEN',
                                                 # x_axis_title='MCS',
                                                 # y_axis_title='AvTGVol',
                                                 # x_scale_type='linear', 
                                                 # y_scale_type='linear',
                                                 # grid=False)
        
        # self.plot_win.add_plot("Avol", style='Dots', color='green', size=5)
        # self.plot_win.add_plot("Avol_SEN", style='Dots', color='red', size=5)
       
       
        # self.plot_win2 = self.add_new_plot_window(title='Average Pressure',
                                                 # x_axis_title='MCS',
                                                 # y_axis_title='Avp',
                                                 # x_scale_type='linear', 
                                                 # y_scale_type='linear',
                                                 # grid=False)
                                                 
                                                 
        # self.plot_win2.add_plot("Ap", style='Lines', color='cyan', size=5)
        
        self.plot_no_cells = self.add_new_plot_window(title='Number of cells',
                                                 x_axis_title='MCS',
                                                 y_axis_title='Cell numbers',
                                                 x_scale_type='linear', 
                                                 y_scale_type='linear',
                                                 grid=False)
                                                 
                                                 
        self.plot_no_cells.add_plot("Num_sen", style='Lines', color='red', size=4)
        self.plot_no_cells.add_plot("Num_nonsen", style='Lines', color='pink', size=4)
        self.plot_no_cells.add_plot("Num_cancer", style='Lines', color='green', size=4)
        
        # self.plot_no_nonsen = self.add_new_plot_window(title='Number of NonSen cells',
                                                 # x_axis_title='MCS',
                                                 # y_axis_title='Number',
                                                 # x_scale_type='linear', 
                                                 # y_scale_type='linear',
                                                 # grid=False)
                                                 
                                                 
        #self.plot_no_nonsen.add_plot("Num_nonsen", style='Lines', color='green', size=5)
        
        # self.plot_no_cancer = self.add_new_plot_window(title='Number of cancer cells',
                                                 # x_axis_title='MCS',
                                                 # y_axis_title='Number',
                                                 # x_scale_type='linear', 
                                                 # y_scale_type='linear',
                                                 # grid=False)
                                                 
                                                 
        # self.plot_no_cancer.add_plot("Num_cancer", style='Lines', color='cyan', size=5)
        

    def step(self, mcs):
        
        # Varibales from shared dictionary
        

        Average_cancer_neighbours = self.shared_steppable_vars["Average_cancer_neighbours"]
        Avol_NON_SEN = self.shared_steppable_vars["Avol_NON_SEN"]
        Avol_SEN = self.shared_steppable_vars["Avol_SEN"]
        Ap_NON_SEN = self.shared_steppable_vars["Ap_NON_SEN"]
        Cancer_cell_area = self.shared_steppable_vars["Cancer cell area"] 
        NON_SEN_area = self.shared_steppable_vars["NON_SEN area"] 
        SEN_area = self.shared_steppable_vars["SEN area"]
        
        
        # arguments are (name of the data series, x, y)
        #if mcs >= 500:
        self.plot_no_cells.add_data_point("Num_sen", mcs, len(self.cell_list_by_type(self.SEN)))
        self.plot_no_cells.add_data_point("Num_nonsen", mcs, len(self.cell_list_by_type(self.NON_SEN)))
        #if mcs >= 2000:
        self.plot_no_cells.add_data_point("Num_cancer", mcs, len(self.cell_list_by_type(self.CANCER)))
        
        self.plot_cancer_neighbours.add_data_point("Contacts", mcs, Average_cancer_neighbours)
        self.plot_coculture_area.add_data_point("Cancer cell area", mcs, Cancer_cell_area)
        self.plot_coculture_area.add_data_point("NON_SEN area", mcs, NON_SEN_area)
        self.plot_coculture_area.add_data_point("SEN area", mcs, SEN_area)
       
        
        #self.plot_win.add_data_point("Avol", mcs, Avol_NON_SEN)
        #self.plot_win2.add_data_point("Ap", mcs, Ap_NON_SEN)   
        #self.plot_win.add_data_point("Avol_SEN", mcs, Avol_SEN/Avol_NON_SEN)


    def finish(self):
        # this function may be called at the end of simulation - used very infrequently though
        return

    def on_stop(self):
        # this gets called each time user stops simulation
        return


        
        
class Secretion_and_uptakeSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        
    def step(self, mcs):
        
        secretor = self.get_field_secretor("CHEMOKINE")
        for cell in self.cell_list_by_type(self.SEN):
            secretor.secreteOutsideCellAtBoundary(cell, 0.1)
            # tot_amount = secretor.secreteOutsideCellAtBoundaryTotalCount(cell, 300).tot_amount
            
        # if len(self.cell_list_by_type(self.CANCER)):
            # for cell in self.cell_list_by_type(self.CANCER):
                # secretor.uptakeInsideCell(cell, 2.0, 0.00001)
                # tot_amount = secretor.uptakeInsideCellTotalCount(cell, 2.0, 0.2).tot_amount
            
        
        
        
    def finish(self):
        # this function may be called at the end of simulation - used very infrequently though
        return

    def on_stop(self):
        # this gets called each time user stops simulation
        return


