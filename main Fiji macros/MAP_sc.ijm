macro"map_singleChannel [g]"{
	//extract the airy scan image from .czi file
	//{
	//only 488 channel is imaged here
	dir= getDirectory("image");//get the directory of current active image
	title=getTitle;// here name includes the extension
	Index = indexOf(title, ".czi"); 
	name1 = substring(title, 0, Index); //exclude extension
	run("Duplicate...", "duplicate channels=1 frames=1");
	//extrac the zeiss file ".czi" with airyscan mode ON. 
	//only 488 is imaged here.
	NewName = dir+name1+"-1"+".tif";//the name of the extracted image, directory+name+extension
	NewTitle = name1+"-1"+".tif";//only the name+extension
	saveAs("Tiff", NewName);
	selectWindow(title);//select the .czi file
	close();//close the .czi file
	//the end of the extract of aryscan image}
	
	selectWindow(NewTitle);//select the extract image
	run("8-bit");
	//setAutoThreshold("Default dark");
	//setAutoThreshold("IsoData dark");
	//setAutoThreshold("IJ_IsoData dark");
	//setAutoThreshold("MaxEntropy dark");
	//setAutoThreshold("Yen dark");
	//setAutoThreshold("Intermodes dark");
	//setAutoThreshold("Huang dark");
	//setAutoThreshold("IsoData dark");
	//setAutoThreshold("MinError dark");
	//setAutoThreshold("Otsu dark");
	//setAutoThreshold("Mean dark");
	//setAutoThreshold("Minimum dark");
	//setAutoThreshold("Triangle dark");
	//setAutoThreshold("Default dark");
	//setAutoThreshold("Shanbhag dark");
	
	////////////////////////////////////
	//try all the threshold methods
	////////////////////////////////////
	
	run("Auto Threshold", "method=[Try all] ignore_black ignore_white show");
	close();
	logString =getInfo("log");
	lines=split(logString, "\n"); 
	mArray = newArray(18);
	//exclude the lines contains "Intermodes Threshold not found after 10000 iterations."
	//exclude the lines contains "not converging. Try 'Ignore black/white' options"
	j=0
	for(i=0; i<lines.length; i++) {
		suffix1 = "Threshold not found after 10000 iterations.";
		suffix2 = "not converging. Try 'Ignore black/white' options";
		if (endsWith(lines[i], suffix1)){
			print("this line not read");
		}
		else if (endsWith(lines[i], suffix1)){
			print("this line not read");
		}
		else{
			mArray[j]=lines[i];
			j++;
			}
		
		}
	print("print the clean table");
	Array.print(mArray);
	thrArray= newArray(7);
	//different autothreshold methods
	thrArray[0]=mArray[0];//default
	thrArray[1]=mArray[4];//isoData
	thrArray[2]=mArray[6];//maxentropy
	thrArray[3]=mArray[10];//moments
	thrArray[4]=mArray[11];//otsu
	thrArray[5]=mArray[13];//Renyientropy
	thrArray[6]=mArray[16];//yen
	print("the chosen ones");
	Array.print(thrArray);
	thrValArray = newArray(7);
	for(i=0; i<thrArray.length; i++) {
		val = split(thrArray[i],": ");
		val = parseInt(val[1]);
		thrValArray[i]=val;
		}
	print("extract the value");
	Array.print(thrValArray);
	Array.getStatistics(thrValArray, min, max, mean, std);
	  print("stats");
	  print("   min: "+min);
	  print("   max: "+max);
	  print("   mean: "+mean);
	  print("   std dev: "+std);
	
	//get the geometricMean
	  function GeometricMean(array1) {
	  	x = array1[0];
	  	n=array1.length;
	  	for(i=1; i<n; i++) {
	  		x=x*array1[i];
	  		}
	  	x=pow(x,1/n);
	      return x;
	  }
	  geomean = GeometricMean(thrValArray)
	  print("	geometric mean:	"+geomean);
	
	  //sort the array from the lowest to highest
	Array.sort(thrValArray);
	//get the median
	median =thrValArray[3];
	 print("	median: "+median);
	Array.print(thrValArray);
	
	//run("Threshold..."); 
	//choose one threshold
	// we can choose min max mean geomean median
	setThreshold((geomean+median)/2,255);
	//setThreshold(27,255);
	//getThreshold(minInUse,maxInUse);
	//##looks like a fixed threshold is more suitable to exclude the muscle region
	//setThreshold(26,255);
	//print("the used threshold is: "+minInUse+ " & "+maxInUse)
	if(isOpen("Threshold")){
	selectWindow("Threshold");
	run("Close");
	}

	
	//waitForUser("set the threshold and press OK, or cancel to exit macro"); 
	//run("Close");
	//run("Make Binary", "thresholded remaining black");
	run("Convert to Mask");
	//run("Fill Holes");
	//run("Watershed");
	//run("Watershed");
	// to remove the small pixel dots process->noise-> despeckle OR
	//it looks like the median filter works better for me. process-> filters-> median
	run("Median...", "radius=1");
	Name2 = dir+name1+"-oriBi"+".tif";//the name of the extracted image, directory+name+extension
	Title2 = name1+"-oriBi"+".tif";//only the name+extension
	saveAs("Tiff", Name2);
	if(1){
	//choose the particle size
	run("Analyze Particles...", "size=0-1000 pixel circularity=0.10-1.00 show=Masks display add");
	//the mask window
	maskWindowTitle = "Mask of "+Title2;
	selectWindow(maskWindowTitle);
	
	run("Close-");
	//////remove the frame of the image
	getDimensions(width, height, channels, slices, frames);
	xmax=width-1;
	ymax=height-1;
	setColor(0);
	drawLine(0,0,0,ymax);
	drawLine(0,0,xmax,0);
	drawLine(xmax,0,xmax,ymax);
	drawLine(0,ymax,xmax,ymax);
	//////
	run("Convert to Mask");
	//run("Fill Holes");
	run("Watershed");
	}
	Name3 = dir+name1+"-binary"+".tif";//the name of the extracted image, directory+name+extension
	Title3 = name1+"-binary"+".tif";//only the name+extension
	saveAs("Tiff", Name3);
	
	selectWindow(Title3);
	
	MaskName = dir+name1+"-msk"+".tif";//the mask image directory+name+extension
	TxtName = dir+name1+"-msk"+".txt";//the txt image directory+name+extension
	saveAs("Tiff", MaskName);
	saveAs("Text Image", TxtName);
	
	// Closes all image windows.
	close("*");
	

if(isOpen("Log")){
	selectWindow("Log");
	run("Close");
	}
if(isOpen("Results")){
selectWindow("Results");
run("Close");
}
if(isOpen("ROI Manager")){
selectWindow("ROI Manager");
run("Close");
}

run("Close All");
	}//extract the airy scan image from .czi file
}
macro "cleanWindows [c]" {
      	if(isOpen("ROI Manager")){
			selectWindow("ROI Manager");
			run("Close");
		}
		close("*");//close all active image
		if(isOpen("Log")){
			selectWindow("Log");
			run("Close");
		}
		if (isOpen("Results")){
			selectWindow("Results");
			run("Close");
		}
  }
  macro "EMTmask [e]" {
		s1= File.openAsString("C:/ZEN/currentTile.txt");
		lines=split(s1,"\n");
		print(lines.length);
		print(lines[0]);//the directory to store the image
		print(lines[1]);// the path of the empty mask file
		close("*")
		newImage("fakemask", "8-bit black", 512, 512, 1);	
  		saveAs("Text Image", lines[1]);
  		close("*")
  		      	if(isOpen("ROI Manager")){
			selectWindow("ROI Manager");
			run("Close");
		}
		close("*");//close all active image
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
  }