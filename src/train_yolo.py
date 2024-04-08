from utils.train_utils import train_model, load_yolo


train_parameter_dict = {
    "n_epochs": 10,
    "imgsz": 640,
    "data_yaml_address": '../data/Yolo-2/data.yaml',
    'patience': 0,
    'device': 'mps',
    'batch': 8
}

yolo_address = "../models/yolov8m-seg.pt"

# load a model
model = load_yolo(yolo_address)

# train a model
results = train_model(model,
                      train_parameter_dict["n_epochs"],
                      train_parameter_dict["data_yaml_address"],
                      imgsz=train_parameter_dict["imgsz"],
                      patience=train_parameter_dict["patience"],
                      device=train_parameter_dict['device'],
                      batch=train_parameter_dict['batch'])

print("Results have been saved in:", results.save_dir)




