#include "ros/ros.h"
#include "armada_flexbe_utilities/GenGraspWaypoints.h"
#include <tf/transform_listener.h>

/**
 * Generate a list of grasp waypoint sets.
 *
 * Given a list of grasp target candidates, generate a set of waypoint poses (pre-approach, target pose, post-retreat) for each candidate.
 *
 * @param[in] req gpd_ros/GraspConfigList Container of grasp target candidates generated by GPD algorithm.
 * @param[out] res armada_flexbe_utilities/GraspPosesList Container of sets of pose waypoints for grasp target candidates.
 * @return Bool Service completion result.
 */
bool executeCB(armada_flexbe_utilities::GenGraspWaypoints::Request  &req,
         armada_flexbe_utilities::GenGraspWaypoints::Response &res)
{
  // determine size of grasp candidates list for pose waypoint processing
  unsigned long n = req.grasp_msg_list.grasps.size();
  armada_flexbe_utilities::GraspPoses grasp_poses_arr[n];

  for (unsigned long i = 0; i < n; ++i) {
    armada_flexbe_utilities::GraspPoses grasp_poses;

    gpd_ros::GraspConfig grasp_msg = req.grasp_msg_list.grasps[i];
    tf::Matrix3x3 rot_matrix_grasp_base(-grasp_msg.axis.x, grasp_msg.binormal.x, grasp_msg.approach.x,
                                        -grasp_msg.axis.y, grasp_msg.binormal.y, grasp_msg.approach.y,
                                        -grasp_msg.axis.z, grasp_msg.binormal.z, grasp_msg.approach.z);

    tf::Vector3 tr_grasp_base(grasp_msg.position.x, grasp_msg.position.y, grasp_msg.position.z);
    tf::Transform tf_grasp_base(rot_matrix_grasp_base, tr_grasp_base);
    tf::StampedTransform tf_base_odom;

    try {
      tf::TransformListener listener;
      listener.waitForTransform("base_link", "base_link", ros::Time(0), ros::Duration(3.0) );
      listener.lookupTransform("base_link", "base_link", ros::Time(0), tf_base_odom);
    } catch (tf::TransformException err) {
      ROS_ERROR("%s", err.what());
    }
  }

  armada_flexbe_utilities::GraspPosesList grasp_poses_list;
  res.grasp_poses_list = grasp_poses_list;
  return true;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "gen_grasp_waypoints_service");
  ros::NodeHandle nh;

  ros::ServiceServer service = nh.advertiseService("gen_grasp_waypoints", executeCB);
  ROS_INFO("Ready to generate grasping waypoints.");
  ros::spin();

  return 0;
}
