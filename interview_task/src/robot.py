#!/usr/bin/env python3

import random
import rospy
from std_msgs.msg import String


class Robot:
    """Robot class"""

    def __init__(self):
        """Constructor"""
        try:
            # Initialize node, publisher and subscriber
            rospy.init_node('robot')
            self._pub = rospy.Publisher('state', String, queue_size=10)
            self._sub = rospy.Subscriber('action', String, self._callback)

            # Get rate from parameter server
            self._rate = rospy.get_param('~rate', 1)

            # Define headings and obstacle
            self._headings = ["north", "east", "south", "west"]
            self._obstacle = ["true", "false"]

            # Initialize state
            self._state = {
                "heading": random.choice(self._headings),
                "obstacle": random.choice(self._obstacle)
            }

        except Exception as e:
            rospy.logerr(e)

        else:
            rospy.loginfo("{} initialized".format(rospy.get_name()))

    def _callback(self, msg):
        """Callback function for subscriber"""
        rospy.loginfo("{}: Action received from operator: {}".format(
            rospy.get_name(), msg.data))
        self._update_state(msg.data)
        rospy.loginfo("{}: New state: Heading: {}, Obstacle: {}".format(
            rospy.get_name(), self._state["heading"], self._state["obstacle"]))

    def _get_state(self):
        """Get state in string format"""
        return "{} {}".format(self._state["heading"], self._state["obstacle"])

    def _update_state(self, action):
        """Update state"""
        # Update heading based on action
        if action == "continue":
            pass
        elif action == "turn_left":
            heading_index = self._headings.index(self._state["heading"])
            self._state["heading"] = self._headings[(
                heading_index - 1) % len(self._headings)]
        elif action == "turn_right":
            heading_index = self._headings.index(self._state["heading"])
            self._state["heading"] = self._headings[(
                heading_index + 1) % len(self._headings)]
        # Update obstacle randomly
        self._state["obstacle"] = random.choice(self._obstacle)

    def run(self):
        """Run the node"""
        rate = rospy.Rate(self._rate)
        while not rospy.is_shutdown():
            try:
                # Publish state and sleep
                self._pub.publish(self._get_state())
                rate.sleep()

            except rospy.ROSInterruptException:
                rospy.loginfo("Exiting...")


def main():
    """Main function"""
    try:
        # Create and run Robot object
        robot = Robot()
        robot.run()

    except Exception as e:
        # Log error
        rospy.logerr(e)


if __name__ == '__main__':
    main()