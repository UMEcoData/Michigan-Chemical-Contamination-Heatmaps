import csv
import matplotlib
import matplotlib.pylab as pylab
from matplotlib import pylab
from pylab import *
import os
import shutil
import sys


#Edit: Choose UCMR and boundry files to work with
ucmr_file = "Michigan_UCMR4.csv"
boundry_file = "zt26_d00"






#get the working directories for this code
output_direc = os.getcwd() + "/output/"
input_direc = os.getcwd() + "/input/"


def read_ascii_boundary(filestem):
    '''
    Reads polygon data from an ASCII boundary file.
    Returns a dictionary with polygon IDs for keys. The value for each
    key is another dictionary with three keys:
    'name' - the name of the polygon
    'polygon' - list of (longitude, latitude) pairs defining the main
    polygon boundary
    'exclusions' - list of lists of (lon, lat) pairs for any exclusions in
    the main polygon
    '''
    metadata_file = filestem + 'a.dat'
    data_file = filestem + '.dat'
    # Read metadata
    lines = [line.strip().strip('"') for line in open(metadata_file)]
   
    polygon_ids = lines[::6]
    #print(polygon_ids)
    polygon_names = lines[2::6]
    #print(polygon_names)
    polygon_data = {}

    for polygon_id, polygon_name in zip(polygon_ids, polygon_names):
        # Initialize entry with name of polygon.
        # In this case the polygon_name will be the 5-digit ZIP code.
        polygon_data[polygon_id] = {'name': polygon_name}
        #print(polygon_data[polygon_id])
    del polygon_data['0']


    # Read lon and lat.
    f = open(data_file)
    for line in f:
        fields = line.split()
        if len(fields) == 3:
            # Initialize new polygon
            polygon_id = fields[0]
            #print(polygon_id)
            polygon_data[polygon_id]['polygon'] = []
            polygon_data[polygon_id]['exclusions'] = []
        elif len(fields) == 1:
            #print(0)
            # -99999 denotes the start of a new sub-polygon
            if fields[0] == '-99999':
                #print(1)
                polygon_data[polygon_id]['exclusions'].append([])
        else:
            # Add lon/lat pair to main polygon or exclusion
            lon = float(fields[0])
            lat = float(fields[1])
            if polygon_data[polygon_id]['exclusions']:
                polygon_data[polygon_id]['exclusions'][-1].append((lon, lat))
                #print(1)
            else:
                polygon_data[polygon_id]['polygon'].append((lon, lat))
    #print(polygon_data)
    return polygon_data



def create_chemical_heatmaps(filename, d, chem_name, year):

    
    #open csv of contaminant data from our chem files
    f = csv.reader(open((output_direc + 'chem_files/' + filename), 'rt'))
    vals = {}
    # Skip header line
    next(f)
    # Add data for each ZIP code
    for row in f:
        #zipcode, resultvalue = row
        number, date, zipcode, resultvalue = row
        vals[zipcode] = float(resultvalue)
    max_vals = max(vals.values())

    # Create figure and two axes: one to hold the map and one to hold
    # the colorbar
    figure(figsize=(20, 20), dpi=100)
    #map_axis = axes([0.0, 0.0, 8, 9])
    #cb_axis = axes([8.3, 1, 0.3, 6])

    #figure(figsize=(5, 5), dpi=30)
    map_axis = axes([0.0, 0.0, 0.9, 0.9])
    cb_axis = axes([0.83, 0.1, 0.03, 0.6])

    # Define colormap to color the ZIP codes.
    # You can try changing this to cm.Blues or any other colormap
    # to get a different effect
    cmap = cm.YlOrRd

    # Create the map axis
    axes(map_axis)
    axis([-90, -80, 40, 50])
    gca().set_axis_off()

    # Loop over the ZIP codes in the boundary file

    for polygon_id in d:
        polygon_data = array(d[polygon_id]['polygon'])
        zipcode = d[polygon_id]['name']
        num_vals = vals[zipcode] if zipcode in vals else 0.
        # Define the color for the ZIP code
        fc = cmap(num_vals / max_vals)
        # Draw the ZIP code
        patch = Polygon(array(polygon_data), facecolor=fc,
            edgecolor=(.3, .3, .3, 1), linewidth=.2)
        gca().add_patch(patch)
    title(('Above minimum reporting levels in Michigan for ' + chem_name), fontsize=30)

    # Draw colorbar
    cb = mpl.colorbar.ColorbarBase(cb_axis, cmap=cmap,
        norm = mpl.colors.Normalize(vmin=0, vmax=max_vals))
    cb.set_label('Critical Value Level', fontsize=40)

    # Change all fonts to Dejavu Sans
    for o in gcf().findobj(matplotlib.text.Text):
        o.set_fontname('DeJavu Sans')




    if not os.path.exists(output_direc + 'maps/'+ chem_name):
      os.makedirs(output_direc + 'maps/'+ chem_name)

    # Export figure to bitmap and save into the maps folder
    savefig(output_direc + 'maps/'+ chem_name + '/' + chem_name + '_' + year + '_map.png')
    close()



