# Copyright (c) OpenMMLab. All rights reserved.
import os
import warnings
from argparse import ArgumentParser

from xtcocotools.coco import COCO

from mmpose.apis import (inference_top_down_pose_model, init_pose_model,
                         vis_pose_result)
from mmpose.datasets import DatasetInfo

import json


def main():
    """Visualize the demo images.

    Require the json_file containing boxes.
    """
    parser = ArgumentParser()
    parser.add_argument('pose_config', help='Config file for detection')
    parser.add_argument('pose_checkpoint', help='Checkpoint file')
    parser.add_argument('--img-root', type=str, default='', help='Image root')
    parser.add_argument(
        '--json-file',
        type=str,
        default='',
        help='Json file containing image info.')
    parser.add_argument(
        '--show',
        action='store_true',
        default=False,
        help='whether to show img')
    parser.add_argument(
        '--out-img-root',
        type=str,
        default='',
        help='Root of the output img file. '
        'Default not saving the visualization images.')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--kpt-thr', type=float, default=0.3, help='Keypoint score threshold')
    parser.add_argument(
        '--radius',
        type=int,
        default=4,
        help='Keypoint radius for visualization')
    parser.add_argument(
        '--thickness',
        type=int,
        default=1,
        help='Link thickness for visualization')

    args = parser.parse_args()

    assert args.show or (args.out_img_root != '')

    coco = COCO(args.json_file)
    # build the pose model from a config file and a checkpoint file
    pose_model = init_pose_model(
        args.pose_config, args.pose_checkpoint, device=args.device.lower())

    dataset = pose_model.cfg.data['test']['type']
    dataset_info = pose_model.cfg.data['test'].get('dataset_info', None)
    if dataset_info is None:
        warnings.warn(
            'Please set `dataset_info` in the config.'
            'Check https://github.com/open-mmlab/mmpose/pull/663 for details.',
            DeprecationWarning)
    else:
        dataset_info = DatasetInfo(dataset_info)

    img_keys = list(coco.imgs.keys())

    # optional
    return_heatmap = False

    # e.g. use ('backbone', ) to return backbone feature
    output_layer_names = None

    json_results = {}
    json_results['info'] = {
        "description": "Lifting data in COCO format",
        "year": 2022,
        "date_created": "2022/12/1"
    }
    json_results['categories'] = [
        {
            "supercategory": "person",
            "id": 1,
            "name": "person",
            "keypoints": [
                "nose",
                "left_eye",
                "right_eye",
                "left_ear",
                "right_ear",
                "left_shoulder",
                "right_shoulder",
                "left_elbow",
                "right_elbow",
                "left_wrist",
                "right_wrist",
                "left_hip",
                "right_hip",
                "left_knee",
                "right_knee",
                "left_ankle",
                "right_ankle"
            ],
            "skeleton": [
                [
                    16,
                    14
                ],
                [
                    14,
                    12
                ],
                [
                    17,
                    15
                ],
                [
                    15,
                    13
                ],
                [
                    12,
                    13
                ],
                [
                    6,
                    12
                ],
                [
                    7,
                    13
                ],
                [
                    6,
                    7
                ],
                [
                    6,
                    8
                ],
                [
                    7,
                    9
                ],
                [
                    8,
                    10
                ],
                [
                    9,
                    11
                ],
                [
                    2,
                    3
                ],
                [
                    1,
                    2
                ],
                [
                    1,
                    3
                ],
                [
                    2,
                    4
                ],
                [
                    3,
                    5
                ],
                [
                    4,
                    6
                ],
                [
                    5,
                    7
                ]
            ]
        }
    ]
    json_results['licenses'] = []
    json_results['images'] = []
    json_results['annotations'] = []
    # process each image
    for i in range(len(img_keys)):
        # get bounding box annotations
        image_id = img_keys[i]
        image = coco.loadImgs(image_id)[0]
        image_name = os.path.join(args.img_root, image['file_name'])
        ann_ids = coco.getAnnIds(image_id)

        # make person bounding boxes
        person_results = []
        for ann_id in ann_ids:
            person = {}
            ann = coco.anns[ann_id]
            # bbox format is 'xywh'
            person['bbox'] = ann['bbox']
            person_results.append(person)

        # test a single image, with a list of bboxes
        pose_results, returned_outputs = inference_top_down_pose_model(
            pose_model,
            image_name,
            person_results,
            bbox_thr=None,
            format='xywh',
            dataset=dataset,
            dataset_info=dataset_info,
            return_heatmap=return_heatmap,
            outputs=output_layer_names)
        # print('pose', pose_results)
        #store annotation into dictionary
        image_dict = {}
        image_dict['id'] = image_id
        image_dict['out_img'] = 'vis_' + str(image_id) + '.jpg'
        image_dict['file_name'] = str(image_id) + '.jpg'
        json_results['images'].append(image_dict)
        annotation_dict = {}
        annotation_dict['id'] = image_id
        annotation_dict['image_id'] = image_id
        annotation_dict['category_id'] = 1
        annotation_dict['keypoints'] = pose_results[0]['keypoints'].tolist()
        #change every 3rd keypoint to .9
        # for i in range(0, len(annotation_dict['keypoints']), 3):
        #     print(i, annotation_dict['keypoints'][i+2])
        #     annotation_dict['keypoints'][i+2] = .9
        annotation_dict['bbox'] = pose_results[0]['bbox'].tolist()
        json_results['annotations'].append(annotation_dict)

        # if image_id == 1 or image_id == 12 or image_id == 53 or image_id == 56 or image_id == 33 or image_id == 24:
        #     image_dict = {}
        #     image_dict['id'] = image_id
        #     image_dict['file_name'] = str(image_id) +'.jpg'
        #     image_dict['width'] = 0
        #     image_dict['height'] = 0
        #     json_results['images'].append(image_dict)
        #     annotation_dict = {}
        #     annotation_dict['id'] = image_id
        #     annotation_dict['image_id'] = image_id
        #     annotation_dict['category_id'] = 1
        #     annotation_dict['keypoints'] = pose_results[0]['keypoints'].tolist()
        #     annotation_dict['bbox'] = pose_results[0]['bbox'].tolist()
        #     json_results['annotations'].append(annotation_dict)
        #     # json_results[image_id] = pose_results[0]
        #     print("ID", image_id)
        #     print(pose_results)
        #     print()
        # if image_id == 10:
        #     keypoints = pose_results[0]['keypoints'].tolist()
        #     for i in keypoints:
        #         print(i, ",")

        


        if args.out_img_root == '':
            out_file = None
        else:
            os.makedirs(args.out_img_root, exist_ok=True)
            out_file = os.path.join(args.out_img_root, f'vis_{image_id}.jpg')

        vis_pose_result(
            pose_model,
            image_name,
            pose_results,
            dataset=dataset,
            dataset_info=dataset_info,
            kpt_score_thr=args.kpt_thr,
            radius=args.radius,
            thickness=args.thickness,
            show=args.show,
            out_file=out_file)
    #write json_results to json file
    with open('C:\\Users\\amart50\\Desktop\\annotations.json', 'w') as f:
        json.dump(json_results, f, indent=4)


if __name__ == '__main__':
    main()
