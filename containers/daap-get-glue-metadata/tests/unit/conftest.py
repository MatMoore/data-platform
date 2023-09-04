import sys
import os
from os.path import dirname, join

sys.path.append(join(dirname(__file__), '../', '../', 'src', 'var', 'task'))
sys.path.append(join(dirname(__file__), '../', '../', '../', 'daap-python-base', 'src', 'var', 'task'))

os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"