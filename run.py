from Hash.HashDeduplicator import HashDeduplicator
from Histogram.HistDeduplicator import HistDeduplicator
import json

def run():
    print('Starting Deduplicator')
    
    with open('config.json') as json_file:  
        params = json.load(json_file)
        
    path_params       = params['relative_path']
    method     = params['method']
    if method == 'Hash':
        deduplicator = HashDeduplicator(path_params)
    elif method == 'Hist':
        deduplicator = HistDeduplicator(path_params)
    
    lof_images = params['lof_images']
    check_all  = params['check_all']
    if check_all == 'Yes':
        lof_images = deduplicator._lof_filenames
    
    for img in lof_images:
        lof_duplicates = deduplicator._find_duplicates(img)
        if len(lof_duplicates)==0:
            print('Found no duplicates for {}'.format(img))
        else:
            print('Found {} as duplicates for {}'.format(lof_duplicates, img))
            
if __name__ == '__main__':
    run()