def choose_chemical_heatmaps(chem_option):


    # Read in ZIP code boundaries for Michigan
    d = read_ascii_boundary(input_direc + boundry_file)


    # Decide which chemicals maps to generate based on the user chem option input

    #If the user chooses all the maps
    if chem_option == 'all_chemicals':
        

        folder = output_direc + 'chem_year_index/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        #grab each file
        for file in os.listdir(output_direc + "chem_files/"):

         #split our file names to get a chemical name and year as strings
         chunks = file.split("_")
         chem_name = (chunks[0])
         year = (chunks[1])

         #Create the chemical heatmap for the file
         create_chemical_heatmaps(file, d, chem_name, year)

        
         #Create an index of all the years a chemical has data for
         os.chdir(output_direc + 'chem_year_index/')
         chem_year_index= open((chem_name+".txt"),"a+")
         chem_year_index.write(year + "\n")
         chem_year_index.close()


    #do a similar process except now when the user only selects for the single 
    else:


        
        filePath = (output_direc + "chem_year_index/" + chem_option +".txt")
        
        # As the chem year index file at filePath is deleted now, so we should check if chem year index file exists or not not before deleting them
        if os.path.exists(filePath):
            os.remove(filePath)

        for file in os.listdir(output_direc + 'chem_files/'):
            if chem_option in file:

                chunks = file.split("_")
                chem_name = (chunks[0])
                year = (chunks[1])


                create_chemical_heatmaps(file, d, chem_name, year)

                #Create an index of all the years a chemical has data for
                os.chdir(output_direc + 'chem_year_index/')
                chem_year_index= open((chem_name+".txt"),"a+")
                chem_year_index.write( year + "\n")
                chem_year_index.close()



def create_chemical_index():

        filePath = (output_direc)
        textfile = (output_direc + 'chem_index.txt')
        
        # As the chem year index file at filePath is deleted now, so we should check if chem year index file exists or not not before deleting them
        if os.path.exists(textfile):
            os.remove(textfile)

        for file in os.listdir(output_direc + 'chem_files/'):
           

                chunks = file.split("_")
                chem_name = (chunks[0])


                #Create an index of all the chemicals
                os.chdir(filePath)
                chem_year_index= open(("chem_index.txt"),"a+")
                with open(output_direc + 'chem_index.txt') as w:
                    if chem_name in w.read():
                        chem_year_index.close()
                    else:
                        chem_year_index.write( chem_name + "\n" + "------" + "\n")
                        chem_year_index.close()
                w.close()

        #add the all option
        os.chdir(filePath)
        chem_year_index= open(("chem_index.txt"),"a+")
        chem_year_index.write("all_chemicals"+ "\n")
        chem_year_index.close()


        #print the chemicals to the user
        f = open('chem_index.txt','r')
        message = f.read()
        print(message)
        f.close()
        os.chdir(output_direc)





if __name__ == '__main__':

    create_chemical_index()

    

    #This will be the sole user input
    chem_option = input("Choose an above chemical option \n" + "\n")
    print("\n" + "you wrote " + chem_option + "\n")
    #chem_option = 'all'

    


    if chem_option != "all_chemicals":
        textfile = (output_direc + 'chem_year_index/' + chem_option +".txt" )
        with open(output_direc + 'chem_index.txt') as w:
            if chem_option in w.read():
                print(".......running.......")
                choose_chemical_heatmaps(chem_option);
                print("Done!\n" + "\n")
                print("Years of Michigan " + chem_option + " heatmaps" + "\n" + "------------")
                f = open(textfile,'r')
                message = f.read()
                print(message)
                f.close()
                print("Michigan heatmaps found in " + output_direc + '/maps/')
            else:
                print("either no chemical data found or revise your input; run program again")
    else:
        print(".......running.......")
        choose_chemical_heatmaps(chem_option);
        print("Done!\n" + "\n")
        print("Michigan Chemical Heatmaps Available for years 2012-2019"+ "\n" + "---------------------")
        print("Michigan heatmaps found in " + output_direc + '/maps/' + "\n")
    




#Inspiration from https://www.christianpeccei.com/zipmap/