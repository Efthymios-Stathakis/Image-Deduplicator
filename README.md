# Image-Deduplicator

## How to run

### Choose configuration
- The configuration for executing the deduplicator module is read from a json file, namely **config.json**. There we can choose the deduplicator method and which images to check for duplicates.
- The "*method*" key corresponds to the method used for detecting duplicates. 
  * *Hash* uses distance between image hashes
  * *Hist* uses correlation between image histograms  
- The "*relative_path*" key corresponds to the folder, where the .jpg images live.
- The "*check_all*" key is set to "*No*". If set to "*Yes*" then it overwrites the parameter "*lof_images*" and checks **all** images for duplicates

### Execution Instructions
To run, first install the requirements and then run the main script. 
```bash
pip3 install -r requirements.txt
python3 run.py
```
## To-Do List
Make the threshold for similarity, e.g., correlation threshold or mean distance threshold, parametrizable. For the time being, the thresholds have fixed values.

## Possible Improvements
1. Use and exploit all channels in the image instead of converting it to gray scale or using just one channel.
2. Test different hashing function, e.g., average hash, difference hash or perceptual hash, perhaps even make the choice of hash function a parameter.
3. Use annotated data, e.g., when we know that two ads are duplicates. In this case, we can use all the abovementioned features. The similarity metrics between images, expressed in terms of distances between hashes or correlation of histograms, can be fed as input to some ML algorith that will learn the underlying disciminating rules.
