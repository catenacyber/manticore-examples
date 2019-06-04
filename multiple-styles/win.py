#python3 -m cProfile test.py > symbolic_multsty_cprofile.txt
from manticore.native import Manticore
m= Manticore("multiple-styles", env={"LD_LIBRARY_PATH": "/usr/local/lib/linux/"})
m.verbosity(2)

@m.hook(0x400a3b)
def hook(state):
    cpu = state.cpu
    with m.locked_context('feature_list', list) as feature_list:
        if len(feature_list) == 0:
           feature_list.append("")
        feature_list[0] += chr(cpu.AL - 10)

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
    with m.locked_context('feature_list', list) as feature_list:
        print(feature_list[0])
    m.kill()

m.concrete_data = "12345678" * 2 + "\n"
m.run()

m2 = Manticore('./multiple-styles', env={"LD_LIBRARY_PATH": "/usr/local/lib/linux/"})

@m2.hook(0x400a6c)
def hook(state):
    cpu = state.cpu
    transform_base = cpu.RBP - 0x50
    flag = ""
    for i in range(17):
        solved = state.solve_one(cpu.read_int(transform_base + i, 8))
        print(solved)
        flag += chr(solved)
    print(flag)
    m2.kill()

m2.run()
