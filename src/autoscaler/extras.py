import os

from autoscaler.gh import Runner


runner = Runner(os.getenv('PAT', ''))
