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
    "Local (LDA)": [
        "HFS", "LDA", "LSD", "VWN", "VWN5", "VWN3", "PWLDA"
    ],
    "GGA": [
        "BP86", "BLYP", "OLYP", "GLYP", "XLYP", "PW91", "MPWPW", "MPWLYP", 
        "PBE", "RPBE", "REVPBE", "RPW86PBE", "PWP", "B97-3C"
    ],
    "Meta-GGA": [
        "B97M-V", "B97M-D3BJ", "B97M-D4", "SCANFUNC", "RSCAN", "R2SCAN", 
        "M06L", "TPSS", "REVTPSS", "R2SCAN-3C"
    ],
    "Global Hybrid": [
        "B1LYP", "B3LYP", "B3LYP/G", "O3LYP", "X3LYP", "B1P86", "B3P86", 
        "B3PW91", "PW1PW", "MPW1PW", "MPW1LYP", "PBE0", "REVPBE0", "REVPBE38", 
        "BHANDHLYL", "M06", "M062X", "PW6B95", "TPSSH", "TPSS0", "R2SCANH", 
        "R2SCAN0", "R2SCAN50", "PBEH-3C", "B3LYP-3C"
    ],
    "Range-Separated Hybrid": [
        "WB97", "WB97X", "WB97X-V", "WB97X-D3", "WB97X-D3BJ", "WB97X-D4", 
        "WB97X-D4REV", "CAM-B3LYP", "LC-BLYP", "LC-PBE", "WB97M-V", 
        "WB97M-D3BJ", "WB97M-D4", "WB97M-D4REV", "WR2SCAN", "WB97X-3C"
    ],
    "Global Double-Hybrid": [
        "DSD-BLYP", "DSD-BLYP/2013", "DSD-PBEP86", "DSD-PBEP86/2013", 
        "DSD-PBEB95", "B2PLYP", "mPW2PLYP", "B2GP-PLYP", "B2K-PLYP", 
        "B2T-PLYP", "B2NC-PLYP", "PWPB95", "PBE-QIDH", "PBE0-DH", 
        "REVDSD-PBEP86/2021", "REVDSD-PBEP86-D4/2021", "REVDOD-PBEP86/2021", 
        "REVDOD-PBEP86-D4/2021"
    ],
    "Range-Separated Double-Hybrid": [
        "WB97M(2)", "WB97X-2", "WPR2SCAN50", "RSX-QIDH", "RSX-0DH", "WB2PLYP", 
        "WB2GP-PLYP", "WB88PP86", "WPBEPP86", "SCS/SOS-WB2PLYP", "SCS-WB2GP-PLYP", 
        "SOS-WB2GP-PLYP", "SCS-RSX-QIDH", "SOS-RSX-QIDH", "SCS-WB88PP86", 
        "SOS-WB88PP86", "SCS-WPBEPP86", "SOS-WPBEPP86"
    ]
}

