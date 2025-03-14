import pytest
import numpy as np

from gym_custom.vector.tests.utils import make_env

from gym_custom.vector.async_vector_env import AsyncVectorEnv
from gym_custom.vector.sync_vector_env import SyncVectorEnv


@pytest.mark.parametrize("shared_memory", [True, False])
def test_vector_env_equal(shared_memory):
    env_fns = [make_env("CubeCrash-v0", i) for i in range(4)]
    num_steps = 100
    try:
        async_env = AsyncVectorEnv(env_fns, shared_memory=shared_memory)
        sync_env = SyncVectorEnv(env_fns)

        async_env.seed(0)
        sync_env.seed(0)

        assert async_env.num_envs == sync_env.num_envs
        assert async_env.observation_space == sync_env.observation_space
        assert async_env.single_observation_space == sync_env.single_observation_space
        assert async_env.action_space == sync_env.action_space
        assert async_env.single_action_space == sync_env.single_action_space

        async_observations = async_env.reset()
        sync_observations = sync_env.reset()
        assert np.all(async_observations == sync_observations)

        for _ in range(num_steps):
            actions = async_env.action_space.sample()
            assert actions in sync_env.action_space

            async_observations, async_rewards, async_dones, _ = async_env.step(actions)
            sync_observations, sync_rewards, sync_dones, _ = sync_env.step(actions)

            assert np.all(async_observations == sync_observations)
            assert np.all(async_rewards == sync_rewards)
            assert np.all(async_dones == sync_dones)

    finally:
        async_env.close()
        sync_env.close()
