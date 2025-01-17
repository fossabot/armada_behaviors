cmake_minimum_required(VERSION 3.0.2)
project(armada_flexbe_utilities)

add_compile_options(-std=c++11)

find_package(Eigen3 REQUIRED)

if(NOT EIGEN3_INCLUDE_DIRS)
  set(EIGEN3_INCLUDE_DIRS ${EIGEN3_INCLUDE_DIR})
endif()

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  genmsg
  actionlib_msgs
  std_msgs
  geometry_msgs
  control_msgs
  moveit_core
  moveit_ros_planning
  moveit_ros_planning_interface
  gpd_ros
  tf
  pcl_conversions
  pcl_ros
  message_generation
  robotiq_2f_gripper_control
)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  GraspPoses.msg
  GraspPosesList.msg
)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  GetPointCloud.srv
  ConcatenatePointCloud.srv
  PointCloudPassthroughFilter.srv
  SacSegmentation.srv
  GPDGraspWaypoints.srv
  BasicGraspWaypoints.srv
  GetGraspCandidates.srv
  ConditionalOutlierRemoval.srv
  StatisticalOutlierRemoval.srv
  RadiusOutlierRemoval.srv
  VoxelGridFilter.srv
  EuclideanClusterExtraction.srv
)

## Generate actions in the 'action' folder
add_action_files(
  FILES
  CartesianMove.action
  NamedPoseMove.action
)

## Generate added msg and srv with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  control_msgs
  actionlib_msgs
  gpd_ros
)

catkin_package(
  CATKIN_DEPENDS
  message_runtime
  actionlib_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(move_arm_cpp_server src/actionserver/move_arm_cpp_server.cpp)
add_executable(get_grasp_candidates_service src/service/get_grasp_candidates_service.cpp)
add_executable(gpd_grasp_waypoint_service src/service/gpd_grasp_waypoint_service.cpp)
add_executable(basic_grasp_waypoint_service src/service/basic_grasp_waypoint_service.cpp)
add_executable(get_pointcloud_service src/service/get_pointcloud_service.cpp)
add_executable(pcl_concatenate_pointcloud_service src/service/pcl_concatenate_pointcloud_service.cpp)
add_executable(pcl_passthrough_filter_service src/service/pcl_passthrough_filter_service.cpp)
add_executable(pcl_plane_segmentation_service src/service/pcl_plane_segmentation_service.cpp)
add_executable(pcl_conditional_outlier_removal_service src/service/pcl_conditional_outlier_removal_service.cpp)
add_executable(pcl_radius_outlier_removal_service src/service/pcl_radius_outlier_removal_service.cpp)
add_executable(pcl_statistical_outlier_removal_service src/service/pcl_statistical_outlier_removal_service.cpp)
add_executable(pcl_voxel_grid_filter_service src/service/pcl_voxel_grid_filter_service.cpp)
add_executable(euclidean_cluster_extraction_service src/service/euclidean_cluster_extraction_service.cpp)

target_link_libraries(move_arm_cpp_server ${catkin_LIBRARIES})
target_link_libraries(get_grasp_candidates_service ${catkin_LIBRARIES})
target_link_libraries(gpd_grasp_waypoint_service ${catkin_LIBRARIES})
target_link_libraries(basic_grasp_waypoint_service ${catkin_LIBRARIES})
target_link_libraries(get_pointcloud_service ${catkin_LIBRARIES})
target_link_libraries(pcl_concatenate_pointcloud_service ${catkin_LIBRARIES})
target_link_libraries(pcl_passthrough_filter_service ${catkin_LIBRARIES})
target_link_libraries(pcl_plane_segmentation_service ${catkin_LIBRARIES})
target_link_libraries(pcl_conditional_outlier_removal_service ${catkin_LIBRARIES})
target_link_libraries(pcl_radius_outlier_removal_service ${catkin_LIBRARIES})
target_link_libraries(pcl_statistical_outlier_removal_service ${catkin_LIBRARIES})
target_link_libraries(pcl_voxel_grid_filter_service ${catkin_LIBRARIES})
target_link_libraries(euclidean_cluster_extraction_service ${catkin_LIBRARIES})

add_dependencies(move_arm_cpp_server armada_flexbe_utilities_gencpp)
add_dependencies(get_grasp_candidates_service armada_flexbe_utilities_gencpp)
add_dependencies(gpd_grasp_waypoint_service armada_flexbe_utilities_gencpp)
add_dependencies(basic_grasp_waypoint_service armada_flexbe_utilities_gencpp)
add_dependencies(get_pointcloud_service armada_flexbe_utilities_gencpp)
add_dependencies(pcl_concatenate_pointcloud_service armada_flexbe_utilities_gencpp)
add_dependencies(pcl_passthrough_filter_service armada_flexbe_utilities_gencpp)
add_dependencies(pcl_plane_segmentation_service armada_flexbe_utilities_gencpp)
add_dependencies(pcl_conditional_outlier_removal_service armada_flexbe_utilities_gencpp)
add_dependencies(pcl_radius_outlier_removal_service armada_flexbe_utilities_gencpp)
add_dependencies(pcl_statistical_outlier_removal_service armada_flexbe_utilities_gencpp)
add_dependencies(pcl_voxel_grid_filter_service armada_flexbe_utilities_gencpp)
add_dependencies(euclidean_cluster_extraction_service armada_flexbe_utilities_gencpp)