BASIS_SETS = {
    "Pople": [
        "STO-3G", "3-21G", "3-21GSP", "4-22GSP", "6-31G", "6-31G*", "6-31G**", 
        "6-31G(d)", "6-31G(d,p)", "6-31G(2d)", "6-31G(2d,p)", "6-31G(2d,2p)", 
        "6-31G(2df)", "6-31G(2df,2p)", "6-31G(2df,2pd)", "6-31+G*", "6-31+G**", 
        "6-31+G(d)", "6-31+G(d,p)", "6-31+G(2d)", "6-31+G(2d,p)", "6-31+G(2d,2p)", 
        "6-31+G(2df)", "6-31+G(2df,2p)", "6-31+G(2df,2pd)", "6-31++G**", 
        "6-31++G(d,p)", "6-31++G(2d,p)", "6-31++G(2d,2p)", "6-31++G(2df,2p)", 
        "6-31++G(2df,2pd)", "6-311G", "6-311G*", "6-311G**", "6-311G(d)", 
        "6-311G(d,p)", "6-311G(2d)", "6-311G(2d,p)", "6-311G(2d,2p)", 
        "6-311G(2df)", "6-311G(2df,2p)", "6-311G(2df,2pd)", "6-311G(3df)", 
        "6-311G(3df,3pd)", "6-311+G*", "6-311+G**", "6-311+G(d)", "6-311+G(d,p)", 
        "6-311+G(2d)", "6-311+G(2d,p)", "6-311+G(2d,2p)", "6-311+G(2df)", 
        "6-311+G(2df,2p)", "6-311+G(2df,2pd)", "6-311+G(3df)", "6-311+G(3df,2p)", 
        "6-311+G(3df,3pd)", "6-311++G**", "6-311++G(d,p)", "6-311++G(2d,p)", 
        "6-311++G(2d,2p)", "6-311++G(2df,2p)", "6-311++G(2df,2pd)", "6-311++G(3df,3pd)", 
        "m6-31G", "m6-31G*"
    ],
    "Karlsruhe def2": [
        "def2-SVP", "def2-SV(P)", "def2-TZVP", "def2-TZVP(-f)", "def2-TZVPP", 
        "def2-QZVP", "def2-QZVPP", "def2-SVPD", "def2-TZVPD", "def2-TZVPPD", 
        "def2-QZVPD", "def2-QZVPPD", "ma-def2-SVP", "ma-def2-SV(P)", "ma-def2-mSVP", 
        "ma-def2-TZVP", "ma-def2-TZVP(-f)", "ma-def2-TZVPP", "ma-def2-QZVPP"
    ],
    "Correlation-Consistent (Dunning)": [
        "cc-pVDZ", "cc-pVTZ", "cc-pVQZ", "cc-pV5Z", "cc-pV6Z", "aug-cc-pVDZ", 
        "aug-cc-pVTZ", "aug-cc-pVQZ", "aug-cc-pV5Z", "aug-cc-pV6Z", "cc-pVD(+d)Z", 
        "cc-pVT(+d)Z", "cc-pVQ(+d)Z", "cc-pV5(+d)Z", "aug-cc-pVD(+d)Z", 
        "aug-cc-pVT(+d)Z", "aug-cc-pVQ(+d)Z", "aug-cc-pV5(+d)Z", "aug-cc-pV6(+d)Z", 
        "apr-cc-pV(Q+d)Z", "may-cc-pV(T+d)Z", "may-cc-pV(Q+d)Z", "jun-cc-pV(D+d)Z", 
        "jun-cc-pV(T+d)Z", "jun-cc-pV(Q+d)Z", "jul-cc-pV(D+d)Z", "jul-cc-pV(T+d)Z", 
        "jul-cc-pV(Q+d)Z", "maug-cc-pV(D+d)Z", "maug-cc-pV(T+d)Z", "maug-cc-pV(Q+d)Z", 
        "cc-pCVDZ", "cc-pCVTZ", "cc-pCVQZ", "cc-pCV5Z", "cc-pCV6Z", "aug-cc-pCVDZ", 
        "aug-cc-pCVTZ", "aug-cc-pCVQZ", "aug-cc-pCV5Z", "aug-cc-pCV6Z"
    ],
    "Jensen (Polarization-Consistent)": [
        "pc-0", "pc-1", "pc-2", "pc-3", "pc-4", "aug-pc-0", "aug-pc-1", "aug-pc-2", 
        "aug-pc-3", "aug-pc-4", "pcseg-0", "pcseg-1", "pcseg-2", "pcseg-3", "pcseg-4", 
        "aug-pcseg-0", "aug-pcseg-1", "aug-pcseg-2", "aug-pcseg-3", "aug-pcseg-4", 
        "pcSseg-0", "pcSseg-1", "pcSseg-2", "pcSseg-3", "pcSseg-4", "aug-pcSseg-0", 
        "aug-pcSseg-1", "aug-pcSseg-2", "aug-pcSseg-3", "aug-pcSseg-4", "pcJ-0", 
        "pcJ-1", "pcJ-2", "pcJ-3", "pcJ-4", "aug-pcJ-0", "aug-pcJ-1", "aug-pcJ-2", 
        "aug-pcJ-3", "aug-pcJ-4", "pcH-1", "pcH-2", "pcH-3", "pcH-4", "aug-pcH-1", 
        "aug-pcH-2", "aug-pcH-3", "aug-pcH-4", "pcX-1", "pcX-2", "pcX-3", "pcX-4", 
        "aug-pcX-1", "aug-pcX-2", "aug-pcX-3", "aug-pcX-4"
    ],
    "Atomic Natural Orbitals (ANO)": [
        "ANO-SZ", "ANO-pVDZ", "ANO-pVTZ", "ANO-pVQZ", "ANO-pV5Z", "ANO-pV6Z", 
        "aug-ANO-pVDZ", "aug-ANO-pVTZ", "aug-ANO-pVQZ", "aug-ANO-pV5Z", 
        "saug-ANO-pVDZ", "saug-ANO-pVTZ", "saug-ANO-pVQZ", "saug-ANO-pV5Z"
    ],
    "Relativistic (DKH/ZORA)": [
        "DKH-SV(P)", "DKH-SVP", "DKH-TZV(P)", "DKH-TZVP", "DKH-TZVPP", "DKH-QZVP", 
        "DKH-QZVPP", "ZORA-SV(P)", "ZORA-SVP", "ZORA-TZV(P)", "ZORA-TZVP", 
        "ZORA-TZVPP", "ZORA-QZVP", "ZORA-QZVPP", "DKH-def2-SVP", "DKH-def2-SV(P)", 
        "DKH-def2-TZVP", "DKH-def2-TZVP(-f)", "DKH-def2-TZVPP", "DKH-def2-QZVPP", 
        "ZORA-def2-SVP", "ZORA-def2-SV(P)", "ZORA-def2-TZVP", "ZORA-def2-TZVP(-f)", 
        "ZORA-def2-TZVPP", "ZORA-def2-QZVPP", "ma-DKH-def2-SVP", "ma-DKH-def2-SV(P)", 
        "ma-DKH-def2-TZVP", "ma-DKH-def2-TZVP(-f)", "ma-DKH-def2-TZVPP", 
        "ma-DKH-def2-QZVPP", "ma-ZORA-def2-SVP", "ma-ZORA-def2-SV(P)", 
        "ma-ZORA-def2-TZVP", "ma-ZORA-def2-TZVP(-f)", "ma-ZORA-def2-TZVPP", 
        "ma-ZORA-def2-QZVPP"
    ],
    "SARC (Heavy Elements)": [
        "SARC-DKH-SVP", "SARC-DKH-TZVP", "SARC-DKH-TZVPP", "SARC-ZORA-SVP", 
        "SARC-ZORA-TZVP", "SARC-ZORA-TZVPP", "SARC2-DKH-QZV", "SARC2-ZORA-QZV"
    ],
    "Effective Core Potentials": [
        "LANL2MB", "LANL2DZ", "CRENBS", "CRENBL", "SDD", "def2-ECP"
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
