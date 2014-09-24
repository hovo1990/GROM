
# Spell checker support
try:
    import enchant
except ImportError:
    enchant = None




pre_processing = {r"\binclude\b":(),
                          r"\bdefine\b":(r"\b-DFLEXIBLE\b", r"\b-DPOSRES\b")}

run_control  = {r"\bintegrator\b":(r"\bmd\b", r"\bmd-vv\b",
                                   "\bmd-vv-avek\b", r"\bsd\b",
                                   "\bsd2\b", r"\bbd\b",
                                   r"\bsteep\b", r"\bcg\b","\bl-bfgs\b",
                                   r"\bnm\b","\btpi\b", r"\btpic\b"),
                r"\btinit\b":(),r"\bdt\b":(),r"\bnsteps\b":(),
                r"\binit-step\b":(), r"\bcomm-mode\b":(r"\bLinear\b",
                                                       r"\bAngular\b",
                                                       "\bNone\b"),
                r"\bnstcomm\b":(),r"\bcomm-grps\b":()}

Langevin_dynamics =  {r"\bbd-fric\b":(),r"\bld-seed\b":()}


Energy_minimization = {r"\bemtol\b":(),r"\bemstep\b":(),r"\bnstcgsteep\b":(),
                       r"\bnbfgscorr\b":()}


Shell_Molecular_Dynamics = {r"\bemtol\b":(),r"\bniter\b":(),
                            r"\bfcstep\b":()}


Test_particle_insertion = {r"\brtpi\b":()}


Output_control = {r"\bnstxout\b":(),r"\bnstxtcout\b":(), r"\bnstvout\b":(),r"\bnstfout\b":(),
                    r"\bnstlog\b":(),r"\bnstcalcenergy\b":(),r"\bnstenergy\b":(),
                    r"\bnstxout-compressed\b":(),r"\bcompressed-x-precision\b":(),r"\bcompressed-x-grps\b":(),
                    r"\benergygrps\b":()}


Neighbor_searching =  {r"\bcutoff-scheme\b":(r"\bVerlet\b", r"\bgroup\b"),
                    r"\bnstlist\b":(),r"\bnstcalclr\b":(),
                    r"\bns-type\b":(r"\bgrid\b", r"\bsimple\b"),
                    r"\bns_type\b":(),
                    r"\bpbc\b":(r"\bxyz\b", r"\bno\b", r"\bxy\b"),
                    r"\bperiodic-molecules\b":(r"\bno\b", r"\byes\b"),
                    r"\bverlet-buffer-tolerance\b":(),r"\brlist\b":(),r"\brlistlong\b":()}



Electrostaticselectrostatics = {r"\bcoulombtype\b":(r"\bCut-off\b", r"\bEwald\b", r"\bPME\b",r"\bP3M-AD\b",
                r"\bReaction-Field electrostaticsreaction-field electrostatics\b",
                r"\bGeneralized-Reaction-Field\b",r"\bReaction-Field-zero\b",
                r"\bReaction-Field-nec\b",r"\bShift\b",r"\bEncad-Shift\b",
                r"\bSwitch\b",r"\bUser\b",r"\bPME-Switch\b",
                r"\bPME-User\b",r"\bPME-User-Switch\b"),
                r"\bcoulomb-modifier\b":(r"\bPotential-shift-Verlet\b", r"\bPotential-shift\b", r"\bNone\b"),
                r"\brcoulomb-switch\b":(),r"\brcoulomb\b":(),r"\bepsilon-r\b":(),r"\bepsilon-rf\b":()}



VdW = {r"\bvdw-modifier\b":(r"\bPotential-shift-Verlet\b",
         r"\bPotential-shift\b", r"\bNone\b",r"\bForce-switch\b",
    r"\bPotential-switch\b"),
    r"\brvdw-switch\b":(),
    r"\brvdw\b":(),
    r"\bDispCorr\b":(r"\bno\b"),r"\bEnerPres\b":(),r"\bEner\b":()}

Tables = {r"\btable-extension\b":(),
    r"\benergygrp-table\b":()}

