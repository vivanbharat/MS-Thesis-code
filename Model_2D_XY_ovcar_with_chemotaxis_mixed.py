from cc3d import CompuCellSetup

from Model_2D_XY_ovcar_with_chemotaxis_mixedSteppables import Model_2D_2cell_with_ExpotenSteppable
CompuCellSetup.register_steppable(steppable=Model_2D_2cell_with_ExpotenSteppable(frequency=1))

from Model_2D_XY_ovcar_with_chemotaxis_mixedSteppables import CellMotilitySteppable
CompuCellSetup.register_steppable(steppable=CellMotilitySteppable(frequency=50))
        
from Model_2D_XY_ovcar_with_chemotaxis_mixedSteppables import GrowthandMitosisSteppable
CompuCellSetup.register_steppable(steppable=GrowthandMitosisSteppable(frequency=1))
       
from Model_2D_XY_ovcar_with_chemotaxis_mixedSteppables import PlottingSteppable
CompuCellSetup.register_steppable(steppable=PlottingSteppable(frequency=250))
                
# from Model_2D_XY_ovcar_with_chemotaxis_mixedSteppables import Secretion_and_uptakeSteppable
# CompuCellSetup.register_steppable(steppable=Secretion_and_uptakeSteppable(frequency=1))

CompuCellSetup.run()
