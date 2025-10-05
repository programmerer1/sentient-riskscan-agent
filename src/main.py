import os
from sentient_agent_framework.implementation.default_server import DefaultServer
from agent.agent import Agent

if __name__ == "__main__":
    server = DefaultServer(Agent())
    server.run(host=os.getenv("APP_HOST"), port=int(os.getenv("APP_PORT")))
