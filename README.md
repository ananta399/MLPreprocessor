# OpenCV Preprocessor
Preprocessor for shark detection ML algorithm that eliminates false positives from Aerial drone based shark footage at the shores. The ML algorithm is not included however, it can be assumed to analyze movement patterns.

Tested and designed for a diverse set of drone based shark footage collected by our sponsers. 
Object recognition algorithms could not be used due to the wide field of view. The individual objects are low resolution and have little color gradient as submerged objects take the color of the ocean.

## Approach

![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/original.PNG)

Identify common false positives that can confuse ML and try to eliminate them.
Common flase positives: Boats, Seals,Algae, Birds, Waves, Glare, Fish, Noise

Major hurdles:
*Low resolution of sharks given the wide field of view of the camera. For standard height of the drone, the area of a shark in our images was only around 15x5 pixels. Sharks further lost clarity when submerged.

*Sophisticated human visual processing. As you can see in the above image, our brain “tricks” us into believing the shark is black, however, isolating the shark reveals that it is actually still green. So, our images actually have low color gradient. A submerged shark may look black to the eye however, in an image, it takes the color of whatever water it is in. Water color depends on weather and other conditions.

Most of the time was spent experimenting rather than coding. Due to high altitude of the drones, the sharks were just tiny low resolution hazy blobs with no defining features. Furthermore, as they were submerged, they had no distinct color and just took the color of the ocean with little color gradient. The color of the ocean also changed with different weather and lighting conditions. 

We analyzed different color spaces for images in different conditions (having sharks, land, glare, boats, seals, different weather conditions etc). Analysis of the different color channels led us to realize that some features (such as waves) were greatly removed in some color spaces while some features (such as glare) were highly noticeable in some color spaces. This lead us to switch from the approach of trying to isolate the shark to trying to remove common hurdles that are not sharks.


![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/colorspaces.PNG)

Note that the image above is just an example of the concept and not necessarily the algorithm.

Image is processed under different colorspaces and masked using thresholding. After every individual colorspace processing, image was gradually blurred using the mask to make it blend with the background. Only the region of no interest was blurred, sharks were not, maintaining the quality of the image in the region of interest.

Furthermore, linear combinations of colorspaces were obtained experimentally to produce a noise free image.


![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/mask1.png)

The above example image has a shark in the center, a bird in the top right corner, waves, shore, glare, and a boat. The final output image is given below.

![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/out.PNG)

As we can see in the above image, the background, glare, noise, etc are removed. So is the bird.
The shark remains but so does the boat shadow. This is because both submerged sharks and shadows are similar and is not differentiated by the preprocessor alone.
However, this is much noise free than the original image.



## Results on a Matlab Object Tracker
We evaluated the results on a Matlab object traker just to evaluate the preprocessor. The tracker parameters were changed to only track objects with duration greater than a second to remove random noise.

![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/tracker1.png)

As we can see, from the middle and bottom images, the tracker tracks only the shark in the preprocessed image while the unprocessed image has a lot of noise.

We tested our algorithm against 50 selected videos from the video database. To effectively test the success and adaptability of our algorithm, videos in different weather, tidal and other ocean conditions as well as videos containing different objects were selected, including a few videos of vacant oceans. Clips where the camera was stationary were extracted from the videos to accommodate our motion based object tracker, as it is a requirement for our approach. Ideal videos refer to scenarios where the shark is obviously spotted by eye, which translates to minimal glare and the shark not being too deep. Otherwise the video is marked as non-ideal.

![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/tables.PNG)

Algaes, Seals and other fish were most common false positives. This distinction is left out for other steps in the classification process. Deeply submerged sharks were most common false negatives.

## CONCLUSION
The image preprocessor, while needs to be improved, is a good proof-of-concept and can be used (with modifications) to remove false positives from object tracking algorithms or machine learning algorithms. The algorithm, although better under ideal conditions, was able to preprocess videos under different weather conditions, videos with wide field of view and therefore low resolution of objects, and submerged/hazy sharks to qualify for a proof-of-conecpt.
