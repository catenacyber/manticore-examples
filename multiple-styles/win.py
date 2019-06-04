#python3 -m cProfile test.py > symbolic_multsty_cprofile.txt
from manticore.native import Manticore
m= Manticore("multiple-styles", env={"LD_LIBRARY_PATH": "/usr/local/lib/linux/"})
m.verbosity(2)

m.context['flag'] = ""

@m.hook(0x400a3b)
def hook(state):
    cpu = state.cpu
    m.context['flag'] += chr(cpu.AL - 10)

@m.hook(0x400a3e)
def hook2(state):
    cpu = state.cpu
    cpu.ZF = True

@m.hook(0x400a40)
def hookf(state):
    print("Failed")
    m.kill()

@m.hook(0x400a6c)
def hooks(state):
    print("Success!")
    print(m.context['flag'])
    m.kill()

m.concrete_data = "12345678" * 2 + "\n"
m.run()

m2 = Manticore('./multiple-styles', env={"LD_LIBRARY_PATH": "/usr/local/lib/linux/"})
m2.context['flag'] = ""

@m2.hook(0x400a6c)
def hook(state):
    cpu = state.cpu
    transform_base = cpu.RBP - 0x50
    for i in range(17):
        solved = state.solve_one(cpu.read_int(transform_base + i, 8))
        print(solved)
        m2.context['flag'] += chr(solved)
    print(m2.context['flag'])
    m2.kill()

m2.run()
