# This file creates a function that is called by "main_generation.py" to perform nonlinear model generation

# Modified by: Stevan Gavrilovic @ SimCenter, UC Berkeley
# Last revision: 09/2020

import os
import pickle

from nonlinear_analysis import NonlinearAnalysis


def model_generation(base_directory, pathDataFolder, workingDirectory):
    ##########################################################################
    #                       Load Building Design Result                      #
    ##########################################################################

    # Change the directory to the folder where the design results are stored
    os.chdir(workingDirectory + '/BuildingDesignResults/')
    # Load all design results (stored as .pkl files)
    with open('construction_building.pkl', 'rb') as file:
        building = pickle.load(file)
    with open('construction_column_set.pkl', 'rb') as file:
        column_set = pickle.load(file)
    with open('construction_beam_set.pkl', 'rb') as file:
        beam_set = pickle.load(file)
    with open('construction_connection_set.pkl', 'rb') as file:
        connection_set = pickle.load(file)

    ##########################################################################
    #                 Update the Building Directory                          #
    ##########################################################################

    # Update the directory because Seismic Design might be run on some other PCs
    # As a result, the directory stored in construction_building.pkl might not work
    # in this PC
    # Define path to folder where the baseline .tcl files for elastic analysis are saved
    building.directory['baseline files elastic'] = (
        base_directory + '/BaselineTclFiles/ElasticAnalysis'
    )
    # Define path to folder where the baseline .tcl files for nonlinear analysis are stored
    building.directory['baseline files nonlinear'] = (
        base_directory + '/BaselineTclFiles/NonlinearAnalysis'
    )
    # Define path to folder where the building data (.csv) are saved
    building.directory['building data'] = pathDataFolder
    # Define path to folder where the generated elastic analysis OpenSees model is saved
    building.directory['building elastic model'] = (
        workingDirectory + '/BuildingElasticModels'
    )
    # Define path to folder where the generated nonlinear analysis OpenSees model is saved
    building.directory['building nonlinear model'] = (
        workingDirectory + '/BuildingNonlinearModels'
    )

    ##########################################################################
    #                 Generate Nonlinear Analysis Model                      #
    ##########################################################################

    analysis_list = ['EigenValueAnalysis', 'PushoverAnalysis', 'DynamicAnalysis']
    for analysis_type in analysis_list:
        model = NonlinearAnalysis(
            building, column_set, beam_set, connection_set, analysis_type
        )
