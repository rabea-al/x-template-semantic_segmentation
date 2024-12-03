from xai_components.base import InArg, OutArg, Component, xai_component
import os
from tqdm import tqdm

@xai_component
class PrepareButterflyDataset(Component):

        
    def execute(self, ctx) -> None:

        fn = "leedsbutterfly_dataset_v1.1.zip"


        if not os.path.exists(fn):

            print("Downloading Leeds Butterfly dataset...")

            import requests
            url = 'https://zenodo.org/records/7559420/files/leedsbutterfly_dataset_v1.1.zip?download=1'

            #the server requires a user header to fetch
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

            with requests.get(url, headers=headers, stream=True) as r:
                r.raise_for_status()
                with open(fn, 'wb') as f:
                    pbar = tqdm(total=int(r.headers['Content-Length']))
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            pbar.update(len(chunk))

            print("Leeds dataset successfully downloaded.")

        if not os.path.exists("leedsbutterfly"):

            print("Extracting dataset from zip file...")

            import zipfile
            with zipfile.ZipFile("leedsbutterfly_dataset_v1.1.zip","r") as zip_ref:
                zip_ref.extractall(".")

            print("Leeds dataset successfully extracted.")


        if not os.path.exists("leedsbutterfly/segmentations/butterfly/0010001.png"):

            import shutil

            print("Rearranging dataset for segmentation workflow...")

            paths_to_update = ["leedsbutterfly/segmentations/", "leedsbutterfly/images/"]

            for path in paths_to_update:
                new_path = path + "/butterfly/"
                
                files = os.listdir(path)
                os.mkdir(new_path)

                for file in files:

                    # mask segmentation and original image must have the same filename
                    shutil.move(path + file, new_path + file.replace("_seg0",""))

        print("Leeds butterfly dataset ready!")
        
        if not os.path.exists("leedsbutterfly/images-transformed/train_image"):        
            os.mkdir("leedsbutterfly/images-transformed")
            os.mkdir("leedsbutterfly/segmentations-transformed")
