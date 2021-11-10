import sys
import subprocess

def write_output(text, dest=sys.stdout):
    print(text, file=dest)
    dest.flush()


class IntegratedModelRunner():

    def __init__(self, pynsim_config):
        self.pynsim_config = pynsim_config

    def run_subprocess(self):
        fdf, fdfcmd = "fdf", "run"
        modelargs = [ self.pynsim_config ]
        pargs = (fdf, fdfcmd, *modelargs)
        write_output(f"Begin model run using: {pargs=}...")
        proc = subprocess.Popen(pargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = proc.communicate()

        write_output(f"Model execution complete with exit code: {proc.returncode}")
