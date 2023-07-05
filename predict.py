import filepaths
import json
import numpy as np
import preprocess
import subprocess
from tensorflow import keras


MODEL_PATH = filepaths.MODELS_PATH + "\\CNN"
TEMP_DATA_PATH = ".\\TempMusicData"
TEMP_JSON_PATH = ".\\temp_mfccs.json"

LABELS = [
        "Dragonspine",
        "Enkanomiya",
        "Inazuma",
        "Liyue",
        "Mondstadt",
        "Ocean",
        "SumeruDesert",
        "SumeruRainforest"
]

def download_audio(youtube_link):
    try:
        subprocess.check_call(['bash', './youtube_downloader_predict.sh', youtube_link])
    except:
        return False
    return True

def predict():
    # Take the raw audio data and convert it to a format we can use
    preprocess.preprocess(TEMP_DATA_PATH, TEMP_JSON_PATH)

    with open(TEMP_JSON_PATH, "r") as fp:
        data = json.load(fp)
    input_array = np.array(data["mfcc"])
    print(input_array.shape[0])

    # Load model from file
    model = keras.models.load_model(MODEL_PATH)

    # Make predictions from model
    predict_list = []
    for i in range(input_array.shape[0]):
        print("Predicting input number " + str(i))

        input = input_array[i]
        # Add an axis because the CNN expects a 4 dimensional input
        input = input[np.newaxis, ...]

        prediction = model.predict(input)
        predicted_index = np.argmax(prediction, axis=1)
        predict_list.append(LABELS[predicted_index[0]])
        

    return predict_list

if __name__ == "__main__":
    # Prompt user for youtube link
    maybe_link = input("Paste a Youtube link for prediction: ")
    download_succeeded = download_audio(maybe_link)

    if not download_succeeded:
        print("Download failed, not calling model for prediction.")
    else:
        print("Calling the model for prediction.")
        print(predict())