# Image-Deduplicator

## How to run

### Choose configuration
- The configuration is read from a json file, namely json.config. There we can choose which images to check for duplicates.
- The "*relative_path*" key corresponds to the folder, where the images live.
- The "*check_all*" key is set to "*No*". If set to "*Yes*" then it overwrites the parameter "*lof_images*" and checks **all** images for duplicates

### Execution Instructions
To run, first install the requirements and then run the main script. 
```bash
pip install -r requirements.txt
python3 ImageDeduplicator.py
```

## Possible Improvements
1. Use histogram, exploit all channels in the image instead of converting it to gray scale 
2. Test different hashing function, e.g., average hash, difference hash or perceptual hash
3. Use annotated data, i.e., know that two ads are duplicated. In this case, we can use all the abovementioned features. The similarity values between images, expressed in terms of distances between hashes or image histograms, can be fed as input to some ML algorith that will learn disciminating rules.
