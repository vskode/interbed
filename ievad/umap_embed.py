import yaml
import pickle
import numpy as np
from pathlib import Path
from ievad.generate_embeddings import generate_embeddings, Loader
 
with open('ievad/config.yaml', 'rb') as f:
    config = yaml.safe_load(f)
    

def get_embeddings(limit = None):
    generate_embeddings(model_name=config['embedding_model'], 
                        ignore_check_if_combination_exists=False)
    generate_embeddings(model_name='umap', 
                        ignore_check_if_combination_exists=False)

    ld = Loader(model_name='umap', 
                ignore_check_if_combination_exists=False)
    embeds = []
    for file in ld.files:
        embeds.append(ld.load(file))
    
    # return acc_embeddings, file_list, lengths

def create_timeList(lengths, files):
    lin_array = np.arange(0, max(lengths), 0.96)
    files_array = []
    divisions_array = []
    for i in range(len(lengths)):
        for j in range(lengths[i]):
            files_array.append(files[i])
            divisions_array.append(
                f'{int(lin_array[j]/60)}:{np.mod(lin_array[j], 60):.2f}s')
    return divisions_array, files_array
    
def generate_umaps(audioEmbeddingsList, lengths, files):
    umap_embeds = compute_umap_embeddings(audioEmbeddingsList)

    divisions_array, files_array = create_timeList(lengths, 
                                [f.stem for f in files])
