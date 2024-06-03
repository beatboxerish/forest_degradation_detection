import json


def merge_coco_files(list_of_file_names, save_path):
    # reading information on all coco files
    all_files = read_coco_files(list_of_file_names)
    all_images = [i["images"] for i in all_files]
    all_annotations = [i["annotations"] for i in all_files]
    all_categories = [i["categories"] for i in all_files]

    # changing individual annotation id for each file and it's annotations
    all_annotations = change_annotation_id(all_annotations)

    # changing image id for each file and it's images
    all_images, all_annotations = change_image_id(all_images, all_annotations)

    # changing category id for each file and it's annotations
    new_category_dict, new_categories = generate_new_category_dict(all_categories)
    all_annotations = change_category_id(all_annotations, new_category_dict, all_categories)

    # converting everything into a single list
    all_annotations, all_images = convert_to_single_list([all_annotations, all_images])

    # forming new coco_dict
    new_coco_dict = {
        'info': {'description': 'Project'},
        'categories': new_categories,
        'images': all_images,
        'annotations': all_annotations
    }
    save_coco_file(new_coco_dict, save_path)
    return new_coco_dict


def change_annotation_id(list_of_annotations):
    """
    This assumes that annotation IDs are numeric in nature and are unique
    """
    existing_id = []

    new_list_of_annotations = []
    for annotation_list in list_of_annotations:
        new_annotation_list = []
        for annotation in annotation_list:
            if annotation['id'] in existing_id:
                max_id = max(existing_id)
                new_id = max_id +1
                annotation["id"] = new_id
            existing_id.append(annotation['id'])
            new_annotation_list.append(annotation)
        new_list_of_annotations.append(new_annotation_list)
    return new_list_of_annotations


def change_image_id(list_of_images, list_of_annotations):
    """
    """
    existing_id = []

    new_list_of_images = []
    new_list_of_annotations = []
    for file_idx, file_images in enumerate(list_of_images):
        annotation_list = list_of_annotations[file_idx]

        new_images_list = []
        for image_idx, image in enumerate(file_images):
            if image['id'] in existing_id:
                max_id = max(existing_id)
                new_id = max_id +1
                for annotation in annotation_list:
                    if annotation["image_id"] == image['id']:
                        annotation["image_id"] = new_id
                image["id"] = new_id


            existing_id.append(image['id'])
            new_images_list.append(image)
        new_list_of_annotations.append(annotation_list)
        new_list_of_images.append(new_images_list)
    return new_list_of_images, new_list_of_annotations


def generate_new_category_dict(all_categories):
    new_category_dict = dict()
    for category_list in all_categories:
        for category_dict in category_list:
            if category_dict['name'] in new_category_dict.values():
                pass
            else:
                new_id = len(new_category_dict.keys()) + 1
                new_category_dict[new_id] = category_dict['name']

    new_categories = []
    for key, value in new_category_dict.items():
        new_categories.append({'id' :key, 'name' :value})
    return new_category_dict, new_categories


def change_category_id(all_annotations, new_category_dict, all_categories):
    # generating reverse mapper
    reverse_new_category_dict = {j :i for i, j in new_category_dict.items()}
    new_all_annotations = []
    for file_idx, annotation_file in enumerate(all_annotations):
        new_file_annotations = []
        for annotation in annotation_file:
            annotation_category_id = annotation['category_id']
            annotation_category_name = all_categories[file_idx][annotation_category_id-1]["name"]
            new_annotation_category_id = reverse_new_category_dict[annotation_category_name]
            annotation['category_id'] = new_annotation_category_id
            new_file_annotations.append(annotation)
        new_all_annotations.append(new_file_annotations)
    return new_all_annotations


def read_coco_files(list_of_addresses):
    all_files = []
    for file in list_of_addresses:
        all_files.append(read_coco_file(file))
    return all_files


def read_coco_file(coco_file_address):
    open_file = open(coco_file_address)
    coco_file = json.load(open_file)
    return coco_file


def save_coco_file(coco_dict, save_address):
    with open(save_address, 'w') as f:
        json.dump(coco_dict, f)
    return None


def preprocess_labels(coco_files, preprocess_dict):
    label_dict = preprocess_dict['labels']
    if not label_dict:
        return coco_files
    for j, file in enumerate(coco_files):
        coco_files[j] = preprocess_labels_single_coco_file(file, label_dict)
    return coco_files


def preprocess_labels_single_coco_file(coco_file, label_dict):
    old_category_id_to_name = get_cat_id_to_name_dict(coco_file['categories'])

    old_label_to_new_id, new_label_to_new_id = get_id_dict_from_label_dict(label_dict)
    new_category_list = [{"id": v, 'name': k, 'supercategory': k} for k, v in new_label_to_new_id.items()]
    coco_file['categories'] = new_category_list

    new_annotations = []
    for annotation in coco_file['annotations']:
        current_category_id = annotation["category_id"]
        current_category_name = old_category_id_to_name[current_category_id]
        try:
            new_id = old_label_to_new_id[current_category_name]
        except KeyError:
            continue
        annotation['category_id'] = new_id
        new_annotations.append(annotation)
    # rectifying annotation ids
    for annotation_id, annotation in enumerate(new_annotations):
        annotation['id'] = annotation_id + 1
    coco_file['annotations'] = new_annotations
    return coco_file


def get_id_dict_from_label_dict(label_dict):
    label_to_new_id_dict = dict()
    value_id_dict = dict()
    previous_id = 0
    for key, value in label_dict.items():
        if value in value_id_dict.keys():
            label_to_new_id_dict[key] = value_id_dict[value]
        else:
            new_id = previous_id + 1
            label_to_new_id_dict[key] = new_id
            value_id_dict[value] = new_id
            previous_id = new_id
    return label_to_new_id_dict, value_id_dict


def get_cat_id_to_name_dict(category_list):
    return {cat['id'] :cat["name"] for cat in category_list}
