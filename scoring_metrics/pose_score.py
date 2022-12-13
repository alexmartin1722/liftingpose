
import json

class PoseScore(object):
    """
    Pose scoring between gold and estimate
    """

    def __init__(self, lift, estimate_pose):
        self.lift = lift
        self.gold_poses = self.get_gold()
        self.estimate_pose = self.get_estimate(estimate_pose)
        self._score = None
    
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
        for i in self.gold_poses:
            for j in keypoint_pairs:
                keypoint_annotation_pairs = self.get_keypoints(keypoint_pairs=i, gold_annotation=j)
                keypoint_score_pairs = self.get_keypoint_score(keypoint_annotation_pairs=keypoint_annotation_pairs)
    
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
            return keypoints[0:2]
        elif joint_name == 'left_eye':
            return keypoints[3:5]
        elif joint_name == 'right_eye':
            return keypoints[6:8]
        elif joint_name == 'left_ear':
            return keypoints[9:11]
        elif joint_name == 'right_ear':
            return keypoints[12:14]
        elif joint_name == 'left_shoulder':
            return keypoints[15:17]
        elif joint_name == 'right_shoulder':
            return keypoints[18:20]
        elif joint_name == 'left_elbow':
            return keypoints[21:23]
        elif joint_name == 'right_elbow':
            return keypoints[24:26]
        elif joint_name == 'left_wrist':
            return keypoints[27:29]
        elif joint_name == 'right_wrist':
            return keypoints[30:32]
        elif joint_name == 'left_hip':
            return keypoints[33:35]
        elif joint_name == 'right_hip':
            return keypoints[36:38]
        elif joint_name == 'left_knee':
            return keypoints[39:41]
        elif joint_name == 'right_knee':
            return keypoints[42:44]
        elif joint_name == 'left_ankle':
            return keypoints[45:47]
        elif joint_name == 'right_ankle':
            return keypoints[48:50]
        else:
            raise ValueError('Invalid joint name')

    
    def get_annotations_keypoint(self, gold_keypoints, estimate_keypoints, keypoint_pair):
        joint_one = keypoint_pair[0]
        joint_two = keypoint_pair[1]
        joint_one_annotation = self.get_annotations(joint_name=joint_one['name'], keypoints=estimate_keypoints)
        joint_two_annotation = self.get_annotations(joint_name=joint_two['name'], keypoints=estimate_keypoints)
        joint_one_gold = self.get_annotations(joint_name=joint_one['name'], keypoints=gold_keypoints)
        joint_two_gold = self.get_annotations(joint_name=joint_two['name'], keypoints=gold_keypoints)
        return [(joint_one_gold, joint_two_gold), (joint_one_annotation, joint_two_annotation)]


    def get_keypoints(self, keypoint_pairs, gold_annotation):
        gold_keypoints = gold_annotation['annotations'][0]['keypoints']
        estimate_keypoints = self.estimate_pose['annotations'][0]['keypoints']
        keypoint_annotation_pairs = {}
        for i in keypoint_pairs:
            annotation_pair = self.get_annotations_keypoint(gold_keypoints=gold_keypoints, 
                                                                                estimate_keypoints=estimate_keypoints, keypoint_pair=i)
            keypoint_annotation_pairs[i] = annotation_pair
        return keypoint_annotation_pairs

    def get_keypoint_score(self, keypoint_annotation_pairs):
        """
        Score each keypoint pair
        """
        keypoint_score_pairs = {}
        for i in keypoint_annotation_pairs:
            score = self.get_score(keypoint_annotation_pairs[i])
            keypoint_score_pairs[i] = score
        return keypoint_score_pairs

    def get_distance(self, keypoints):
        """
        Eucledian distance between two keypoints
        """
        joint_one = keypoints[0]
        joint_two = keypoints[1]
        x1 = joint_one[0]
        y1 = joint_one[1]
        x2 = joint_two[0]
        y2 = joint_two[1]
        distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        return distance


    def get_score(self, keypoint_pair):
        """
        Score the ratio of distances between the gold keypoints and estimate keypoints
        """
        gold_pair = keypoint_pair[0]
        estimate_pair = keypoint_pair[1]

        gold_distances = self.get_distance(gold_pair)
        estimate_distances = self.get_distance(estimate_pair)

        score = self.get_score_from_distances(gold_distances=gold_distances, estimate_distances=estimate_distances)
        return score

if __name__ == '__main__':
    scorer = PoseScore(lift_type='bench', estimate_pose='C:\\Users\\amart50\\Desktop\\annotations.json')
    bad_pairs = scorer(keypoint_pairs=[('left_shoulder', 'left_elbow'), ('right_shoulder', 'right_elbow'), 
                    ('right_elbow','left_elbow'), ('right_wrist', 'left_wrist')])
    print('Feedback is needed for:', bad_pairs)