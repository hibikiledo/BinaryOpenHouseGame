import subprocess
import re

process = subprocess.Popen("ps aux | grep python",
                             shell=True,
                             stdout=subprocess.PIPE,
                           )

processes = process.communicate()[0].split('\n')

for proc in processes:
    tokens = re.split(r'\s+', proc)
    subprocess.check_call(['kill', '-9', tokens[1]])
