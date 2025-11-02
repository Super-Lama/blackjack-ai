from blackjack_env import BlackjackEnv

env = BlackjackEnv

observation, info = env.reset()

print(observation, info)

round_over = False
total_reward = 0

while not round_over:
    action = int(input("Action? "))

    observation, reward, terminated, truncated, info = env.step(action)

    total_reward += reward
    episode_over = terminated or truncated

print(f"Round finished! Total reward: {total_reward}")
env.close()