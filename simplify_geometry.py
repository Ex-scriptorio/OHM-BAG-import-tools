# This script reads geojson files and simplifies them by removing superfluous
# nodes from polygons. 

import os
import sys
import geopandas as gpd


def simplify_geometry(df):

    # In testing this tool on BAG exports, a tolerance of 10**-6 was found to 
    # remove most superfluous points while preserving geometries. However, 
    # since the tolerance is relative to the CRS of the data it might not work
    # as well in other applications.

    df['geometry'] = df['geometry'].simplify_coverage(10**-6)

def write_dataframe_to_file(df, path):

    if os.path.exists(path):

        if input('The file {} already exists.\nReplace it? (Y/n)'.format(path)).upper() != 'Y':
            
            # If path exists and user does not want to replace it, save it
            # with another name
            base, ext = os.path.splitext(path)
            
            i = 1
            while os.path.exists("{}_{}{}".format(base, i, ext)):
                i += 1

            path = "{}_{}{}".format(base, i, ext)
    
    # Write the dataframe to a file
    df.to_file(path, driver='GeoJSON')

def main():
    
    # Read command line arguments
    args = sys.argv[1:]

    # If no arguement was passed, let the user input a path
    if len(args) == 0:
        args.append(input('Enter a file path:\n>'))
   
    # Loop over the arguments 
    for arg in args:
        
        # If an invalid path was passed, throw an error
        if not os.path.exists(arg):
            raise FileNotFoundError("No such file or directory: '{}'".format(arg))

        # Read the file in as a geopandas dataframe
        df = gpd.read_file(arg)
        
        # Simplify the datadrame
        simplify_geometry(df)
        
        # Write the result to disk
        base, ext = os.path.splitext(arg)
        write_dataframe_to_file(df, "{}_simplified{}".format(base, ext))

if __name__ == "__main__":
    main()
