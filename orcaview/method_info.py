"""
Information database for DFT functionals, basis sets, and methods.
Contains brief descriptions, applicability, and recommendations.
"""

DFT_FUNCTIONAL_INFO = {
    # Local (LDA)
    "HFS": "Hartree-Fock-Slater exchange-only functional. Historical interest only. Not recommended for production calculations.",
    "LDA": "Local Density Approximation with VWN5 correlation. Simple but inaccurate for most systems. Good for jellium models.",
    "LSD": "Local Spin Density approximation. Same as LDA but for open-shell systems. Limited accuracy.",
    "VWN": "Vosko-Wilk-Nusair correlation functional (parameter set V). Part of many hybrid functionals. Rarely used alone.",
    "VWN5": "VWN parameter set V. Standard choice for LDA correlation. Better than VWN3 for most applications.",
    "VWN3": "VWN parameter set III. Alternative parameterization. Less commonly used than VWN5.",
    "PWLDA": "Perdew-Wang LDA parameterization. Slightly better than VWN for some properties. Still limited accuracy.",
    
    # GGA
    "BP86": "Becke88 exchange + Perdew86 correlation. Good for geometries and frequencies. Tends to overbind.",
    "BLYP": "Becke88 exchange + Lee-Yang-Parr correlation. Popular for organic systems. Good for weak interactions.",
    "OLYP": "Handy's optimal exchange + LYP correlation. Better than BLYP for some properties. Less common.",
    "GLYP": "Gill96 exchange + LYP correlation. Alternative to BLYP. Similar performance characteristics.",
    "XLYP": "Xu-Goddard exchange + LYP correlation. Designed for improved performance. Less tested.",
    "PW91": "Perdew-Wang 91 functional. Predecessor to PBE. Good general-purpose functional.",
    "MPWPW": "Modified PW exchange + PW correlation. Improved over PW91 for some systems.",
    "MPWLYP": "Modified PW exchange + LYP correlation. Combines mPW improvements with LYP correlation.",
    "PBE": "Perdew-Burke-Ernzerhof functional. Very popular, good all-around performance. Excellent for solids.",
    "RPBE": "Revised PBE for improved surface chemistry. Better for adsorption energies than PBE.",
    "REVPBE": "Revised PBE with different gradient correction. Better for some molecular properties.",
    "RPW86PBE": "PBE correlation with refitted PW86 exchange. Specialized for certain applications.",
    "PWP": "PW91 exchange + Perdew86 correlation. Combination of different exchange-correlation parts.",
    "B97-3C": "Composite method by Grimme. Includes dispersion and basis set corrections. Fast and accurate.",
    
    # Meta-GGA
    "B97M-V": "Head-Gordon's meta-GGA with VV10 nonlocal correlation. Excellent for non-covalent interactions.",
    "B97M-D3BJ": "B97M-V modified with D3(BJ) dispersion. Alternative dispersion treatment to VV10.",
    "B97M-D4": "B97M-V with DFT-D4 dispersion correction. Latest dispersion correction method.",
    "SCANFUNC": "Strongly Constrained and Appropriately Normed functional. Satisfies many exact conditions.",
    "RSCAN": "Regularized SCAN. Fixes numerical issues of SCAN while maintaining accuracy.",
    "R2SCAN": "Restored and regularized SCAN. Latest version with improved stability and accuracy.",
    "M06L": "Minnesota M06-L meta-GGA. Good for main group thermochemistry. No exact exchange.",
    "TPSS": "Tao-Perdew-Staroverov-Scuseria meta-GGA. Well-balanced for various properties.",
    "REVTPSS": "Revised TPSS with improved performance. Better than original TPSS for most systems.",
    "R2SCAN-3C": "Composite method based on r²SCAN. Includes corrections for fast, accurate calculations.",
    
    # Global Hybrid
    "B1LYP": "One-parameter hybrid (25% HF exchange). Simple hybrid with good performance.",
    "B3LYP": "Most popular hybrid functional (20% HF exchange). Excellent for organic chemistry.",
    "B3LYP/G": "B3LYP as implemented in Gaussian. Slightly different VWN parameterization.",
    "O3LYP": "Handy's hybrid functional (11.6% HF exchange). Good for some specific applications.",
    "X3LYP": "Xu-Goddard hybrid (21.8% HF exchange). Alternative to B3LYP with similar performance.",
    "PBE0": "PBE-based hybrid (25% HF exchange). Excellent general-purpose functional, good for solids.",
    "REVPBE0": "Hybrid based on revPBE (25% HF exchange). Better for some surface properties.",
    "REVPBE38": "revPBE hybrid with 37.5% HF exchange. Higher HF content for specific applications.",
    "M06": "Minnesota M06 functional (27% HF exchange). Good for main group and transition metals.",
    "M062X": "Minnesota M06-2X (54% HF exchange). Excellent for non-covalent interactions.",
    "TPSSH": "TPSS-based hybrid (10% HF exchange). Conservative hybrid, good for transition metals.",
    "TPSS0": "TPSS hybrid with 25% HF exchange. Better energetics than TPSSh.",
    "R2SCANH": "r²SCAN hybrid (10% HF exchange). Modern meta-GGA hybrid.",
    "R2SCAN0": "r²SCAN hybrid (25% HF exchange). Standard hybrid amount for r²SCAN.",
    "R2SCAN50": "r²SCAN hybrid (50% HF exchange). High HF content for specific applications.",
    
    # Range-Separated Hybrid
    "WB97X": "ωB97X range-separated hybrid. Excellent for non-covalent interactions and charge transfer.",
    "CAM-B3LYP": "Coulomb-attenuated B3LYP. Good for excited states and charge transfer complexes.",
    "LC-BLYP": "Long-range corrected BLYP. Pure long-range HF exchange, good for charge transfer.",
    "LC-PBE": "Long-range corrected PBE. Alternative to LC-BLYP with PBE base.",
    "WB97M-V": "Range-separated meta-GGA with VV10. Excellent accuracy for many properties.",
    "WB97X-D3": "ωB97X with D3 dispersion correction. Combines range separation with dispersion.",
    
    # Double-Hybrid
    "B2PLYP": "First double-hybrid functional. Includes MP2 correlation. Very accurate but expensive.",
    "DSD-BLYP": "Dispersion-corrected spin-component scaled double-hybrid. Excellent for thermochemistry.",
    "REVDSD-PBEP86/2021": "Latest DSD variant. State-of-the-art accuracy for thermochemical properties.",
    "PWPB95": "Double-hybrid with good performance. Alternative to B2PLYP with different base.",
}

