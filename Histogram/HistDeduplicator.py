import cv2
import os
import numpy as np
import json

class HistDeduplicator():
    
    """
    This class reads and stores all images in a target folder. For each image, it computes 
    the histogram and the correlation between histograms to identify possible duplicates.
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
        self._lof_images = list()

        # Load list of images
        for img_idx, img_name in enumerate(self._lof_filenames):
            # Load images and store them to list
            self._lof_images.append(cv2.imread(self._img_filepath+img_name))

    def _compute_dof_histograms(self):
        """
        For each image compute the normalized histogram using 256 bins.
        """
        dof_histograms = dict()
        for img_idx, img in enumerate(self._lof_images):
            img_hist = cv2.calcHist([img],[0],None, [256], [0, 256])
            cv2.normalize(img_hist, img_hist, 0, 255, cv2.NORM_MINMAX)
            dof_histograms[img_idx] = img_hist
        return dof_histograms

    def _compute_histogram_corr(self, img_name):
        """
        Compute correlation between the histogram of the selected image, that 
        given as input, and the histograms of all other images in the folder. 
        Parameters
        ----------
        img_name : string that corresponds to the filename that we want to check for duplicates
        """
        dof_histograms = self._compute_dof_histograms()
        img_idx        = self._lof_filenames.index(img_name)
        img_histogram  = dof_histograms[img_idx]
        aof_correlations = np.zeros(len(self._lof_images))
        for idx in range(len(dof_histograms)):
            other_histogram       = dof_histograms[idx]
            aof_correlations[idx] = self.hist_corr(img_histogram, other_histogram)
        return aof_correlations

    def _find_duplicates(self, img_name, tol=0.95):
        """
        Check if the target image has duplicates
        Parameters
        ----------
        img_name : string that corresponds to the filename that we want to check for duplicates
        tol      : float that corresponds to the threshold rho_s, such that if the correlation 
                   between two histograms is greater than rho_s then they are considered as duplicates
        """
        aof_correlations = self._compute_histogram_corr(img_name)
        lof_nearest_img = list(np.where(aof_correlations>tol)[0])
        # Remove the index that corresponds to the correlation  
        # between the target image and itself (it is always 1)
        lof_nearest_img.remove(self._lof_filenames.index(img_name))
        return [self._lof_filenames[idx] for idx in lof_nearest_img]
    
    @staticmethod
    def hist_corr(hist1, hist2):
        return cv2.compareHist(hist1, hist2, 0)