Ewald = {r"\bfourierspacing\b":(),
    r"\bfourier-nx\b":(),
    r"\bfourier_nx\b":(),
    r"\bfourier-ny\b":(),
    r"\bfourier_ny\b":(),
    r"\bfourier-nz\b":(),
    r"\bfourier_nz\b":(),
    r"\bpme-order\b":(),
    r"\bpme_order\b":(),
    r"\bewald-rtol\b":(),
    r"\bewald_rtol\b":(),
    r"\bewald-rtol-lj\b":(),
    r"\bewald_rtol_lj\b":(),
    r"\blj-pme-comb-rule\b":(r"\bGeometric\b", r"\bLorentz-Berthelot\b"),
    r"\bewald-geometry\b":(r"\b3d\b", r"\b3dc\b"),
    r"\boptimize_fft\b":(r"\bno\b", r"\byes\b")}


Temperature_coupling = {r"\btcoupl\b":(r"\bno\b", r"\bBerendsen\b",
                         r"\bNose-Hoover\b", r"\bAndersen\b",
                         r"\bAndersen-Massive\b", r"\bV-rescale\b",r"\bv-rescale\b"),
                        r"\bTcoupl\b":(),
                        r"\bnsttcouple\b":(),
                        r"\bnh-chain-length\b":(),
                        r"\btc-grps\b":(),
                        r"\btc_grps\b":(),
                        r"\btau-t\b":(),
                        r"\btau_t\b":(),
                        r"\bref-t\b":(),r"\bref_t\b":(),r"\bref_t\b":()}

Pressure_coupling = {r"\bpcoupl\b":(r"\bno\b", r"\bberendsen\b",
                         r"\bParrinello-Rahman\b"),
                        r"\bPcoupl\b":(),
                        r"\bMTTK\b":(),
                        r"\bpcoupltype\b":(r"\bisotropic\b", r"\bsemiisotropic\b",
                         r"\banisotropic\b", r"\bsurface-tension\b"),
                        r"\bnstpcouple\b":(),
                        r"\btau-p\b":(),
                        r"\btau_p\b":(),
                        r"\bcompressibility\b":(),
                        r"\bref-p\b":(),
                        r"\bref_p\b":(),
                        r"\brefcoord-scaling\b":(r"\bno\b", r"\ball\b",
                         r"\bcom\b"),
                        r"\brefcoord_scaling\b":(r"\bno\b", r"\ball\b",
                         r"\bcom\b")}

Simulated_annealing = {r"\bannealing\b":(r"\bno\b", r"\bsingle\b",
                         r"\bperiodic\b"),
                        r"\bannealing-npoints\b":(),
                        r"\bannealing-time\b":(),
                        r"\bannealing-temp\b":()}

Velocity_generation =  {r"\bgen_vel\b":(r"\bno\b", r"\byes\b"),
                        r"\bgen-temp\b":(),r"\bgen_temp\b":(),
                        r"\bgen-seed\b":(),r"\bgen_seed\b":()}

Bonds = {r"\bconstraintsconstraint algorithms\b":(r"\bnone\b", r"\bh-bonds\b",
                         r"\ball-bonds\b",r"\bh-angles\b",r"\ball-angles\b"),
                        r"\bconstraint-algorithm\b":(r"\bLINCS\b", r"\blincs\b",
                         r"\bSHAKE\b", r"\bshake\b"),
                        r"\bconstraint_algorithm\b":(r"\byes\b", r"\bno\b"),
                        r"\bconstraints\b":(),
                        r"\bcontinuation\b":(r"\byes\b", r"\bno\b"),
                        r"\bshake-tol\b":(),
                        r"\bshake_tol\b":(),
                        r"\blincs-order\b":(),
                        r"\blincs_order\b":(),
                        r"\blincs-iter\b":(),
                        r"\blincs_iter\b":(),
                        r"\blincs-warnangle\b":(),
                        r"\blincs_warnangle\b":(),
                         r"\bmorse\b":(r"\byes\b", r"\bno\b")}

Energy_exclusions = {r"\benergygrp-excl\b":()}

Wallswalls = {r"\bnwall\b":(),
                r"\bwall-atomtype:\b":(),
                r"\bwall-type\b":(r"\b9-3\b", r"\b10-4\b",r"\b12-6\b",
                                  r"\btable\b"),
                r"\bwall-r-linpot\b":(),
                r"\bwall-density\b":(),
                r"\bwall-ewald-zfac\b":()}

