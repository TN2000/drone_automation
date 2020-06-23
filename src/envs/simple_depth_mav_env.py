#! /usr/bin/python2
# Atharv Sonwane <atharvs.twm@gmail.com>

from __future__ import print_function

import gym
import rospy

from .. import DepthProcessor, WaypointController
from .mav_env import MavEnv

gym.envs.registration.register(
    id='SimpleDepthMavEnv-v0',
    entry_point='simple_depth_mav_env:SimpleDepthMavEnv',
)

default_launch_file_path = "../launch/iris_depth_warehouse.launch"
MAX_STEPS = 100
ACTION_LOOKUP = {0: "FORWARD", 1: "LEFT", 2: "RIGHT"}


class SimpleDepthMavEnv(MavEnv):
    def __init__(self,
                 launch_file=default_launch_file_path,
                 move_dist=0.2,
                 n_features=3):
        super(SimpleDepthMavEnv, self).__init__(launch_file)

        self.observation_space = gym.spaces.Box(low=0,
                                                high=100,
                                                shape=(n_features, ))
        self.action_space = gym.spaces.Discrete(n=len(ACTION_LOOKUP))

        self.depth_processor = DepthProcessor()
        self.n_features = n_features
        self.move_dist = move_dist

    def _execute_action(self, action):
        if action == 0:
            self.controller.goto_relative(self.move_dist, 0, 0)
        elif action == 1:
            self.controller.goto_relative(0, self.move_dist, 0)
        elif action == 2:
            self.controller.goto_relative(0, self.move_dist, 0)

    def _observe(self):
        return self.depth_processor.obstacle_features

    def _compute_reward(self, obs):
        return sum(obs)

    def _update_done(self):
        return self.steps_taken >= MAX_STEPS