def train_model(model,
                n_epochs,
                data_yaml_address,
                imgsz=640,
                patience=0,
                device=None,
                batch=16):
    results = model.train(data=data_yaml_address, epochs=n_epochs, imgsz=imgsz, patience=patience,
                          device=device, batch=batch)
    return results