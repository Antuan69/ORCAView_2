'''
Configuration file for ORCAView.

This file contains static data used to populate the UI, such as lists of
job types, methods, basis sets, and solvents. Separating this data from the
main application logic makes the code cleaner and easier to maintain.
'''

JOB_TYPES = {
    "Single Point": "SP",
    "Geometry Optimization": "Opt",
    "Frequency Analysis": "Freq",
    "Transition State Search": "OptTS",
    "Composite Methods": "",
    "NEB": "NEB",
    "IRC": "IRC"
}

METHODS = ["DFT", "HF", "Semi-Empirical", "xTB"]

DFT_FUNCTIONALS = {
    "Hybrid": ["B3LYP", "PBE0", "TPSSh", "HSE06", "CAM-B3LYP", "wB97X-D3"],
    "GGA": ["BP86", "PBE", "revPBE", "B97-D3"],
    "Meta-GGA": ["TPSS", "revTPSS", "M06-L", "SCAN"],
    "Double-Hybrid": ["B2PLYP", "DSD-PBEP86-D3"]
}

BASIS_SETS = {
    "Pople": ["6-31G(d)", "6-311G(d,p)", "6-311++G(2d,2p)"],
    "Dunning": ["cc-pVDZ", "aug-cc-pVDZ", "cc-pVTZ", "aug-cc-pVTZ"],
    "Karlsruhe": ["def2-SVP", "def2-TZVP", "def2-QZVP"]
}

SEMIEMPIRICAL_METHODS = {
    "AM1": "AM1",
    "PM3": "PM3",
    "MNDO": "MNDO",
    "OM3": "OM3",
    "PM7": "PM7",
    "GFN2-xTB": "GFN2-xTB"
}

XTB_METHODS = {
    "GFN1-xTB": "GFN1-xTB",
    "GFN2-xTB": "GFN2-xTB"
}

SOLVATION_MODELS = {
    "xTB": ["None", "ALPB", "DDCOSMO", "CPCMX"],
    "Other": ["None", "CPCM", "SMD"]
}

