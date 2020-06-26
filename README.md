# MLPreprocessor
Preprocessor for shark detection ML algorithm that eliminates flase positives from Aerial drone based shark footage at the shores of Cape Cod

Tested and designed for Cape Cod diverse set of drone based shark footage collected by our sponsers. Object recognition algorithms cannot be used due to the wide field of view, the individual objects are low resolution and very little color gradient as submerged objects take the color of the ocean.

Discontinued approach: Try to Isolate Sharks before feeding to machine learning

![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/original.PNG)

Problems with the approach:
(The above result looks great, but is not representative of the dataset)
Due to wide field of view and low gradient of color between submerged sharks and background, very difficult to achieve.

Actual approach:
Identify common false positives that can confuse ML and try to eliminate them.
Common flase positives: Boats, Seals,Algae, Birds, Waves, Glare, Fish, Noise

We analyzed different color spaces for images in different conditions (having sharks, land, glare, boats, seals, different weather conditions etc). Analysis of the different color channels led us to realize that some features (such as waves) were greatly removed in some color spaces while some features (such as glare) were highly noticeable in some color spaces. This lead us to switch from the approach of trying to isolate the shark to trying to remove common hurdles that are not sharks.


![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/colorspaces.PNG)

Image is processed under different colorspaces and masked. After evrey processing, image was gradually blurred using the mask to make it blend with the background. Only false positives were blurred, sharks were not, maintaining the quality of the image in the region of interest.

Furthermore, linear combinations of colorspaces were obtained experimentally to produce a noise free image.


![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/mask.png)

Image below has a shark in the center.

![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/out.PNG)

As we can see in the above image, the background, glare, noise, etc are removed. So is the bird.
The shark remains but so does the boat shadow. This is because both submerged sharks and shadows are similar and is not differentiated by the preprocessor alone.
However, this is much noise free than the original image.



# Results on a Matlab Object Tracker
We evaluated the results on a Matlab object traker just to evaluate the preprocessor. The tracker parameters were changed for the purposes of the evaluation. One change was to only track objects with duration greater than a second to remove random noise. The other change was to specify bounding box sizes so only shark-sized objects would be tracked.

![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/tracker.png)

As we can see, from the middle and bottom images, the tracker tracks only the shark in the preprocessed image while the unprocessed image has a lot of noise.

We tested our algorithm against 50 selected videos from the video database. To effectively test the success and adaptability of our algorithm, videos in different weather, tidal and other ocean conditions as well as videos containing different objects were selected, including a few videos of vacant oceans. Clips where the camera was stationary were extracted from the videos to accommodate our motion based object tracker, as it is a requirement for our approach. Ideal videos refer to scenarios where the shark is obviously spotted by eye, which translates to minimal glare and the shark not being too deep. Otherwise the video is marked as non-ideal.

![alt text](https://github.com/ananta399/MLPreprocessor/blob/master/readmeImages/tables.PNG)

Algaes, Seals and other fish were most common false positives. This distinction is left out for other steps in the classification process. Deeply submerged sharks were most common false negatives.

# CONCLUSION
The image preprocessor, while needs to be improved, is a good proof-of-concept and can be used (with modifications) to remove false positives from object tracking algorithms or machine learning algorithms. The algorithm, although better under ideal conditions, was able to preprocess videos under different weather conditions, videos with wide field of view and therefore low resolution of objects, and submerged/hazy sharks to qualify for a proof-of-conecpt.
