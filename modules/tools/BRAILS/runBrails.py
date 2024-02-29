# Import packages needed for setting up required packages:
import sys
import subprocess
from importlib import metadata as importlib_metadata

# If not installed, install BRAILS, argparse, and requests:
required = {'BRAILS', 'argparse', 'requests'}
installed = set()

# Detect installed packages using Python-provided importlib.metadata:
for x in importlib_metadata.distributions():
    try:
        installed.add(x.name)
    except:
        pass

# If installed packages could not be detected, use importlib_metadata backport:
if not installed:
    import importlib_metadata
    for x in importlib_metadata.distributions():
        try:
            installed.add(x.name)
        except:
            pass
missing = required - installed

# Install missing packages:
python = sys.executable
if missing:
    print('\nInstalling packages required for running this widget...')
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], 
                          stdout=subprocess.DEVNULL)
    print('Successfully installed the required packages')

# If requests and BRAILS were previously installed ensure they are at their latest versions:
subprocess.check_call([python, '-m', 'pip', 'install', 'requests','-U'],
                      stdout=subprocess.DEVNULL)
 
import requests
latestBrailsVersion = requests.get('https://pypi.org/pypi/BRAILS/json').json()['info']['version']
if  importlib_metadata.version('BRAILS')!=latestBrailsVersion:
    print('\nAn older version of BRAILS was detected. Updating to the latest BRAILS version..')    
    subprocess.check_call([python, '-m', 'pip', 'install', 'BRAILS','-U'],
                          stdout=subprocess.DEVNULL)
    print('Successfully installed the latest version of BRAILS')   
 
# Import packages required for running the latest version of BRAILS:
import argparse
import os
from time import gmtime, strftime
from brails.InventoryGenerator import InventoryGenerator    

# Define a standard way of printing program outputs:
def log_msg(msg):
    formatted_msg = '{} {}'.format(strftime('%Y-%m-%dT%H:%M:%SZ', gmtime()), msg)
    print(formatted_msg)

# Define a way to call BRAILS InventoryGenerator:
def runBrails(latMin, latMax, longMin, longMax, locationStr, fpSource,
              fpAttrMap, seed, numBuildings, gKey, outputFile, lengthUnit):    
    
    # Initialize InventoryGenerator:
    if locationStr=="":
        invGenerator = InventoryGenerator(location=(longMin,latMin,longMax,latMax),
                                          nbldgs=numBuildings, randomSelection=seed,
                                          GoogleAPIKey=gKey)
    else:
        invGenerator = InventoryGenerator(location=locationStr,
                                          nbldgs=numBuildings, randomSelection=seed,
                                          GoogleAPIKey=gKey)
    

    # Run InventoryGenerator to generate an inventory for the entered location:
    invGenerator.generate(attributes='all', outFile=outputFile, 
                          lengthUnit=lengthUnit)

# Define a way to collect GUI input:
def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--latMin', default=None, type=float)
    parser.add_argument('--latMax', default=None, type=float)
    parser.add_argument('--longMin', default=None, type=float)
    parser.add_argument('--longMax', default=None, type=float)
    parser.add_argument('--location', default=None, type=str)
    parser.add_argument('--fpSource', default=None, type=str)
    parser.add_argument('--fpAttrMap', default=None, type=str)
    parser.add_argument('--outputFile', default=None)
    parser.add_argument('--googKey', default=None)
    parser.add_argument('--seed', default=None, type=int)
    parser.add_argument('--numBuildings', default=None, type=int)  
    parser.add_argument('--lengthUnit', default="m", type=str) 

    args = parser.parse_args(args)

    # Create the folder for the user-defined output directory, if it does not exist:
    outdir = os.path.abspath(args.outputFile).replace(os.path.split(args.outputFile)[-1],'')
    os.makedirs(outdir, exist_ok=True)

    # Run BRAILS BRAILS InventoryGenerator with the user-defined arguments:
    runBrails(
        args.latMin, args.latMax, args.longMin, args.longMax, args.location,
        args.fpSource, args.fpAttrMap, args.seed, args.numBuildings, args.googKey, 
        args.outputFile, args.lengthUnit)

    log_msg('BRAILS successfully generated the requested building inventory')
    
# Run main:
if __name__ == '__main__':
    main(sys.argv[1:])