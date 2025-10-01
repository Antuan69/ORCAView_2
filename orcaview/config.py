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
    "NEB": "NEB",
    "IRC": "IRC",
    "GOAT": "GOAT"
}

METHODS = ["DFT", "HF", "Semiempirical", "xTB"]

DFT_FUNCTIONALS = {
    "LDA": ["Slater/VWN", "LDA", "VWN", "VWN5", "VWN3", "PZ81", "PWLDA"],
    "GGA": [
        "BP86", "PBE", "BLYP", "revPBE", "RPBE", "PW91", "B97-D3", "OLYP",
        "HCTH120", "HCTH147", "HCTH407", "N12", "B88", "PBEX", "PW86", "G96", 
        "mPBE", "rPBE", "HCTH93", "OPTX", "P86", "PBEC", "LYP", "mPWPW"
    ],
    "Meta-GGA": [
        "TPSS", "revTPSS", "SCAN", "rSCAN", "r2SCAN", "M06-L", "M11-L", "MN12-L",
        "MS0", "MS1", "MS2", "TPSS0"
    ],
    "Hybrid": [
        "B3LYP", "PBE0", "TPSSh", "HSE06", "CAM-B3LYP", "wB97X-D3", "B1LYP",
        "O3LYP", "X3LYP", "B97", "B97-1", "B97-2", "B97-3", "mPW1PW", "SCAN0",
        "M06", "M06-2X", "M06-HF", "SOGGA11-X", "LC-BLYP", "wB97", "wB97X", "HSE03"
    ],
    "Double-Hybrid": [
        "B2PLYP", "mPW2-PLYP", "B2GP-PLYP", "DSD-BLYP-D3", "DSD-PBEP86-D3",
        "DSD-PBEB95-D3", "PWPB95-D3", "PTPSS-D3", "revDSD-PBEP86-D4"
    ],
    "Dispersion-Corrected": [
        "PBE-D3(BJ)", "B3LYP-D3", "PBE-D4", "B3LYP-D4", "VV10", "LC-VV10"
    ]
}

BASIS_SETS = {
    "Pople": [
        "STO-3G", "3-21G", "6-31G", "6-31G(d)", "6-31G(d,p)", "6-31+G(d)", 
        "6-31++G(d,p)", "6-311G", "6-311G(d)", "6-311G(d,p)", "6-311+G(d)", 
        "6-311++G(d,p)"
    ],
    "Dunning": [
        "cc-pVDZ", "cc-pVTZ", "cc-pVQZ", "cc-pV5Z", "cc-pV6Z",
        "aug-cc-pVDZ", "aug-cc-pVTZ", "aug-cc-pVQZ", "aug-cc-pV5Z", "aug-cc-pV6Z",
        "d-aug-cc-pVDZ",
        "cc-pCVDZ", "cc-pCVTZ", "cc-pCVQZ", "cc-pCV5Z",
        "aug-cc-pCVDZ", "aug-cc-pCVTZ", "aug-cc-pCVQZ",
        "cc-pwCVDZ", "cc-pwCVTZ", "cc-pwCVQZ",
        "aug-cc-pwCVTZ", "aug-cc-pwCVQZ", "aug-cc-pwCV5Z",
        "cc-pVDZ-DK", "cc-pVTZ-DK", "cc-pVQZ-DK",
        "cc-pVDZ-F12", "cc-pVTZ-F12", "cc-pVQZ-F12"
    ],
    "Karlsruhe/Ahlrichs": [
        "VDZ", "TZV", "TZVP", "QZVP",
        "def2-SVP", "def2-SVPD", "def2-TZVP", "def2-TZVPD", "def2-TZVPP", 
        "def2-TZVPPD", "def2-QZVP", "def2-QZVPD", "def2-QZVPP", "def2-QZVPPD",
        "ma-def2-SVP", "ma-def2-TZVP", "ma-def2-TZVPP", "ma-def2-QZVPP",
        "dhf-SV(P)", "dhf-SVP", "dhf-TZVP", "dhf-TZVPP", "dhf-QZVP", "dhf-QZVPP",
        "dhf-SVP-2c", "dhf-TZVP-2c", "dhf-TZVPP-2c", "dhf-QZVP-2c", "dhf-QZVPP-2c"
    ],
    "Jensen": [
        "pc-0", "pc-1", "pc-2", "pc-3", "pc-4",
        "aug-pc-0", "aug-pc-1", "aug-pc-2", "aug-pc-3", "aug-pc-4",
        "pcS-0", "pcS-1", "pcS-2", "pcS-3", "pcS-4",
        "pcJ-0", "pcJ-1", "pcJ-2", "pcJ-3", "pcJ-4"
    ],
    "Sapporo": [
        "Sapporo-DZP-2012", "Sapporo-TZP-2012", "Sapporo-QZP-2012",
        "Sapporo-DKH3-DZP-2012", "Sapporo-DKH3-TZP-2012", "Sapporo-DKH3-QZP-2012"
    ],
    "ANO": [
        "ANO-SZ", "ANO-pVDZ", "ANO-pVTZ", "ANO-pVQZ", "ANO-pV5Z", "ANO-pV6Z",
        "aug-ANO-pVDZ", "aug-ANO-pVTZ", "aug-ANO-pVQZ", "aug-ANO-pV5Z",
        "saug-ANO-pVDZ", "saug-ANO-pVTZ", "saug-ANO-pVQZ"
    ],
    "ECP": [
        "LANL2MB", "LANL2DZ", "CRENBS", "CRENBL", "SDD"
    ],
    "Relativistic": [
        "SARC-SVP", "SARC-TZVP", "SARC-QZVP",
        "x2c-SVPall", "x2c-TZVPall", "x2c-QZVPall"
    ]
}

SEMIEMPIRICAL_METHODS = {
    "AM1": "AM1",
    "PM3": "PM3",
    "MNDO": "MNDO",
    "ZINDO/1": "ZINDO/1",
    "ZINDO/2": "ZINDO/2",
    "ZINDO/S": "ZINDO/S",
    "ZNDDO/1": "ZNDDO/1",
    "ZNDDO/2": "ZNDDO/2"
}

XTB_METHODS = {
    "GFN0-xTB": "GFN0-xTB",
    "GFN1-xTB": "GFN1-xTB",
    "GFN2-xTB": "GFN2-xTB",
    "GFN-FF": "GFN-FF"
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