BASIS_SET_INFO = {
    # Pople
    "STO-3G": "Minimal basis set. 1 function per orbital. Only for qualitative studies or very large systems.",
    "3-21G": "Split-valence basis set. Inner shell (3 Gaussians), valence (2+1). Better than STO-3G.",
    "6-31G": "Popular split-valence basis. Inner shell (6 Gaussians), valence (3+1). Good starting point.",
    "6-31G(d)": "6-31G with d polarization on heavy atoms. Minimum recommended for most calculations.",
    "6-31G(d,p)": "6-31G(d) with p functions on hydrogen. Standard choice for organic molecules.",
    "6-31+G(d)": "6-31G(d) with diffuse functions on heavy atoms. Better for anions and excited states.",
    "6-31++G(d,p)": "Fully augmented 6-31G(d,p). Good for systems with diffuse electron density.",
    "6-311G(d,p)": "Triple-zeta valence with polarization. More flexible than 6-31G(d,p).",
    "6-311++G(d,p)": "Triple-zeta with diffuse functions. Good balance of accuracy and cost.",
    
    # Karlsruhe def2
    "def2-SVP": "Split-valence polarized. Efficient for large systems. Good geometry optimizations.",
    "def2-SV(P)": "def2-SVP with reduced polarization. Slightly smaller, similar accuracy.",
    "def2-TZVP": "Triple-zeta valence polarized. Excellent general-purpose basis set.",
    "def2-TZVPP": "def2-TZVP with additional polarization. Better for properties and energetics.",
    "def2-QZVP": "Quadruple-zeta valence polarized. High accuracy, expensive. For benchmarking.",
    "def2-SVPD": "def2-SVP with diffuse functions. Better for anions and excited states.",
    "def2-TZVPD": "def2-TZVP with diffuse functions. Excellent for properties requiring diffuse functions.",
    "ma-def2-SVP": "Minimally augmented def2-SVP. Cost-effective improvement over def2-SVP.",
    "ma-def2-TZVP": "Minimally augmented def2-TZVP. Recommended for most accurate calculations.",
    
    # Correlation-Consistent
    "cc-pVDZ": "Correlation-consistent double-zeta. Designed for correlated methods. Systematic improvability.",
    "cc-pVTZ": "Correlation-consistent triple-zeta. Excellent for CCSD(T) and other correlated methods.",
    "cc-pVQZ": "Correlation-consistent quadruple-zeta. High accuracy, expensive. For benchmarking.",
    "aug-cc-pVDZ": "cc-pVDZ with diffuse functions. Essential for anions and Rydberg states.",
    "aug-cc-pVTZ": "cc-pVTZ with diffuse functions. Gold standard for many properties.",
    "aug-cc-pVQZ": "cc-pVQZ with diffuse functions. Benchmark quality, very expensive.",
    "cc-pCVTZ": "Core-valence correlation consistent. Includes core correlation effects.",
    
    # Jensen
    "pc-1": "Polarization-consistent single-zeta. Efficient for large systems.",
    "pc-2": "Polarization-consistent double-zeta. Good balance of accuracy and efficiency.",
    "pc-3": "Polarization-consistent triple-zeta. High accuracy for most applications.",
    "pc-4": "Polarization-consistent quadruple-zeta. Benchmark quality.",
    "aug-pc-2": "pc-2 with diffuse functions. Good for properties requiring diffuse functions.",
    "pcJ-2": "Optimized for NMR spin-spin coupling constants. Specialized for NMR calculations.",
    "pcSseg-2": "Optimized for NMR chemical shifts. Specialized for NMR shielding calculations.",
    
    # ANO
    "ANO-pVDZ": "Atomic natural orbital double-zeta. Very accurate for given size.",
    "ANO-pVTZ": "ANO triple-zeta. Excellent accuracy, but expensive integral evaluation.",
    "ANO-pVQZ": "ANO quadruple-zeta. Benchmark quality, very expensive.",
    "aug-ANO-pVTZ": "ANO-pVTZ with diffuse functions. High accuracy for properties.",
    
    # Relativistic
    "DKH-def2-TZVP": "def2-TZVP recontracted for DKH2 Hamiltonian. For relativistic calculations.",
    "ZORA-def2-TZVP": "def2-TZVP recontracted for ZORA Hamiltonian. Alternative relativistic approach.",
    "SARC-DKH-TZVP": "Segmented all-electron relativistic. For heavy elements with DKH2.",
    "SARC-ZORA-TZVP": "SARC basis for ZORA. For heavy elements with ZORA Hamiltonian.",
}