SOLVENTS_BY_MODEL = {
    "None": [],
    "ALPB": [
        "1,4-dioxane", "1-octanol", "acetone", "acetonitrile", "aniline", "benzaldehyde", "benzene", 
        "carbon disulfide", "chloroform", "dichloromethane", "diethyl ether", "n,n-dimethylformamide", 
        "dimethylsulfoxide", "ethanol", "ethyl acetate", "furan", "n-hexadecane", "n-hexane", 
        "methanol", "nitromethane", "octanol(wet)", "phenol", "tetrahydrofuran", "toluene", "water"
    ],
    "ddCOSMO": [
        "1,4-dioxane", "1-octanol", "acetone", "acetonitrile", "aniline", "benzaldehyde", "benzene",
        "carbon disulfide", "chloroform", "conductor", "dichloromethane", "diethyl ether",
        "n,n-dimethylformamide", "dimethylsulfoxide", "ethanol", "ethyl acetate", "furan",
        "n-hexadecane", "n-hexane", "methanol", "nitromethane", "octanol(wet)", "phenol",
        "tetrahydrofuran", "toluene", "water"
    ],
    "CPCMX": [
        "1,2,4-trimethylbenzene", "1,2-dichloroethane", "1-butanol", "1-chlorohexane", "1-decanol", 
        "1-fluorooctane", "1-heptanol", "1-hexanol", "1-iodohexadecane", "1-nonanol", "1-octanol", 
        "1-pentanol", "1-propanol", "2,2,4-trimethylpentane", "2,6-dimethylpyridine", "2-butanol", 
        "2-methoxyethanol", "2-methyl-1-propanol", "2-methylpyridine", "2-propanol", 
        "4-methyl-2-pentanone", "acetic acid", "acetonitrile", "acetophenone", "aniline", "anisole", 
        "benzene", "benzonitrile", "benzyl alcohol", "bromobenzene", "bromoethane", "bromoform", 
        "butanone", "butyl ethanoate", "n-butylbenzene", "sec-butylbenzene", "tert-butylbenzene", 
        "carbon disulfide", "carbon tetrachloride", "chlorobenzene", "chloroform", "m-cresol", 
        "cyclohexane", "cyclohexanone", "decalin", "n-decane", "dibromomethane", "dibutylether", 
        "o-dichlorobenzene", "dichloromethane", "diethyl ether", "diisopropyl ether", 
        "n,n-dimethylacetamide", "n,n-dimethylformamide", "dimethylsulfoxide", "diphenylether", 
        "n-dodecane", "ethanol", "ethyl acetate", "ethyl phenyl ether", "ethylbenzene", 
        "fluorobenzene", "n-heptane", "n-hexadecane", "n-hexane", "iodobenzene", "isopropylbenzene", 
        "p-isopropyltoluene", "mesitylene", "methanol", "n-methylformamide", "nitrobenzene", 
        "nitroethane", "nitromethane", "o-nitrotoluene", "n-nonane", "n-octane", 
        "n-pentadecane", "n-pentane", "perfluorobenzene", "phenol", "pyridine", 
        "tetrachloroethene", "tetrahydrofuran", "tetrahydrothiophene-s,s-dioxide", "tetralin", 
        "toluene", "tributylphosphate", "triethylamine", "n-undecane", "water", "xylene"
    ],
    "CPCM": [
        "1,1,1-trichloroethane", "1,1,2-trichloroethane", "1,2,4-trimethylbenzene",
        "1,2-dibromoethane", "1,2-dichloroethane", "1,2-ethanediol", "1,4-dioxane",
        "1-bromo-2-methylpropane", "1-bromooctane", "1-bromopentane", "1-bromopropane",
        "1-butanol", "1-chlorohexane", "1-chloropentane", "1-chloropropane", "1-decanol",
        "1-fluorooctane", "1-heptanol", "1-hexanol", "1-hexene", "1-hexyne", "1-iodobutane",
        "1-iodohexadecane", "1-iodopentane", "1-iodopropane", "1-nitropropane", "1-nonanol",
        "1-octanol", "1-pentanol", "1-pentene", "1-propanol", "2,2,2-trifluoroethanol",
        "2,2,4-trimethylpentane", "2,4-dimethylpentane", "2,4-dimethylpyridine",
        "2,6-dimethylpyridine", "2-bromopropane", "2-butanol", "2-chlorobutane",
        "2-heptanone", "2-hexanone", "2-methoxyethanol", "2-methyl-1-propanol",
        "2-methyl-2-propanol", "2-methylpentane", "2-methylpyridine", "2-nitropropane",
        "2-octanone", "2-pentanone", "2-propanol", "2-propen-1-ol", "e-2-pentene",
        "3-methylpyridine", "3-pentanone", "4-heptanone", "4-methyl-2-pentanone",
        "4-methylpyridine", "5-nonanone", "acetic acid", "acetone", "acetonitrile",
        "acetophenone", "ammonia", "aniline", "anisole", "benzaldehyde", "benzene",
        "benzonitrile", "benzyl alcohol", "bromobenzene", "bromoethane", "bromoform",
        "butanal", "butanoic acid", "butanone", "butanonitrile", "butyl ethanoate",
        "butylamine", "n-butylbenzene", "sec-butylbenzene", "tert-butylbenzene",
        "carbon disulfide", "carbon tetrachloride", "chlorobenzene", "chloroform",
        "a-chlorotoluene", "o-chlorotoluene", "conductor", "m-cresol", "o-cresol",
        "cyclohexane", "cyclohexanone", "cyclopentane", "cyclopentanol", "cyclopentanone",
        "decalin", "cis-decalin", "n-decane", "dibromomethane", "dibutylether",
        "o-dichlorobenzene", "e-1,2-dichloroethene", "z-1,2-dichloroethene",
        "dichloromethane", "diethyl ether", "diethyl sulfide", "diethylamine",
        "diiodomethane", "diisopropyl ether", "cis-1,2-dimethylcyclohexane",
        "dimethyl disulfide", "n,n-dimethylacetamide", "n,n-dimethylformamide",
        "dimethylsulfoxide", "diphenylether", "dipropylamine", "n-dodecane",
        "ethanethiol", "ethanol", "ethyl acetate", "ethyl methanoate", "ethyl phenyl ether",
        "ethylbenzene", "fluorobenzene", "formamide", "formic acid", "n-heptane",
        "n-hexadecane", "n-hexane", "hexanoic acid", "iodobenzene", "iodoethane",
        "iodomethane", "isopropylbenzene", "p-isopropyltoluene", "mesitylene", "methanol",
        "methyl benzoate", "methyl butanoate", "methyl ethanoate", "methyl methanoate",
        "methyl propanoate", "n-methylaniline", "methylcyclohexane", "n-methylformamide",
        "nitrobenzene", "nitroethane", "nitromethane", "o-nitrotoluene", "n-nonane",
        "n-octane", "n-pentadecane", "pentanal", "n-pentane", "pentanoic acid",
        "pentyl ethanoate", "pentylamine", "perfluorobenzene", "phenol", "propanal",
        "propanoic acid", "propanonitrile", "propyl ethanoate", "propylamine", "pyridine",
        "tetrachloroethene", "tetrahydrofuran", "tetrahydrothiophene-s,s-dioxide",
        "tetralin", "thiophene", "thiophenol", "toluene", "trans-decalin",
        "tributylphosphate", "trichloroethene", "triethylamine", "n-undecane", "water",
        "xylene", "m-xylene", "o-xylene", "p-xylene"
    ],
    "SMD": [
        "1,1,1-trichloroethane", "1,1,2-trichloroethane", "1,2,4-trimethylbenzene",
        "1,2-dibromoethane", "1,2-dichloroethane", "1,2-ethanediol", "1,4-dioxane",
        "1-bromo-2-methylpropane", "1-bromooctane", "1-bromopentane", "1-bromopropane",
        "1-butanol", "1-chlorohexane", "1-chloropentane", "1-chloropropane", "1-decanol",
        "1-fluorooctane", "1-heptanol", "1-hexanol", "1-hexene", "1-hexyne", "1-iodobutane",
        "1-iodohexadecane", "1-iodopentane", "1-iodopropane", "1-nitropropane", "1-nonanol",
        "1-octanol", "1-pentanol", "1-pentene", "1-propanol", "2,2,2-trifluoroethanol",
        "2,2,4-trimethylpentane", "2,4-dimethylpentane", "2,4-dimethylpyridine",
        "2,6-dimethylpyridine", "2-bromopropane", "2-butanol", "2-chlorobutane",
        "2-heptanone", "2-hexanone", "2-methoxyethanol", "2-methyl-1-propanol",
        "2-methyl-2-propanol", "2-methylpentane", "2-methylpyridine", "2-nitropropane",
        "2-octanone", "2-pentanone", "2-propanol", "2-propen-1-ol", "e-2-pentene",
        "3-methylpyridine", "3-pentanone", "4-heptanone", "4-methyl-2-pentanone",
        "4-methylpyridine", "5-nonanone", "acetic acid", "acetone", "acetonitrile",
        "acetophenone", "aniline", "anisole", "benzaldehyde", "benzene",
        "benzonitrile", "benzyl alcohol", "bromobenzene", "bromoethane", "bromoform",
        "butanal", "butanoic acid", "butanone", "butanonitrile", "butyl ethanoate",
        "butylamine", "n-butylbenzene", "sec-butylbenzene", "tert-butylbenzene",
        "carbon disulfide", "carbon tetrachloride", "chlorobenzene", "chloroform",
        "a-chlorotoluene", "o-chlorotoluene", "m-cresol", "o-cresol", "cyclohexane",
        "cyclohexanone", "cyclopentane", "cyclopentanol", "cyclopentanone", "decalin",
        "cis-decalin", "n-decane", "dibromomethane", "dibutylether", "o-dichlorobenzene",
        "e-1,2-dichloroethene", "z-1,2-dichloroethene", "dichloromethane", "diethyl ether",
        "diethyl sulfide", "diethylamine", "diiodomethane", "diisopropyl ether",
        "cis-1,2-dimethylcyclohexane", "dimethyl disulfide", "n,n-dimethylacetamide",
        "n,n-dimethylformamide", "dimethylsulfoxide", "diphenylether", "dipropylamine",
        "n-dodecane", "ethanethiol", "ethanol", "ethyl acetate", "ethyl methanoate",
        "ethyl phenyl ether", "ethylbenzene", "fluorobenzene", "formamide", "formic acid",
        "n-heptane", "n-hexadecane", "n-hexane", "hexanoic acid", "iodobenzene",
        "iodoethane", "iodomethane", "isopropylbenzene", "p-isopropyltoluene", "mesitylene",
        "methanol", "methyl benzoate", "methyl butanoate", "methyl ethanoate",
        "methyl methanoate", "methyl propanoate", "n-methylaniline", "methylcyclohexane",
        "n-methylformamide", "nitrobenzene", "nitroethane", "nitromethane",
        "o-nitrotoluene", "n-nonane", "n-octane", "n-pentadecane", "pentanal",
        "n-pentane", "pentanoic acid", "pentyl ethanoate", "pentylamine", "perfluorobenzene",
        "propanal", "propanoic acid", "propanonitrile", "propyl ethanoate", "propylamine",
        "pyridine", "tetrachloroethene", "tetrahydrofuran",
        "tetrahydrothiophene-s,s-dioxide", "tetralin", "thiophene", "thiophenol",
        "toluene", "trans-decalin", "tributylphosphate", "trichloroethene", "triethylamine",
        "n-undecane", "water", "xylene", "m-xylene", "o-xylene", "p-xylene"
    ],
    "CPCMX": ["Acetonitrile", "DMSO", "H2O", "Methanol", "THF"],
    "DDCOSMO": ["acetone", "acetonitrile", "h2o", "hexane", "methanol", "toluene"]
}
