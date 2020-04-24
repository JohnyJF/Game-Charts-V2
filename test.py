import subprocess as cmd

cp = cmd.run("git commit", check=True, shell=True)
cp = cmd.run("git push -u origin master -f", check=True, shell=True)