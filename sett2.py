import os
import sys
import imp

def simulate(runName, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax):
    """Create images of a simulated liquid crystal films with defects

    Args:
        runName (str): the name of the directory the output of this function will be stored in. If it already exists, nothing will be overwritten
        numImages (int): number of images the function should create
        imageDims (list): dimensions of the images to be simulated as [x, y]
        maxDefects (int): maximum number of defects an image can have
        minDefects (int): minimum number of defects an image can have
        decrossMin (int): minimum "Hourglass-ness" of a defect UPDATE
        decrossMax (int): maximum "Hourglass-ness" of a defect UPDATE

    Writes:
        *_defect*.dat: Writes defect location data files to ../sett2/<runName>
        *_out*.dat: Writes spin data files to ../sett2/<runName>
        *_defect*.jpg: Writes images of the schlieren texture to ../sett2/<runName>
        *_defect*.txt: *defect*.dat converted to txt written to ../sett2/<runName>
        *_defect*SIMMARKED.jpg: Writes images of schlieren texture with annotated defects to ../sett2/<runName>/SIMMARKED
        *_defect*.xml: Writes defect bounding boxes in .xml format for YOLO training to ../sett2/<runName>/out

    Note:
        Creates *out*.dat files storing spins of individual molecules, *defect*.dat with defect locations marked.
        Also creates .jpg files containing the schlieren texture, the same images with annotated defect locaions and
        .xml files with defect locations to be used by YOLO.

    """

    simString = 'simulations/randomDefects/runSim.py' # Path containing the runSim module.
    functionName = 'runSim' # Name of function being instantiated in runSim.

    home = os.getcwd() + '/defectSimulation/' # Home directory of sett2.

    print("Running Simulation")

    path, exFile = os.path.split(simString) # Splitting path and runSim.py.
    fullPath = os.path.join(home, path) # Creating full path for runSim.py.
    sys.path.append(fullPath) # Adding simulation directory to PATH.
    os.chdir(fullPath) # Changing directory to simulation.

    # Importing the module runSim.
    sim = imp.load_source('packages', exFile)

    # Importing the function in runSim.
    runSimulation = getattr(sim,functionName)

    # Calling function to simulate.
    runSimulation(home, runName, numImages, imageDims, maxDefects, minDefects, decrossMin, decrossMax)

    # Changing directory back to home.
    os.chdir(home)

def extractSmartNoise(crop, cropManual, cropX, cropY):
    """Extract noise .jpg files from experimental images as .bmp files

    Args:
        crop (bool): Decide whether the experimental images should be cropped before extracting noise
        cropManual (bool): Decide whether all images should be cropped manually with individual limits
        cropX (int): crop width used when cropManual is False
        cropY (int): crop height used when cropManual is False

    Writes:
        noise*.jpg: Noise image files written to ../sett2/smartNoise/noiseSamples/noiseFiles

    Note:
        Input .bmp experimental images in the folder ..sett2/smartNoise/noiseSamples and decide 
        the region being used with cropping parameters. Noise will be extracted and images will be created 
        at ../sett2/smartNoise/noiseSamples/noiseFiles as .jpg files.

    """

    path = "/smartNoise/" # Path containing the noiseExtractor module.

    noiseSamplePath = "/smartNoise/noiseSamples/" # Path containing .bmp experimental images.
    
    home = os.getcwd() + '/defectSimulation/' # Home directory of sett2.

    print("Extracting Smart Noise")
    
    functionPath = home + path # Path of noiseExtractor function.
    
    # Importing the module noiseExtractor.
    noiseExtraction = imp.load_source('packages', os.path.join(functionPath,'noiseExtractor.py'))
    
    # Calling function noiseExtractor.
    noiseExtraction.noiseExtractor(home, noiseSamplePath, crop, cropManual, cropX, cropY)