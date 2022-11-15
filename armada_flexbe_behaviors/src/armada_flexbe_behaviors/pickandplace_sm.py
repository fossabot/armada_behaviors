#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from armada_flexbe_states.approach_commander_state import ApproachCommanderState
from armada_flexbe_states.get_pointcloud_service_state import GetPointCloudServiceState
from armada_flexbe_states.gpd_grasp_candidates_service_state import GPDGraspCandidatesServiceState
from armada_flexbe_states.gpd_grasp_waypoints_service_state import GPDGraspWaypointsServiceState
from armada_flexbe_states.gripper_command_action_state import GripperCommandActionState
from armada_flexbe_states.move_arm_action_state import MoveArmActionState
from armada_flexbe_states.pcl_concatenate_pointcloud_service_state import PCLConcatenatePointCloudServiceState
from armada_flexbe_states.pcl_passthrough_filter_service_state import PCLPassthroughFilterServiceState
from armada_flexbe_states.pcl_plane_segmentation_service_state import PCLPlaneSegmentationServiceState
from armada_flexbe_states.pointcloud_publisher_state import PointCloudPublisherState
from armada_flexbe_states.retreat_commander_state import RetreatCommanderState
from armada_flexbe_states.snapshot_commander_state import SnapshotCommanderState
from flexbe_practice_states.step_iterator_state import stepIteratorState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Nov 8 2022
@author: Brian Flynn
'''
class PickAndPlaceSM(Behavior):
	'''
	Perform a pick and place option with a real robot arm and object(s).
	'''


	def __init__(self):
		super(PickAndPlaceSM, self).__init__()
		self.name = 'PickAndPlace'

		# parameters of this behavior
		self.add_parameter('wait_time', 2)
		self.add_parameter('camera_topic', '/camera_wrist/depth_registered/points')
		self.add_parameter('concatenated_cloud_topic', '/combined_cloud')
		self.add_parameter('gripper_topic', '/r2f85_gripper_command')
		self.add_parameter('grasp_candidates_topic', '/detect_grasps/clustered_grasps')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:360 y:665, x:367 y:351
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.wait_pose = ['wait']
		_state_machine.userdata.snapshot_pose_list = ['above','robot_left','robot_right']
		_state_machine.userdata.target_pose = ['']
		_state_machine.userdata.current_snapshot_step = 0
		_state_machine.userdata.pointcloud_list = []
		_state_machine.userdata.combined_pointcloud = 0
		_state_machine.userdata.grasp_candidates = []
		_state_machine.userdata.grasp_waypoints_list = []
		_state_machine.userdata.grasp_attempt = 0
		_state_machine.userdata.grasp_state = 'approach'
		_state_machine.userdata.gripper_state = 'open'
		_state_machine.userdata.gripper_target_position = 0.0
		_state_machine.userdata.gripper_initial_state = 0.0
		_state_machine.userdata.gripper_actual_position = 0.0
		_state_machine.userdata.dropoff_pose = ['dropoff']

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:117 y:485, x:341 y:247
		_sm_solvegraspwaypointscontainer_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['combined_pointcloud', 'grasp_candidates', 'combined_pointcloud_cluster'], output_keys=['grasp_waypoints_list'])

		with _sm_solvegraspwaypointscontainer_0:
			# x:30 y:40
			OperatableStateMachine.add('PublishPointCloud',
										PointCloudPublisherState(topic=self.concatenated_cloud_topic),
										transitions={'continue': 'PublishCluster', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pointcloud': 'combined_pointcloud'})

			# x:15 y:380
			OperatableStateMachine.add('GPDGraspWaypoints',
										GPDGraspWaypointsServiceState(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'grasp_candidates': 'grasp_candidates', 'grasp_waypoints_list': 'grasp_waypoints_list'})

			# x:386 y:134
			OperatableStateMachine.add('PublishCluster',
										PointCloudPublisherState(topic=self.Cluster_cloud),
										transitions={'continue': 'GPDGraspCandidates', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pointcloud': 'combined_pointcloud_cluster'})

			# x:401 y:44
			OperatableStateMachine.add('WaitForNodeRespawn',
										WaitState(wait_time=self.wait_time),
										transitions={'done': 'PublishPointCloud'},
										autonomy={'done': Autonomy.Off})

			# x:28 y:275
			OperatableStateMachine.add('GPDGraspCandidates',
										GPDGraspCandidatesServiceState(combined_cloud_topic=self.concatenated_cloud_topic, grasp_candidates_topic=self.grasp_candidates_topic),
										transitions={'continue': 'GPDGraspWaypoints', 'failed': 'WaitForNodeRespawn'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'combined_pointcloud': 'combined_pointcloud', 'grasp_candidates': 'grasp_candidates'})


		# x:317 y:17, x:420 y:184
		_sm_snapshotcontainer_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['snapshot_pose_list', 'current_snapshot_step', 'pointcloud_list', 'combined_pointcloud'], output_keys=['snapshot_pose_list', 'current_snapshot_step', 'pointcloud_list'])

		with _sm_snapshotcontainer_1:
			# x:30 y:40
			OperatableStateMachine.add('SnapshotCommander',
										SnapshotCommanderState(),
										transitions={'continue': 'finished', 'take_snapshot': 'MoveToSnapshotPose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'take_snapshot': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'snapshot_pose_list': 'snapshot_pose_list', 'current_snapshot_step': 'current_snapshot_step', 'target_pose': 'target_pose'})

			# x:97 y:175
			OperatableStateMachine.add('MoveToSnapshotPose',
										MoveArmActionState(),
										transitions={'finished': 'GetPointCloud', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target_pose_list': 'target_pose'})

			# x:23 y:346
			OperatableStateMachine.add('GetPointCloud',
										GetPointCloudServiceState(camera_topic=self.camera_topic),
										transitions={'continue': 'MoveToSnapshotPose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pointcloud_list': 'pointcloud_list'})


		# x:147 y:320, x:349 y:148
		_sm_retreatcontainer_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['grasp_waypoints_list', 'grasp_attempt'], output_keys=['target_pose_list', 'gripper_target_position'])

		with _sm_retreatcontainer_2:
			# x:77 y:50
			OperatableStateMachine.add('RetreatCommander',
										RetreatCommanderState(),
										transitions={'continue': 'MoveArmRetreat', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'grasp_task_candidates': 'grasp_waypoints_list', 'grasp_attempt': 'grasp_attempt', 'target_pose_list': 'target_pose_list', 'gripper_target_position': 'gripper_target_position'})

			# x:84 y:182
			OperatableStateMachine.add('MoveArmRetreat',
										MoveArmActionState(),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target_pose_list': 'target_pose_list'})


		# x:115 y:405, x:404 y:181
		_sm_pclfiltercontainer_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pointcloud_list', 'combined_pointcloud'], output_keys=['combined_pointcloud', 'pointcloud_list', 'combined_pointcloud_cluster'])

		with _sm_pclfiltercontainer_3:
			# x:31 y:46
			OperatableStateMachine.add('ConcatenatePointCloud',
										PCLConcatenatePointCloudServiceState(),
										transitions={'continue': 'PCLPassthroughFilter', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pointcloud_list_in': 'pointcloud_list', 'combined_pointcloud': 'combined_pointcloud', 'pointcloud_list_out': 'pointcloud_list'})

			# x:42 y:126
			OperatableStateMachine.add('PCLPassthroughFilter',
										PCLPassthroughFilterServiceState(x_min=-1.125, x_max=-0.225, y_min=-0.6, y_max=0.6, z_min=-0.1, z_max=0.15),
										transitions={'continue': 'PCLPlanarSegmentation', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pointcloud_in': 'combined_pointcloud', 'pointcloud_out': 'combined_pointcloud'})

			# x:38 y:200
			OperatableStateMachine.add('PCLPlanarSegmentation',
										PCLPlaneSegmentationServiceState(),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pointcloud_in': 'combined_pointcloud', 'pointcloud_out': 'combined_pointcloud'})


		# x:203 y:421, x:475 y:110
		_sm_approachcontainer_4 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['grasp_waypoints_list', 'gripper_target_position', 'gripper_actual_position', 'gripper_initial_state', 'grasp_attempt', 'gripper_state'], output_keys=['grasp_attempt', 'gripper_actual_position', 'gripper_state'])

		with _sm_approachcontainer_4:
			# x:30 y:40
			OperatableStateMachine.add('ApproachCommander',
										ApproachCommanderState(),
										transitions={'continue': 'MoveArmGrasp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'grasp_task_candidates': 'grasp_waypoints_list', 'grasp_attempt': 'grasp_attempt', 'target_pose_list': 'target_pose_list', 'gripper_target_position': 'gripper_target_position'})

			# x:212 y:116
			OperatableStateMachine.add('GraspStepIterator',
										stepIteratorState(),
										transitions={'continue': 'ApproachCommander', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'iterator_in': 'grasp_attempt', 'iterator_out': 'grasp_attempt'})

			# x:140 y:274
			OperatableStateMachine.add('GripperClose',
										GripperCommandActionState(gripper_topic=self.gripper_topic),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'gripper_target_position': 'gripper_target_position', 'gripper_initial_state': 'gripper_initial_state', 'gripper_actual_position': 'gripper_actual_position', 'gripper_state': 'gripper_state'})

			# x:30 y:176
			OperatableStateMachine.add('MoveArmGrasp',
										MoveArmActionState(),
										transitions={'finished': 'GripperClose', 'failed': 'GraspStepIterator'},
										autonomy={'finished': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target_pose_list': 'target_pose_list'})



		with _state_machine:
			# x:51 y:70
			OperatableStateMachine.add('GripperCommandInit',
										GripperCommandActionState(gripper_topic=self.gripper_topic),
										transitions={'continue': 'MoveArmPreSnapshot', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'gripper_target_position': 'gripper_target_position', 'gripper_initial_state': 'gripper_initial_state', 'gripper_actual_position': 'gripper_actual_position', 'gripper_state': 'gripper_state'})

			# x:540 y:536
			OperatableStateMachine.add('GripperCommandOpen',
										GripperCommandActionState(gripper_topic=self.gripper_topic),
										transitions={'continue': 'WaitForGripperOpen', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'gripper_target_position': 'gripper_target_position', 'gripper_initial_state': 'gripper_initial_state', 'gripper_actual_position': 'gripper_actual_position', 'gripper_state': 'gripper_state'})

			# x:554 y:406
			OperatableStateMachine.add('MoveArmPostGrasp',
										MoveArmActionState(),
										transitions={'finished': 'GripperCommandOpen', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target_pose_list': 'dropoff_pose'})

			# x:548 y:240
			OperatableStateMachine.add('MoveArmPostSnapshot',
										MoveArmActionState(),
										transitions={'finished': 'PCLFilterContainer', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target_pose_list': 'wait_pose'})

			# x:551 y:161
			OperatableStateMachine.add('MoveArmPreSnapshot',
										MoveArmActionState(),
										transitions={'finished': 'SnapshotContainer', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'target_pose_list': 'wait_pose'})

			# x:55 y:233
			OperatableStateMachine.add('PCLFilterContainer',
										_sm_pclfiltercontainer_3,
										transitions={'finished': 'SolveGraspWaypointsContainer', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pointcloud_list': 'pointcloud_list', 'combined_pointcloud': 'combined_pointcloud', 'combined_pointcloud_cluster': 'combined_pointcloud_cluster'})

			# x:61 y:533
			OperatableStateMachine.add('RetreatContainer',
										_sm_retreatcontainer_2,
										transitions={'finished': 'MoveArmPostGrasp', 'failed': 'GripperCommandOpen'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'grasp_waypoints_list': 'grasp_waypoints_list', 'grasp_attempt': 'grasp_attempt', 'target_pose_list': 'target_pose_list', 'gripper_target_position': 'gripper_target_position'})

			# x:57 y:155
			OperatableStateMachine.add('SnapshotContainer',
										_sm_snapshotcontainer_1,
										transitions={'finished': 'MoveArmPostSnapshot', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'snapshot_pose_list': 'snapshot_pose_list', 'current_snapshot_step': 'current_snapshot_step', 'pointcloud_list': 'pointcloud_list', 'combined_pointcloud': 'combined_pointcloud'})

			# x:27 y:340
			OperatableStateMachine.add('SolveGraspWaypointsContainer',
										_sm_solvegraspwaypointscontainer_0,
										transitions={'finished': 'ApproachContainer', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'combined_pointcloud': 'combined_pointcloud', 'grasp_candidates': 'grasp_candidates', 'combined_pointcloud_cluster': 'combined_pointcloud_cluster', 'grasp_waypoints_list': 'grasp_waypoints_list'})

			# x:63 y:625
			OperatableStateMachine.add('WaitForGripperOpen',
										WaitState(wait_time=self.wait_time),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:58 y:437
			OperatableStateMachine.add('ApproachContainer',
										_sm_approachcontainer_4,
										transitions={'finished': 'RetreatContainer', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'grasp_waypoints_list': 'grasp_waypoints_list', 'gripper_target_position': 'gripper_target_position', 'gripper_actual_position': 'gripper_actual_position', 'gripper_initial_state': 'gripper_initial_state', 'grasp_attempt': 'grasp_attempt', 'gripper_state': 'gripper_state'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]