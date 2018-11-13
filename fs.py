import os,sys,json
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/DatabaseManager")
sys.path.append(str(os.path.dirname(os.path.realpath(__file__)))+"/Utils")
from Evaluator.visualizer import visual
from shutil import copyfile
arr = {"otb": {"CPU Optimizations": 6.171593669387186, "Vector Optimizations": 15.915673555053983, "totalOverhead": 835.2806072339172, "GPU Optimizations": 77.91273277555884}, "set": {"optimized": [2.633197, 1.7823328971862793, 4.148033], "nonOptimized": [11.11588375, 13.360341, 5.095723], "loopSections": ["69:80", "88:100", "180:242"]}, "lsb": {"GPU Optimizable": 39.64094018108503, "Vector Optimizable": 47.64501773238657, "Not Optimizable": 29.63164902878328, "CPU Optimizable": 18.172126946036038}, "oet": {"optimized": 16.872698967624956, "nonOptimized": 37.881083820438676}}
visual(arr)
if (os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/2MM/optimized_2mm_profile.c")):
    os.remove(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/2MM/optimized_2mm_profile.c")
if (os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/2MM/optimized_dummy.c")):
    os.remove(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/2MM/optimized_dummy.c")
if (os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/2MM/optimization_summary.json")):
    os.remove(os.path.dirname(os.path.realpath(__file__))+"/Sandbox/2MM/optimization_summary.json")
copyfile(os.path.dirname(os.path.realpath(__file__))+"/DependencyManager/failsafe/optimized_2mm_profile.c", os.path.dirname(os.path.realpath(__file__))+"/Sandbox/2MM/optimized_2mm_profile.c")
copyfile(os.path.dirname(os.path.realpath(__file__))+"/DependencyManager/failsafe/optimized_dummy.c", os.path.dirname(os.path.realpath(__file__))+"/Sandbox/2MM/optimized_dummy.c")
copyfile(os.path.dirname(os.path.realpath(__file__))+"/DependencyManager/failsafe/optimization_summary.json", os.path.dirname(os.path.realpath(__file__))+"/Sandbox/2MM/optimization_summary.json")
