#!/usr/bin/env python

import rospy
import math as m

from std_msgs.msg import String, Bool
from cse_190_final.msg import PolicyList

from qlearn import Qs, QLearner

from read_config import read_config


class Robot():
    def __init__(self):
        """ This will read the config files and set up the different
        listeners and what not
        """
        self.config = read_config()

        self.robotInit()

        rospy.init_node("robot")
        self.start()

    def robotInit(self):
        """ Init Publishers"""
        self.resultsPolicyPub = rospy.Publisher(
                "/results/policy_list",
                PolicyList,
                queue_size = 20
        )
        self.simulationCompletePub = rospy.Publisher(
                "/map_node/sim_complete",
                Bool,
                queue_size = 10
        )

    def beginSimulation(self):
        qlearn = QLearner(self.config)

        while qlearn.renameThis():
            print "Iterate"
            result_policy = qlearn.iterate()
            print "publish"
            self.resultsPolicyPub.publish(result_policy)
            print "Will Continue?", qlearn.renameThis()

        self.simulationCompletePub.publish(True)
        rospy.sleep(10)
        rospy.signal_shutdown("Simulation has Completed")



    def start(self):
        rospy.sleep(5)
        self.beginSimulation()

        rospy.spin()

if __name__ == '__main__':
    rb = Robot()