SEMIEMPIRICAL_INFO = {
    "AM1": "Austin Model 1. Good for organic molecules. Fast calculations. Limited to main group elements.",
    "PM3": "Parametric Method 3. Improved over AM1 for some properties. Widely used for large systems.",
    "MNDO": "Modified Neglect of Diatomic Overlap. Older method. Less accurate than AM1/PM3.",
    "ZINDO/1": "Zerner's INDO method. Good for spectroscopic properties. Specialized applications.",
    "ZINDO/2": "ZINDO variant 2. Different parameterization. Used for specific properties.",
    "ZINDO/S": "ZINDO for spectroscopy. Optimized for electronic spectra calculations.",
}

XTB_INFO = {
    "GFN0-xTB": "Geometry, Frequency, Non-covalent 0. Fastest xTB method. Good for large systems.",
    "GFN1-xTB": "GFN1 extended tight-binding. Balanced accuracy and speed. Good general purpose.",
    "GFN2-xTB": "GFN2 extended tight-binding. Most accurate xTB method. Includes dispersion and halogen bonding.",
    "GFN-FF": "GFN force field. Ultra-fast for very large systems. Limited accuracy.",
}

DISPERSION_INFO = {
    "None": "No dispersion correction applied. Suitable for systems where van der Waals interactions are not important or when using functionals with built-in dispersion (e.g., B97M-V, ωB97M-V).",
    "D2": "Grimme's D2 dispersion correction. Simple pairwise C6/R^6 correction. Less accurate than D3/D4 but computationally cheap. Good for quick estimates.",
    "D3": "Grimme's D3 dispersion correction. Improved over D2 with coordination-number dependent C6 coefficients. Standard choice for many applications. More accurate than D2.",
    "D3BJ": "D3 with Becke-Johnson damping. Often more accurate than standard D3, especially for short-range interactions. Recommended over plain D3 for most functionals.",
    "D3ZERO": "D3 with zero damping function. Alternative damping scheme to BJ damping. Good performance for many systems, especially with specific functionals.",
    "D4": "Latest Grimme dispersion correction. Most accurate dispersion method. Includes charge-dependent coefficients and improved damping. Recommended for high-accuracy calculations.",
    "VV10": "Vydrov-Van Voorhis non-local correlation functional. Built into some functionals (B97M-V, ωB97M-V). Handles both medium and long-range dispersion.",
    "NOVDW": "Explicitly disable all dispersion corrections. Useful when comparing with/without dispersion or when using functionals that already include dispersion effects."
}

METHOD_RECOMMENDATIONS = {
    "Organic Chemistry": "B3LYP/6-31G(d,p) or PBE0/def2-TZVP for higher accuracy",
    "Inorganic Chemistry": "PBE0/def2-TZVP or TPSS/def2-TZVP for transition metals",
    "Non-covalent Interactions": "ωB97X-D3/def2-TZVP or B97M-V/def2-TZVP",
    "Thermochemistry": "revDSD-PBEP86-D4/def2-TZVP or ωB97M-V/def2-TZVP",
    "Excited States": "CAM-B3LYP/aug-cc-pVTZ or ωB97X/aug-cc-pVTZ",
    "Large Systems": "B97-3C or r²SCAN-3C (includes basis set and dispersion)",
    "Benchmark Calculations": "CCSD(T)/aug-cc-pVTZ or revDSD-PBEP86-D4/aug-cc-pVQZ",
}
