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
        proc = subprocess.Popen(pargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        src,err = proc.communicate()

        if err:
            write_output("Internal FDF execution error")
            raise OSError(err)

        write_output("Model execution complete.")