COM_pulling = {r"\bpull\b":(r"\bno\b", r"\bumbrella\b",
                 r"\constraint\b",r"\bconstant-force\b"),
                r"\bpull_geometry\b":(r"\bdistance\b", r"\bdirection\b",
                 r"\bdirection-periodic\b", r"\bcylinder\b"),
                r"\bpull_dim\b":(),
                r"\bpull_r1\b":(),
                r"\bpull_r0\b":(),
                r"\bpull_constr-tol\b":(),
                r"\bpull_start\b":(r"\bno\b", r"\byes\b"),
                 r"\bpull_print-reference\b":(r"\bno\b", r"\byes\b"),
                 r"\bpull_nstxout\b":(),
                 r"\bpull_nstfout\b":(),
                 r"\bpull_ngroups\b":(),
                 r"\bpull_ncoords\b":(),
                 r"\bpull_group1-name\b":(),
                 r"\bpull_group1\b":(),
                 r"\bpull_group0\b":(),
                 r"\bpull_init1\b":(),
                 r"\bpull_rate1\b":(),
                 r"\bpull_k1\b":(),
                 r"\bpull_group1-weights\b":(),
                 r"\bpull_group1-pbcatom\b":(),
                 r"\bpull_coord1-groups\b":(),
                 r"\bpull_coord1-origin\b":(),
                 r"\bpull_coord1-vec\b":(),
                 r"\bpull_coord1-init\b":(),
                 r"\bpull_coord1-rate\b":(),
                 r"\bpull_coord1-k\b":(),
                 r"\bpull_coord1-kB\b":()}

NMR_refinement = {r"\bdisre\b":(r"\bno\b", r"\bsimple\b",
                 r"\ensemble\b"),
                r"\bdisre_weighting\b":(r"\bequal\b", r"\bconservative\b"),
                r"\bdisre_mixed\b":(r"\bno\b",r"\byes\b"),
                r"\bdisre-fc\b":(),
                r"\bdisre_fc\b":(),
                r"\bdisre-tau\b":(),
                r"\bdisre_tau\b":(),
                 r"\borire\b":(r"\bno\b",r"\byes\b"),
                 r"\borire-fc\b":(),
                 r"\borire_fc\b":(),
                 r"\borire-tau\b":(),
                 r"\borire_tau\b":(),
                 r"\borire-fitgrp\b":(),
                 r"\borire_fitgrp\b":(),
                 r"\bnstorireout\b":()}

Free_energy = {r"\free-energy\b":(r"\bno\b", r"\byes\b",
                 r"\expanded\b"),
                r"\bfree_energy\b":(r"\bequal\b", r"\bconservative\b"),
                r"\bdisre-mixed\b":(r"\bno\b",r"\byes\b"),
                r"\bdisre-fc\b":(),
                r"\bdisre_fc\b":(),
                r"\bdisre-tau\b":(),
                r"\bdisre_tau\b":(),
                 r"\borire\b":(r"\bno\b",r"\byes\b"),
                 r"\borire-fc\b":(),
                 r"\borire_fc\b":(),
                 r"\borire-tau\b":(),
                 r"\borire_tau\b":(),
                 r"\borire-fitgrp\b":(),
                 r"\borire_fitgrp\b":(),
                 r"\bnstorireout\b":()}


Total = (pre_processing,run_control,Langevin_dynamics,
         Energy_minimization,Shell_Molecular_Dynamics,
         Test_particle_insertion, Output_control,Neighbor_searching,
         Electrostaticselectrostatics, VdW, Tables,Ewald,
         Temperature_coupling, Pressure_coupling, Simulated_annealing,
         Velocity_generation, Bonds,  Energy_exclusions, Wallswalls,
         COM_pulling, NMR_refinement, Free_energy )



def create_custom_Dict():
    custom_dict = enchant.pypwl.PyPWL()
    for section in Total:
        keys = list(section.keys())
        for i in keys:
            text_key = "%s" %(i[2:-2])
            if len(text_key) > 0:
                custom_dict.add(str(text_key))
            list_is = section[i]
            if len(list_is) > 0:
                for element in list_is:
                    #print('element is ',element)
                    text = "%s" %(element[2:-2])
                    if len(text) > 0:
                        custom_dict.add(str(text))
    return custom_dict


#dictus = create_custom_Dict()
##dictus = enchant.pypwl.PyPWL()
##print('tada ',dictus)
##dictus.add('fuck')
#print(dictus.check('damn'))
#print(dictus.check('distance'))