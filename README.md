# rosetta_scripts
Standard scripts for Rosetta Modelling, including enzyme design, fast-relax, mutation, packing and minimization, etc.

```
srun python design_protease.py -s /projects/f_sdk94_1/EnzymeModelling/CrystalStructure/TEV/TEV_QS.pdb 
-od /projects/f_sdk94_1/EnzymeModelling/CompleteSilentFiles/TEV_var -name H28L_T30A -seq TENLYFQSGT 
-site 215 -cons tev.cst -cr 39 74 144 -dprot 0 -dpep 0 -mm 21 L -mm 23 A
srun python design_protease.py -s /projects/f_sdk94_1/EnzymeModelling/CrystalStructure/TEV_L2F/TEV_L2F_QS.pdb 
-od /projects/f_sdk94_1/EnzymeModelling/TEVFinalStructures -seq TELTHFQSGT -name L2F_TELTHFQSGT 
-site 215 -cons tev.cst -cr 39 74 144 -dprot 0 -dpep 0
```
