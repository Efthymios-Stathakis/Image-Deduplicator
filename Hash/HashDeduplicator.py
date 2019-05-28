from PIL import Image
from imagehash import average_hash as ahash, dhash, phash, whash
import os
import numpy as np
import json

class HashDeduplicator():
    
    """
    This class reads and stores all images in a target folder. For each image, 
    it computes a hash value and it compares the hamming distance between hash 
    values to detect if there are any duplicate images
    """
    def __init__(self, rel_path='/images/'):
        """
        Initialize the class and some attributes

        Parameters
        ----------
        rel_path : string that corresponds to the nested folder containing the images
        """
        self._img_filepath  = os.getcwd()+rel_path
        self._lof_filenames = os.listdir(self._img_filepath)
        self._hash_val = None
        self._lof_images = list()

        # Load list of images
        for img_idx, img_name in enumerate(self._lof_filenames):
            # Load image and convert to grayscale
            self._lof_images.append(Image.open(self._img_filepath+img_name).convert('L'))

    def _compute_aof_hashes(self):
        """
        Each image is reshaped to match the expected input size of the hashing function "whash". 
        The resulting matrices are vectorized to simplify computations
        """
        hash_val = self._get_hashval()
        aof_hashes = np.zeros((hash_val**2, len(self._lof_images)))
              
        for img_idx, img in enumerate(self._lof_images):
            resized_img            = img.resize((hash_val+1, hash_val), Image.ANTIALIAS)
            aof_hashes[:, img_idx] = whash(resized_img, hash_size=hash_val).hash\
                                                                           .ravel()
        return aof_hashes

    def _compute_hash_key_distances(self, img_name):
        """
        We compute all distances between the hash vector of the selected image, 
        given as input, and all images in the folder 
        Parameters
        ----------
        img_name : string that corresponds to the filename that we want to check for duplicates
        """
        aof_hashes    = self._compute_aof_hashes()
        img_idx       = self._lof_filenames.index(img_name)
        img_phash     = aof_hashes[:, img_idx]
        aof_distances = self.hamming_dist(aof_hashes, img_phash.reshape(-1,1))
        return aof_distances

    def _find_duplicates(self, img_name, tol=1e-1):
        """
        Check if the target image has duplicates
        Parameters
        ----------
        img_name : string that corresponds to the filename that we want to check for duplicates
        tol      : float that corresponds to the threshold t_s, such that if the distance between 
                   two images is less than t_s then they are considered as duplicates of each otehr 
        """
        aof_distances = self._compute_hash_key_distances(img_name)
        lof_nearest_img = list(np.where(aof_distances<tol)[0])
        # Remove the index that corresponds to the distance  
        # between the target image and itself (it is always 0)
        lof_nearest_img.remove(self._lof_filenames.index(img_name))
        return [self._lof_filenames[idx] for idx in lof_nearest_img]
    
    def _get_hashval(self):
        """
        In general, the images may have different sizes. We want to choose a hash value as 
        large as possible and that is also a power of 2. We find the smallest dimension d_min 
        among all images and then return the largest power of 2 that is less than d_v. For 
        example, if d_v=150 then hash_val=128, if d_v=90 then hash_val=64
        """
        # Find the minimum dimension d_min among all images
        size_array = np.zeros((len(self._lof_filenames),2))
        for img_idx, img_name in enumerate(self._lof_filenames):
            # Store the 2-d shape of the image
            size_array[img_idx,:] = self._lof_images[img_idx].size

        # The hash size will be the largest power of that is smaller than d_min 
        self._hash_val = np.power(2, int(np.log2(int(size_array.min()))))
        return self._hash_val
    
    @staticmethod
    def hamming_dist(input_arr, input_vec):
        return np.abs(input_arr - input_vec.reshape(-1,1)).mean(axis=0)
