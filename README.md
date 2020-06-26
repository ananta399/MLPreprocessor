# MLPreprocessor
Preprocessor for shark detection Ll algorithm that eliminates flase positives from Aerial drone based shark footage at the shores of Cape Cod

Discontinued approach: Try to Isolate Sharks before feeding to machine learning

![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/original.PNG)

Problems with the approach:
Due to wide field of view and low gradient of color between submerged sharks and background, very difficult to achieve.

Actual approach:
Identify common false positives that can confuse ML and try to eliminate them.
Common flase positives: Boats, Seals,Algae, Birds, Waves, Glare, Fish, Noise

We analyzed different color spaces for images in different conditions (having sharks, land, glare, boats, seals, different weather conditions etc). Analysis of the different color channels led us to realize that some features (such as waves) were greatly removed in some color spaces while some features (such as glare) were highly noticeable in some color spaces. This lead us to switch from the approach of trying to isolate the shark to trying to remove common hurdles that are not sharks.


![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/colorspaces.PNG)

Image is processed under different colorspaces and masked. After evrey processing, image was gradually blurred using the mask to make it blend with the background. Only false positives were blurred, sharks were not, maintaining the quality of the image in the region of interest.

Furthermore, linear combinations of colorspaces were obtained experimentally to produce a noise free image.


![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/mask.png)


![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/out.PNG)
