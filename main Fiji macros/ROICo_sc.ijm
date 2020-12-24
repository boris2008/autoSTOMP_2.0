macro"ROICo_sc [g]"{
function readROICo(path){
    //1. open .czi file in imagej. this .czi file contains a single channel
    open(path);
    filename= File.nameWithoutExtension;
    print(filename);
    dir = File.directory;
    
	run("16-bit");
	run("Brightness/Contrast...");
	waitForUser("adjust every channel, OK to finish");
	//selectWindow("Composite");
	
	cname = filename+".tif";
	saveAs("Tiff", dir+cname);
	run("Scale to Fit"); //fit all the whole image into the current window. image=> zoom=> scale to fit
	//slide the bar at the bottom "c", ajust the brightness and contrast for each channel in the "B&C" window. 
	setTool("freehand");
	//open the ROI manager
	run("ROI Manager...");
	roiManager("Show All");
	waitForUser("Draw, add ROIs manually, OK to finish");  
	//makePolygon(1672,554,1612,638,1588,776,1616,884,1690,974,1772,984,1852,956,1916,832,1914,710,1846,552,1784,528);
	resultfile = dir+filename+"_ROICo.txt";
	f = File.open(resultfile); 
	numROIs = roiManager("count");
		for(i=0; i<numROIs;i++) {
		// loop through ROIs
		roiManager("Select", i);
		getSelectionCoordinates(x, y);//if the ROI is a multipoint ROIs x and y are arrays
		ind = i+1;
		print(f,"---ROI "+ind+"---"+"has "+x.length+" coordinates x & y in pixels\n");
		//print("y-array size: "+y.length);
		for (j=0; j<x.length; j++) {
			print(f,x[j]+"\t"+y[j]+"\n");
			}
		}
	File.close(f);
	
	run("Scale to Fit"); //fit all the whole image into the current window. image=> zoom=> scale to fit

	//You can look to the function selectionType() IF this returns -1, there is no selection (place your function here)
	//ELSE do something else -1 is the value for no selection. So that will prevents you from getting a error.

	//measure all the selections in ROI manager
	//measure the area and centroid of the ROIs. The results in the unit of micron
	//run("Set Measurements...", "area centroid redirect=None decimal=2");
	run("Set Measurements...", "centroid redirect=None decimal=2");
	array=newArray(numROIs);
	for(i=0; i<numROIs;i++) {
	        array[i] = i;
	}
	roiManager("Select", array);
	roiManager("Measure");
	measurefile = dir+filename+"_centroid_"+".csv";
	saveAs("Results", measurefile);
    //select the image and save the selections to it.
    selectWindow(cname);
	run("From ROI Manager");
	run("Save");
	close("*");//close all active image
	//close other windows
	if(isOpen("Log")){
		selectWindow("Log");
		run("Close");
	}
	if (isOpen("Results")){
		selectWindow("Results");
		run("Close");
	}
	if(isOpen("ROI Manager")){
		selectWindow("ROI Manager");
		run("Close");
	}
	if(isOpen("B&C")){
		selectWindow("B&C");
		run("Close");
	}
}      
//path1=File.openDialog("choose a file");
//readROICo(path1);


//dir = getDirectory("Choose a Directory ");//open dialogue and ask for a directory
//setBatchMode(true);
f = File.openAsString("C:/ZEN/pwd_mROIs.txt");
lines=split(f,"\n"); //to convert the string to an array of lines.
nlines = lines.length;
Array.print(lines);
print(nlines);
for (i=0; i<nlines; i++) {
print(lines[i]);
}
dir = lines[1]//the second one is the directory that contains the tile scan image
list = getFileList(dir);
for (i=0; i<list.length; i++) {
          if (endsWith(list[i], ".czi")){
          	print(list[i]);
              readROICo(dir+list[i]);
          }
              
              if ((i+1)==list.length)
              	waitForUser("finished!");
}
waitForUser("spyder=>EOE...=>tile_imputation.py");
exit();
}