
import json
import math

class PoseScore(object):
    """
    Pose scoring between gold and estimate
    """

    def __init__(self, lift, estimate_pose):
        self.lift = lift
        self.gold_poses = self.get_gold()
        self.estimate_pose = self.get_estimate(estimate_pose)
        self.score = []
    
    def get_estimate(self, estimate_pose):
        est_json = json.load(open(estimate_pose))
        return est_json

    def get_gold(self):
        if self.lift == 'bench':
            # liftingpose\gold_annotations\pose_estimations\bench\gold_bench.json
            gold_json = json.load(open('gold_annotations/pose_estimations/bench/gold_bench.json'))
            return gold_json
        elif self.lift == 'squat':
            # liftingpose\gold_annotations\pose_estimations\squat\gold_squat.json
            gold_json = json.load(open('gold_annotations/pose_estimations/squat/gold_squat.json'))
            return gold_json
        elif self.lift == 'deadlift':
            # liftingpose\gold_annotations\pose_estimations\deadlift\gold_deadlift.json
            gold_json = json.load(open('gold_annotations/pose_estimations/deadlift/gold_deadlift.json'))
            return gold_json
        else:
            raise ValueError('Invalid lift type')
        
    def __call__(self, keypoint_pairs):
        for i in self.gold_poses['annotations']:
            for j in keypoint_pairs:
                keypoint_annotation_pairs = self.get_keypoints(keypoint_pairs=j, gold_annotation=i['keypoints'])
                print(keypoint_annotation_pairs)
                score = self.score_annotation(keypoint_annotation_pairs, i['image_id'], keypoint_pairs=j)
                if score:
                    self.score.append(score)
        return self.score
    
    def score_annotation(self, keypoint_annotation_pairs, image_id, keypoint_pairs):
        gold_annotation = keypoint_annotation_pairs['gold']
        gold_ratio = self.get_ratio(gold_annotation, gold=True, image_id=image_id)

        estimate_annotation = keypoint_annotation_pairs['estimate']
        estimate_ratio = self.get_ratio(estimate_annotation)
        # print(gold_ratio, estimate_ratio, abs(gold_ratio-estimate_ratio))
        if abs(gold_ratio-estimate_ratio) > 0.1:
            print(keypoint_pairs)
            return keypoint_pairs
        else:
            return None

    def get_ratio(self, keypoint_annotation, gold=False, image_id = None):
        annotations = []
        for i in keypoint_annotation:
            annotations.append(keypoint_annotation[i])
        
        height, width = self.get_image_size(image_id=image_id)
        distance = self.get_distance(annotations[0], annotations[1], height, width)
        return distance

    def get_image_size(self, image_id=None):
        if image_id is not None:
            images = self.gold_poses['images']
            for i in images:
                if i['id'] == image_id:
                    height = i['height']
                    width = i['width']
            return height, width
        height = self.estimate_pose['images'][0]['height']
        width = self.estimate_pose['images'][0]['width']
        return height, width

    def get_distance(self, joint_one, joint_two, height, width):
        x1 = joint_one[0]
        y1 = joint_one[1]
        x2 = joint_two[0]
        y2 = joint_two[1]
        distance = (((x2 - x1)/width)**2 + ((y2 - y1)/height)**2)**0.5
        distance = distance
        return distance


    def get_keypoints(self, keypoint_pairs, gold_annotation):
        gold_keypoint_pair_annotations = self.get_keypoint_annotations(keypoint_pairs=keypoint_pairs, gold_annotation=gold_annotation)
        estimate_keypoint_pair_annotations = self.get_user_keypoint_annotations(keypoint_pairs=keypoint_pairs)
        return {'gold':gold_keypoint_pair_annotations, 'estimate':estimate_keypoint_pair_annotations}

    def get_user_keypoint_annotations(self, keypoint_pairs):
        name_annotation = {}
        joint_name_one = keypoint_pairs[0]
        joint_name_two = keypoint_pairs[1]
        joint_one = self.get_annotations(joint_name=joint_name_one, keypoints=self.estimate_pose['annotations'][0]['keypoints'])
        joint_two = self.get_annotations(joint_name=joint_name_two, keypoints=self.estimate_pose['annotations'][0]['keypoints'])
        name_annotation[joint_name_one] = joint_one
        name_annotation[joint_name_two] = joint_two
        return name_annotation

    def get_keypoint_annotations(self, keypoint_pairs, gold_annotation):
        name_annotation = {}
        joint_name_one = keypoint_pairs[0]
        joint_name_two = keypoint_pairs[1]
        joint_one = self.get_annotations(joint_name=joint_name_one, keypoints=gold_annotation)
        joint_two = self.get_annotations(joint_name=joint_name_two, keypoints=gold_annotation)
        name_annotation[joint_name_one] = joint_one
        name_annotation[joint_name_two] = joint_two
        return name_annotation

    def get_annotations(self, joint_name, keypoints):
        """
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
        """
        if joint_name == 'nose':
            return keypoints[0][0:2]
        elif joint_name == 'left_eye':
            return keypoints[1][0:2]
        elif joint_name == 'right_eye':
            return keypoints[2][0:2]
        elif joint_name == 'left_ear':
            return keypoints[3][0:2]
        elif joint_name == 'right_ear':
            return keypoints[4][0:2]
        elif joint_name == 'left_shoulder':
            return keypoints[5][0:2]
        elif joint_name == 'right_shoulder':
            return keypoints[6][0:2]
        elif joint_name == 'left_elbow':
            return keypoints[7][0:2]
        elif joint_name == 'right_elbow':
            return keypoints[8][0:2]
        elif joint_name == 'left_wrist':
            return keypoints[9][0:2]
        elif joint_name == 'right_wrist':
            return keypoints[10][0:2]
        elif joint_name == 'left_hip':
            return keypoints[11][0:2]
        elif joint_name == 'right_hip':
            return keypoints[12][0:2]
        elif joint_name == 'left_knee':
            return keypoints[13][0:2]
        elif joint_name == 'right_knee':
            return keypoints[14][0:2]
        elif joint_name == 'left_ankle':
            return keypoints[15][0:2]
        elif joint_name == 'right_ankle':
            return keypoints[16][0:2]
        else:
            print(joint_name)
            raise ValueError('Invalid joint name')

    
    # def get_annotations_keypoint(self, gold_keypoints, estimate_keypoints, keypoint_pair):
    #     joint_one = keypoint_pair[0]
    #     joint_two = keypoint_pair[1]
    #     joint_one_annotation = self.get_annotations(joint_name=joint_one['name'], keypoints=estimate_keypoints)
    #     joint_two_annotation = self.get_annotations(joint_name=joint_two['name'], keypoints=estimate_keypoints)
    #     joint_one_gold = self.get_annotations(joint_name=joint_one['name'], keypoints=gold_keypoints)
    #     joint_two_gold = self.get_annotations(joint_name=joint_two['name'], keypoints=gold_keypoints)
    #     return [(joint_one_gold, joint_two_gold), (joint_one_annotation, joint_two_annotation)]


    # def get_keypoints(self, keypoint_pairs, gold_annotation):
    #     gold_keypoints = gold_annotation['annotations'][0]['keypoints']
    #     estimate_keypoints = self.estimate_pose['annotations'][0]['keypoints']
    #     keypoint_annotation_pairs = {}
    #     for i in keypoint_pairs:
    #         annotation_pair = self.get_annotations_keypoint(gold_keypoints=gold_keypoints, 
    #                                                                             estimate_keypoints=estimate_keypoints, keypoint_pair=i)
    #         keypoint_annotation_pairs[i] = annotation_pair
    #     return keypoint_annotation_pairs

    # def get_keypoint_score(self, keypoint_annotation_pairs):
    #     """
    #     Score each keypoint pair
    #     """
    #     keypoint_score_pairs = {}
    #     for i in keypoint_annotation_pairs:
    #         score = self.get_score(keypoint_annotation_pairs[i])
    #         keypoint_score_pairs[i] = score
    #     return keypoint_score_pairs

    # def get_distance(self, keypoints):
    #     """
    #     Eucledian distance between two keypoints
    #     """
    #     joint_one = keypoints[0]
    #     joint_two = keypoints[1]
    #     x1 = joint_one[0]
    #     y1 = joint_one[1]
    #     x2 = joint_two[0]
    #     y2 = joint_two[1]
    #     distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    #     return distance


    # def get_score(self, keypoint_pair):
    #     """
    #     Score the ratio of distances between the gold keypoints and estimate keypoints
    #     """
    #     gold_pair = keypoint_pair[0]
    #     estimate_pair = keypoint_pair[1]

    #     gold_distances = self.get_distance(gold_pair)
    #     estimate_distances = self.get_distance(estimate_pair)

    #     score = self.get_score_from_distances(gold_distances=gold_distances, estimate_distances=estimate_distances)
    #     return score

if __name__ == '__main__':
    scorer = PoseScore(lift='bench', estimate_pose='C:\\Users\\amart50\\Desktop\\annotations.json')
    bad_pairs = scorer(keypoint_pairs=[('left_shoulder', 'left_elbow'), ('right_shoulder', 'right_elbow'), 
                    ('right_elbow','left_elbow'), ('right_wrist', 'left_wrist')])
    print('Feedback is needed for:', bad_pairs)