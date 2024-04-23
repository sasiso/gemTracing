// Macro to find the outline of a gemstone in an image

// Open the image
open("C:\\Users\\sss\\Desktop\\Archive\\gemTracing\\test\\1.jpg");
// Macro to find the outline of a gemstone in an image with background removal and blurring

// Convert to grayscale
run("8-bit");

 // Apply median filter with a 5-pixel radius
 run("Median...", "radius=5");

setAutoThreshold("Default dark 16-bit no-reset");
//run("Threshold...");
setAutoThreshold("Default 16-bit no-reset");
setThreshold(0, 250);
setOption("BlackBackground", false);
run("Convert to Mask");
run("Find Edges");
