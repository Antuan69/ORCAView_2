"""
Information database for DFT functionals, basis sets, and methods.
Contains brief descriptions, applicability, and recommendations.
"""

DFT_FUNCTIONAL_INFO = {
    # Local (LDA)
    "HFS": "Hartree-Fock-Slater exchange-only functional. Historical interest only. Severely underestimates binding energies and overestimates bond lengths. No correlation energy included. Only suitable for educational purposes or as a reference point. Not recommended for any production calculations.",
    
    "LDA": "Local Density Approximation with VWN5 correlation. Systematic overbinding (~1 eV per bond) and underestimation of bond lengths (~0.1 Å too short). Good for electron gas systems and some solid-state properties. Fails for molecules with significant correlation effects. Computationally very fast but generally too inaccurate for chemical applications.",
    
    "VWN": "Vosko-Wilk-Nusair correlation functional (parameter set V). Used as correlation component in many hybrid functionals like B3LYP. Provides reasonable correlation for homogeneous electron gas but fails for molecular systems when used alone. Essential component of popular hybrid functionals but not suitable for standalone use.",
    
    "VWN5": "VWN parameter set V - standard choice for LDA correlation. Slightly better than VWN3 for most molecular properties. Still suffers from LDA limitations: overbinding, short bonds, poor barrier heights. Used internally in hybrid functionals. Computational cost is negligible.",
    
    "LSD": "Local Spin Density approximation - spin-polarized version of LDA. Same systematic errors as LDA but handles open-shell systems. Overbinding by ~1 eV per bond, bond lengths 0.1 Å too short. Good for magnetic systems in solid state. Poor for molecular radicals and open-shell organics. Computationally fast but limited accuracy.",
    
    "VWN3": "VWN parameter set III - alternative parameterization. Less commonly used than VWN5. Similar accuracy to VWN5 but slightly different behavior for some properties. Used in some implementations of B3LYP (Gaussian vs others). Computational cost identical to VWN5. Generally superseded by VWN5.",
    
    "PWLDA": "Perdew-Wang LDA parameterization - alternative to VWN correlation. Slightly better than VWN for some solid-state properties. Still suffers from all LDA limitations. Better asymptotic behavior than VWN. Used in some solid-state applications. Not commonly used for molecular systems.",
    
    # GGA
    "BP86": "Becke88 exchange + Perdew86 correlation. Excellent for geometries (±0.02 Å accuracy) and vibrational frequencies. Systematic overbinding by ~0.3 eV per bond. Poor for barrier heights (underestimated by 5-10 kcal/mol). Good for transition metal complexes. Widely used for geometry optimizations despite energetic deficiencies.",
    
    "BLYP": "Becke88 exchange + Lee-Yang-Parr correlation. Popular for organic systems and weak interactions. Better than BP86 for hydrogen bonds and van der Waals complexes. Still overbinds but less than BP86. Poor barrier heights. Excellent for conformational energies. Often used with dispersion corrections (BLYP-D3).",
    
    "OLYP": "Handy's 'optimal' exchange + Lee-Yang-Parr correlation. Designed to improve upon BLYP performance. Better than BLYP for some thermochemical properties. Less overbinding than BLYP. Good for organic molecules. Less commonly used than BLYP. Requires dispersion corrections for non-covalent interactions.",
    
    "GLYP": "Gill's 1996 exchange + Lee-Yang-Parr correlation. Alternative to BLYP with modified exchange. Similar performance to BLYP for most properties. Good for organic systems. Less tested than BLYP. Reasonable for conformational studies. Requires dispersion corrections.",
    
    "XLYP": "Xu-Goddard exchange + Lee-Yang-Parr correlation. Designed for improved performance over BLYP. Better thermochemistry than BLYP for some systems. Less commonly used and tested. Good for organic molecules. May have issues with some transition metal systems. Requires dispersion corrections.",
    
    "PW91": "Perdew-Wang 91 functional - predecessor to PBE. Good general-purpose GGA functional. Systematic overbinding (~0.25 eV per bond). Underestimates barrier heights by ~5 kcal/mol. Good for both molecules and solids. Largely superseded by PBE. Historical importance in DFT development.",
    
    "MPWPW": "Modified Perdew-Wang exchange + Perdew-Wang correlation. Improved over PW91 for some thermochemical properties. Better barrier heights than PW91. Good for main group thermochemistry. Less overbinding than PW91. Not as widely used as PBE. Good alternative to PBE for some applications.",
    
    "MPWLYP": "Modified Perdew-Wang exchange + Lee-Yang-Parr correlation. Combines mPW exchange improvements with LYP correlation benefits. Good for thermochemistry and conformational energies. Better than BLYP for some properties. Requires dispersion corrections. Good for organic systems.",
    
    "RPBE": "Revised PBE - modified exchange enhancement factor. Better for surface chemistry and chemisorption than PBE. Reduces overbinding compared to PBE. Worse for molecular geometries than PBE. Good for gas-surface interactions. Used in surface science applications. Less accurate for molecular thermochemistry.",
    
    "RPW86PBE": "PBE correlation with refitted Perdew86 exchange. Specialized functional for certain applications. Better than PBE for some properties. Less commonly used than standard PBE. Good for systems where PBE exchange is problematic. Limited testing compared to PBE.",
    
    "PWP": "Perdew-Wang 91 exchange + Perdew 86 correlation. Combination of different exchange-correlation components. Historical interest in functional development. Generally superseded by more modern functionals. Limited accuracy compared to newer GGAs. Not recommended for routine use.",
    
    "PBE": "Perdew-Burke-Ernzerhof functional. Excellent general-purpose GGA. Good balance of accuracy for molecules and solids. Systematic overbinding (~0.2 eV per bond). Underestimates barrier heights by ~5 kcal/mol. Excellent for solid-state calculations. Forms basis of popular PBE0 hybrid. Very reliable for geometry optimizations.",
    
    "REVPBE": "Revised PBE with modified exchange enhancement factor. Better for surface chemistry and adsorption energies than PBE. Reduces overbinding compared to PBE. Slightly worse for molecular geometries. Good for gas-surface interactions. Used in some composite methods.",
    
    "B97-3C": "Composite method by Grimme including dispersion (D3) and basis set corrections. Excellent accuracy-to-cost ratio. Good for large systems (>100 atoms). Includes empirical corrections that may not transfer to all systems. Excellent for conformational searches and screening calculations. Not suitable for high-accuracy thermochemistry.",
    
    # Meta-GGA
    "B97M-V": "Head-Gordon's meta-GGA with VV10 nonlocal correlation. Excellent for non-covalent interactions without additional dispersion corrections. Good for thermochemistry and barrier heights. Computationally more expensive than GGAs. Excellent all-around functional for organic chemistry. May struggle with some transition metal systems.",
    
    "B97M-D3BJ": "B97M-V modified with D3(BJ) dispersion correction. Alternative dispersion treatment to built-in VV10. Similar accuracy to B97M-V but with different dispersion approach. Good for systems where VV10 may be problematic. Slightly less expensive than B97M-V. Excellent for non-covalent interactions.",
    
    "B97M-D4": "B97M-V with latest DFT-D4 dispersion correction. Most accurate dispersion treatment available. Excellent for non-covalent interactions and thermochemistry. More expensive than B97M-D3BJ. State-of-the-art accuracy for many properties. Recommended for high-accuracy calculations requiring dispersion.",
    
    "RSCAN": "Regularized SCAN - fixes numerical issues of original SCAN. Better numerical stability than original SCAN while maintaining accuracy. Good for both molecules and solids. More expensive than GGAs. Better than PBE for most molecular properties. Recommended over original SCAN.",
    
    "REVTPSS": "Revised TPSS with improved performance for molecular systems. Better than original TPSS for most molecular properties. Good for transition metals and main group systems. More expensive than GGAs but better accuracy. Reliable for diverse chemical applications. Recommended over original TPSS.",
    
    "SCANFUNC": "Strongly Constrained and Appropriately Normed functional. Satisfies many exact conditions from density functional theory. Good for diverse chemical systems. Can be numerically unstable for some systems. Excellent for solid-state applications. Better than PBE for molecular properties but more expensive.",
    
    "R2SCAN": "Restored and regularized SCAN. Fixes numerical issues of original SCAN while maintaining accuracy. Excellent for both molecules and solids. More expensive than GGAs but very reliable. Good for thermochemistry and barrier heights. Recommended over original SCAN for all applications.",
    
    "M06L": "Minnesota M06-L meta-GGA. Good for main group thermochemistry and kinetics. No exact exchange component. Better barrier heights than GGAs. Can be problematic for transition metals. Good for organic reaction mechanisms. Requires fine integration grids for stability.",
    
    "TPSS": "Tao-Perdew-Staroverov-Scuseria meta-GGA. Well-balanced for various properties. Good for transition metals. Better than GGAs for thermochemistry. More expensive than GGAs. Good compromise between accuracy and cost. Reliable for diverse chemical systems.",
    
    # Global Hybrid
    "B3LYP": "Most popular hybrid functional (20% HF exchange). Excellent for organic chemistry and thermochemistry. Systematic errors: underestimates dispersion, overestimates barrier heights for some reactions. Poor for charge-transfer states. Requires dispersion corrections for non-covalent interactions. Gold standard for organic chemistry despite limitations.",
    
    "PBE0": "PBE-based hybrid (25% HF exchange). More HF exchange than B3LYP leads to better barrier heights. Excellent general-purpose functional for both molecules and solids. Better than B3LYP for inorganic systems. Still requires dispersion corrections. Slightly more expensive than B3LYP due to higher HF exchange percentage.",
    
    "M06": "Minnesota M06 functional (27% HF exchange). Good for main group and transition metals. Better for thermochemistry than B3LYP. Can be numerically unstable. Requires fine integration grids. Good for organometallic systems. May give poor results for some radical systems.",
    
    "M062X": "Minnesota M06-2X (54% HF exchange). Excellent for non-covalent interactions due to high HF exchange. Good for charge-transfer complexes. Can overestimate barrier heights due to high HF content. Poor for transition metals. Excellent for organic host-guest systems and π-π interactions.",
    
    "TPSSH": "TPSS-based hybrid (10% HF exchange). Conservative hybrid good for transition metals. Lower HF exchange reduces self-interaction error gradually. Good for organometallic chemistry. Less accurate than higher-HF hybrids for main group thermochemistry. Reliable for diverse systems.",
    
    # Range-Separated Hybrid
    "WB97X": "ωB97X range-separated hybrid. Excellent for charge-transfer states and non-covalent interactions. Good for excited states calculations. More expensive than global hybrids due to range separation. Excellent for systems with significant charge transfer. May overestimate some barrier heights.",
    
    "CAM-B3LYP": "Coulomb-attenuated B3LYP. Excellent for excited states and charge-transfer complexes. Better than B3LYP for Rydberg states. Good for time-dependent DFT calculations. More expensive than B3LYP. Excellent for photochemistry and electronic spectroscopy applications.",
    
    "LC-BLYP": "Long-range corrected BLYP with 100% long-range HF exchange. Excellent for charge-transfer states and Rydberg excitations. Can overestimate barrier heights significantly. Poor for ground-state thermochemistry. Specialized for excited states and charge-transfer systems only.",
    
    # Double-Hybrid
    "B2PLYP": "First double-hybrid functional including MP2 correlation (27%). Very accurate for thermochemistry when used with large basis sets. Computationally expensive (scales as N^5). Requires large basis sets for convergence. Excellent for benchmark calculations. Not practical for large systems (>50 atoms).",
    
    "DSD-BLYP": "Dispersion-corrected spin-component scaled double-hybrid. Excellent accuracy for thermochemistry and non-covalent interactions. Very expensive computationally. Requires triple-zeta or larger basis sets. Gold standard accuracy for small to medium systems. Includes empirical dispersion corrections.",
    
    "REVDSD-PBEP86/2021": "Latest DSD variant with optimized parameters. State-of-the-art accuracy for thermochemical properties. Extremely expensive (N^5 scaling). Requires very large basis sets (QZ or larger). Benchmark quality results. Only practical for small systems (<30 atoms) with significant computational resources.",
}

BASIS_SET_INFO = {
    # Pople
    "STO-3G": "Minimal basis set with 1 function per orbital. Extremely poor accuracy - bond lengths off by ~0.1 Å, binding energies wrong by >50%. Only suitable for very large systems (>1000 atoms) where accuracy is sacrificed for speed, or educational purposes. Results are qualitatively correct but quantitatively unreliable.",
    
    "3-21G": "Split-valence basis: core (3 Gaussians), valence (2+1 split). Better than STO-3G but still poor accuracy. Bond lengths typically 0.05 Å too long, binding energies underestimated by 20-30%. Suitable for very large systems or preliminary screening. Not recommended for quantitative work.",
    
    "6-31G": "Popular split-valence basis: core (6 Gaussians), valence (3+1). Reasonable geometries (±0.03 Å) but poor energetics. No polarization functions limit accuracy for bonding. Good starting point for geometry optimizations. Requires polarization functions for quantitative results.",
    
    "6-31G(d)": "6-31G with d polarization on heavy atoms. Minimum recommended for most calculations. Good geometries (±0.02 Å) and reasonable energetics. Missing hydrogen polarization affects X-H bonds. Widely used standard for organic molecules. Cost-effective for routine calculations.",
    
    "6-31G(d,p)": "6-31G(d) with p functions on hydrogen. Standard choice for organic molecules. Good balance of accuracy and cost. Geometries accurate to ±0.015 Å. Suitable for most organic chemistry applications. Limitations: poor for anions, excited states, and systems requiring diffuse functions.",
    
    "6-31+G(d)": "6-31G(d) with diffuse functions on heavy atoms. Essential for anions (binding energies improved by 10-20 kcal/mol). Better for excited states and Rydberg states. Increased computational cost (~50% more expensive). Can cause linear dependence issues with large basis sets.",
    
    "6-31++G(d,p)": "Fully augmented 6-31G(d,p) with diffuse functions on all atoms. Excellent for anions, excited states, and systems with diffuse electron density. Significant computational cost increase. Can suffer from numerical instabilities. Gold standard for small molecule anion calculations.",
    
    "6-311G(d,p)": "Triple-zeta valence with polarization. More flexible than 6-31G(d,p) - better energetics and properties. Geometries accurate to ±0.01 Å. Good for thermochemistry. More expensive than 6-31G(d,p) but better accuracy. Excellent compromise for medium-sized systems.",
    
    "6-311++G(d,p)": "Triple-zeta with diffuse functions. High accuracy for most molecular properties. Excellent for anions and excited states. Expensive computationally. Can have linear dependence issues. Recommended for accurate calculations on small to medium systems (<50 atoms).",
    
    # Karlsruhe def2
    "def2-SVP": "Split-valence polarized - efficient for large systems. Optimized for DFT calculations. Good geometries (±0.02 Å) with reasonable computational cost. Smaller than 6-31G(d,p) but similar accuracy. Excellent for geometry optimizations of large systems. Includes ECP for heavy elements automatically.",
    
    "def2-SV(P)": "def2-SVP with reduced polarization functions. Slightly smaller and faster than def2-SVP. Similar accuracy for most properties. Good for very large systems where computational cost is critical. Minimal accuracy loss compared to def2-SVP.",
    
    "def2-TZVP": "Triple-zeta valence polarized. Excellent general-purpose basis set. Good balance of accuracy and cost. Geometries accurate to ±0.01 Å. Suitable for most chemical applications. More accurate than 6-311G(d,p) for energetics. Recommended for production calculations.",
    
    "def2-TZVPP": "def2-TZVP with additional polarization functions. Better for properties requiring high angular momentum. Excellent for NMR calculations and polarizabilities. More expensive than def2-TZVP. Recommended for property calculations and high-accuracy energetics.",
    
    "def2-QZVP": "Quadruple-zeta valence polarized. High accuracy but expensive. Near basis set limit for many properties. Excellent for benchmarking. Only practical for small systems (<30 atoms). Geometries accurate to ±0.005 Å. Used for extrapolation schemes.",
    
    "def2-SVPD": "def2-SVP with diffuse functions. Better for anions and excited states than def2-SVP. Modest computational cost increase. Good compromise for systems requiring diffuse functions. Less prone to linear dependence than Pople augmented sets.",
    
    "def2-TZVPD": "def2-TZVP with diffuse functions. Excellent for properties requiring diffuse functions. High accuracy for anions and excited states. Significant computational cost. Recommended for accurate calculations requiring diffuse character.",
    
    "ma-def2-SVP": "Minimally augmented def2-SVP following Truhlar's scheme. Cost-effective improvement over def2-SVP. Better for anions and excited states. Minimal computational overhead. Good compromise between accuracy and cost for large systems.",
    
    "ma-def2-TZVP": "Minimally augmented def2-TZVP. Excellent accuracy with moderate computational cost. Recommended for most accurate calculations. Good for diverse chemical systems. Better than fully augmented sets for computational efficiency.",
    
    # Correlation-Consistent
    "cc-pVDZ": "Correlation-consistent double-zeta. Designed for systematic improvement and extrapolation. Good for correlated methods (MP2, CCSD). Poor for DFT due to lack of tight functions. Excellent for basis set extrapolation schemes. Smaller than def2-TZVP but designed for post-HF methods.",
    
    "cc-pVTZ": "Correlation-consistent triple-zeta. Excellent for CCSD(T) and other correlated methods. Good balance for post-HF calculations. More expensive than def2-TZVP. Essential for accurate correlated calculations. Designed for systematic convergence to basis set limit.",
    
    "cc-pVQZ": "Correlation-consistent quadruple-zeta. High accuracy for correlated methods. Very expensive computationally. Near basis set limit for most properties. Used for extrapolation and benchmarking. Only practical for small systems with correlated methods.",
    
    "aug-cc-pVDZ": "cc-pVDZ with diffuse functions. Essential for anions with correlated methods. Significant improvement over cc-pVDZ for properties requiring diffuse character. Can have linear dependence issues. Good for systematic studies with extrapolation.",
    
    "aug-cc-pVTZ": "cc-pVTZ with diffuse functions. Gold standard for many correlated calculations. Excellent accuracy for diverse properties. Very expensive computationally. Recommended for benchmark calculations. Excellent for basis set extrapolation schemes.",
    
    "aug-cc-pVQZ": "cc-pVQZ with diffuse functions. Benchmark quality but extremely expensive. Near complete basis set limit. Only for small systems with significant computational resources. Used for high-accuracy reference calculations.",
    
    "cc-pCVTZ": "Core-valence correlation consistent. Includes functions for core-valence correlation. Essential for accurate thermochemistry with correlated methods. More expensive than cc-pVTZ. Required for sub-kcal/mol accuracy in thermochemistry.",
    
    # Jensen
    "pc-1": "Polarization-consistent single-zeta equivalent. Efficient for large systems. Better than minimal basis sets. Good for screening calculations. Limited accuracy but computationally cheap. Suitable for conformational searches of large systems.",
    
    "pc-2": "Polarization-consistent double-zeta. Good balance of accuracy and efficiency. Better organized than Pople sets. Good for routine DFT calculations. More systematic than 6-31G(d,p). Excellent for medium-sized systems.",
    
    "pc-3": "Polarization-consistent triple-zeta. High accuracy for most applications. Well-balanced basis set design. Good for production calculations. More systematic convergence than def2-TZVP. Excellent for diverse chemical systems.",
    
    "pc-4": "Polarization-consistent quadruple-zeta. Benchmark quality results. Very expensive computationally. Near basis set limit for most properties. Used for high-accuracy calculations and extrapolation schemes.",
    
    "aug-pc-2": "pc-2 with diffuse functions. Good for properties requiring diffuse functions. Better organized than Pople augmented sets. Less prone to linear dependence. Good compromise for systems requiring diffuse character.",
    
    "pcJ-2": "Optimized for NMR spin-spin coupling constants. Specialized tight functions for Fermi contact interactions. Essential for accurate J-coupling calculations. Not suitable for general-purpose calculations. Designed specifically for NMR parameter calculations.",
    
    "pcSseg-2": "Optimized for NMR chemical shifts and shieldings. Specialized functions for magnetic shielding calculations. Essential for accurate chemical shift predictions. Not suitable for general calculations. Designed for NMR shielding tensor calculations.",
    
    # ANO
    "ANO-pVDZ": "Atomic natural orbital double-zeta. Very accurate for given size due to general contraction. Expensive integral evaluation. Better accuracy per function than conventional sets. Requires special algorithms. Good for correlated calculations when efficiency is important.",
    
    "ANO-pVTZ": "ANO triple-zeta with excellent accuracy per function. Very expensive integral evaluation but high accuracy. Better than cc-pVTZ for same number of functions. Requires specialized integral algorithms. Excellent for benchmark calculations with correlated methods.",
    
    "ANO-pVQZ": "ANO quadruple-zeta with benchmark quality. Extremely expensive integral evaluation. Near basis set limit accuracy. Only for small systems with significant computational resources. Used for high-accuracy reference calculations.",
    
    "aug-ANO-pVTZ": "ANO-pVTZ with diffuse functions. High accuracy for properties requiring diffuse character. Very expensive computationally. Excellent accuracy per function. Only practical for small systems requiring high accuracy.",
    
    # Relativistic
    "DKH-def2-TZVP": "def2-TZVP recontracted for DKH2 Hamiltonian. Essential for relativistic calculations with DKH2. Maintains def2-TZVP accuracy with relativistic effects. Required for heavy elements (Z>36). More expensive than non-relativistic def2-TZVP due to relativistic integrals.",
    
    "ZORA-def2-TZVP": "def2-TZVP recontracted for ZORA Hamiltonian. Alternative to DKH2 for relativistic effects. Good accuracy for relativistic properties. Computationally efficient relativistic approach. Suitable for systems with heavy elements requiring relativistic treatment.",
    
    "SARC-DKH-TZVP": "Segmented all-electron relativistic contracted for heavy elements. Designed specifically for relativistic calculations. Excellent for transition metals and heavy elements. More expensive than ECP approaches. Provides all-electron treatment of heavy elements.",
    
    "SARC-ZORA-TZVP": "SARC basis for ZORA Hamiltonian. Excellent for heavy element chemistry with ZORA. Good balance of accuracy and computational cost. Suitable for organometallic and heavy element systems. Alternative to ECP methods for heavy elements.",
}

SEMIEMPIRICAL_INFO = {
    "AM1": "Austin Model 1 - improved MNDO parameterization. Good for organic molecules with C, H, N, O. Reasonable geometries (±0.05 Å) and heats of formation (±10 kcal/mol). Fast calculations suitable for large systems (>500 atoms). Limitations: poor for charged species, transition metals, and systems with significant π-conjugation. Overestimates some barrier heights.",
    
    "PM3": "Parametric Method 3 - extensive reparameterization of AM1. Improved over AM1 for heats of formation and geometries. Better for some organics but worse for others. Widely used for large systems and conformational searches. Good for drug-like molecules. Limitations: inconsistent performance, poor for metals, systematic errors for some functional groups.",
    
    "MNDO": "Modified Neglect of Diatomic Overlap - original Dewar semiempirical method. Older method with known systematic errors. Generally less accurate than AM1/PM3 for most properties. Historical importance but superseded by newer methods. Poor for hydrogen bonding and aromatic systems. Not recommended for production use.",
    
    "ZINDO/1": "Zerner's Intermediate Neglect of Differential Overlap. Good for spectroscopic properties and transition metal complexes. Better than AM1/PM3 for d-block elements. Specialized for electronic spectra calculations. Limitations: poor for ground-state thermochemistry, limited parameterization for some elements.",
    
    "ZINDO/2": "ZINDO variant with different parameterization. Alternative parameter set for specific applications. Used for certain spectroscopic properties. Less commonly used than ZINDO/S. Application-specific performance varies significantly.",
    
    "ZINDO/S": "ZINDO optimized for electronic spectroscopy. Excellent for UV-Vis spectra calculations of organic molecules. Good for transition metal complexes. Specialized for excited states and optical properties. Not suitable for ground-state thermochemistry or geometry optimization.",
}

XTB_INFO = {
    "GFN0-xTB": "Geometry, Frequency, Non-covalent 0 - fastest xTB method. Suitable for very large systems (>5000 atoms). Good for quick geometry optimizations and conformational searches. Limited accuracy for energetics. Excellent computational efficiency. Limitations: poor for charged species and transition metals.",
    
    "GFN1-xTB": "GFN1 extended tight-binding with balanced accuracy and speed. Good general-purpose method for large systems (1000-5000 atoms). Reasonable geometries and relative energies. Includes basic dispersion treatment. Good for screening calculations. Better than GFN0 but slower. Suitable for conformational analysis.",
    
    "GFN2-xTB": "Most accurate xTB method with comprehensive parameterization. Includes dispersion, halogen bonding, and hydrogen bonding corrections. Excellent for non-covalent interactions. Good for systems up to 1000 atoms. Best xTB method for quantitative results. Includes anisotropic dispersion and three-body terms.",
    
    "GFN-FF": "GFN force field - ultra-fast for very large systems (>10000 atoms). Machine learning-based force field. Very limited accuracy but extremely fast. Good for molecular dynamics and large-scale screening. Not suitable for quantitative chemistry. Designed for conformational sampling of huge systems.",
}

DISPERSION_INFO = {
    "None": "No dispersion correction applied. Suitable for systems where van der Waals interactions are negligible or when using functionals with built-in dispersion (B97M-V, ωB97M-V). Results in systematic underestimation of binding energies for non-covalent complexes by 2-10 kcal/mol. Good for covalently bonded systems without significant π-π or CH-π interactions.",
    
    "D2": "Grimme's D2 dispersion correction - simple pairwise C6/R^6 approach. Computationally very cheap (~1% overhead). Less accurate than D3/D4 but reasonable for quick estimates. Systematic errors of 1-3 kcal/mol for non-covalent interactions. Good for large systems where computational cost is critical. Limited parameterization for heavy elements.",
    
    "D3": "Grimme's D3 dispersion correction with coordination-number dependent C6 coefficients. Standard choice for many DFT applications. Accuracy typically within 1-2 kcal/mol for non-covalent interactions. Small computational overhead (~2-5%). Excellent parameterization for most elements. Can overestimate dispersion at short distances with some functionals.",
    
    "D3BJ": "D3 with Becke-Johnson damping function. Often more accurate than standard D3, especially for short-range interactions and intramolecular dispersion. Recommended over plain D3 for most functionals. Better behavior at short distances. Excellent for conformational energies. Slightly more expensive than D3 but negligible overhead.",
    
    "D3ZERO": "D3 with zero damping function - alternative to BJ damping. Good performance for many systems, especially with specific functionals like PBE. Different short-range behavior than D3BJ. Functional-dependent performance. Some functionals work better with zero damping than BJ damping. Computational cost identical to D3.",
    
    "D4": "Latest Grimme dispersion correction with charge-dependent C6 coefficients. Most accurate dispersion method currently available. Includes improved damping and three-body terms. Accuracy typically within 0.5-1 kcal/mol for non-covalent interactions. More expensive than D3 (~10% overhead) but still very affordable. Recommended for high-accuracy calculations.",
    
    "VV10": "Vydrov-Van Voorhis non-local correlation functional. Built into some functionals (B97M-V, ωB97M-V) - cannot be used separately. Handles both medium and long-range dispersion self-consistently. More expensive than DFT-D methods (~20-50% overhead). Excellent for non-covalent interactions when properly parameterized within functionals.",
    
    "NOVDW": "Explicitly disable all dispersion corrections. Useful for comparing with/without dispersion effects or when using functionals that already include dispersion (B97M-V, ωB97M-V). Results in systematic underestimation of non-covalent binding energies. Good for studying purely electrostatic or covalent interactions."
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

def evaluate_method_combination(functional, basis_set, dispersion):
    """
    Evaluate the quality and appropriateness of a functional/basis set/dispersion combination.
    Returns a dictionary with evaluation results.
    """
    evaluation = {
        "overall_grade": "C",
        "accuracy_level": "Low",
        "computational_cost": "Medium",
        "recommended_for": [],
        "warnings": [],
        "improvements": [],
        "system_size_limit": "Medium (50-200 atoms)",
        "confidence": "Low"
    }
    
    # Skip evaluation for group separators
    if functional.startswith("--") or basis_set.startswith("--"):
        return None
    
    # Functional quality assessment
    functional_quality = _assess_functional_quality(functional)
    basis_quality = _assess_basis_quality(basis_set)
    dispersion_quality = _assess_dispersion_quality(dispersion, functional)
    
    # Overall grade calculation (weighted average)
    grade_score = (functional_quality["score"] * 0.5 + 
                   basis_quality["score"] * 0.4 + 
                   dispersion_quality["score"] * 0.1)
    
    # Convert score to letter grade
    if grade_score >= 9.0:
        evaluation["overall_grade"] = "A+"
        evaluation["accuracy_level"] = "Benchmark"
        evaluation["confidence"] = "Very High"
    elif grade_score >= 8.5:
        evaluation["overall_grade"] = "A"
        evaluation["accuracy_level"] = "Excellent"
        evaluation["confidence"] = "High"
    elif grade_score >= 7.5:
        evaluation["overall_grade"] = "B+"
        evaluation["accuracy_level"] = "Very Good"
        evaluation["confidence"] = "High"
    elif grade_score >= 6.5:
        evaluation["overall_grade"] = "B"
        evaluation["accuracy_level"] = "Good"
        evaluation["confidence"] = "Medium"
    elif grade_score >= 5.5:
        evaluation["overall_grade"] = "C+"
        evaluation["accuracy_level"] = "Fair"
        evaluation["confidence"] = "Medium"
    elif grade_score >= 4.0:
        evaluation["overall_grade"] = "C"
        evaluation["accuracy_level"] = "Acceptable"
        evaluation["confidence"] = "Low"
    else:
        evaluation["overall_grade"] = "D"
        evaluation["accuracy_level"] = "Poor"
        evaluation["confidence"] = "Very Low"
    
    # Computational cost assessment
    cost_score = (functional_quality["cost"] + basis_quality["cost"]) / 2
    if cost_score <= 2:
        evaluation["computational_cost"] = "Very Low"
        evaluation["system_size_limit"] = "Very Large (>1000 atoms)"
    elif cost_score <= 4:
        evaluation["computational_cost"] = "Low"
        evaluation["system_size_limit"] = "Large (200-1000 atoms)"
    elif cost_score <= 6:
        evaluation["computational_cost"] = "Medium"
        evaluation["system_size_limit"] = "Medium (50-200 atoms)"
    elif cost_score <= 8:
        evaluation["computational_cost"] = "High"
        evaluation["system_size_limit"] = "Small (10-50 atoms)"
    else:
        evaluation["computational_cost"] = "Very High"
        evaluation["system_size_limit"] = "Very Small (<10 atoms)"
    
    # Combine recommendations
    evaluation["recommended_for"] = list(set(
        functional_quality["applications"] + 
        basis_quality["applications"]
    ))
    
    # Combine warnings
    evaluation["warnings"] = (
        functional_quality["warnings"] + 
        basis_quality["warnings"] + 
        dispersion_quality["warnings"]
    )
    
    # Generate improvement suggestions
    evaluation["improvements"] = _generate_improvements(functional, basis_set, dispersion)
    
    return evaluation

def _assess_functional_quality(functional):
    """Assess the quality of a DFT functional."""
    # High-quality functionals (score 8-10)
    high_quality = {
        "B3LYP": {"score": 8.5, "cost": 4, "applications": ["Organic Chemistry", "Thermochemistry"], 
                  "warnings": ["Requires dispersion correction", "Poor for charge-transfer"]},
        "PBE0": {"score": 8.7, "cost": 5, "applications": ["General Purpose", "Inorganic Chemistry"], 
                 "warnings": ["Requires dispersion correction"]},
        "B97M-V": {"score": 9.0, "cost": 6, "applications": ["Non-covalent Interactions", "Thermochemistry"], 
                   "warnings": ["May struggle with transition metals"]},
        "WB97X-D4": {"score": 9.2, "cost": 7, "applications": ["Non-covalent Interactions", "Charge Transfer"], 
                     "warnings": ["Expensive for large systems"]},
        "WB97X": {"score": 8.9, "cost": 7, "applications": ["Charge Transfer", "Excited States"], 
                  "warnings": ["More expensive than global hybrids"]},
        "CAM-B3LYP": {"score": 8.6, "cost": 6, "applications": ["Excited States", "Photochemistry"], 
                      "warnings": ["More expensive than B3LYP"]},
        "R2SCAN": {"score": 8.8, "cost": 6, "applications": ["General Purpose", "Solid State"], 
                   "warnings": ["More expensive than GGAs"]},
        "REVDSD-PBEP86/2021": {"score": 9.8, "cost": 10, "applications": ["Benchmark Calculations"], 
                               "warnings": ["Extremely expensive", "Only for small systems"]},
        "B2PLYP": {"score": 9.3, "cost": 9, "applications": ["Benchmark", "Thermochemistry"], 
                   "warnings": ["Very expensive", "Requires large basis sets"]},
        "M062X": {"score": 8.4, "cost": 6, "applications": ["Non-covalent Interactions", "Host-Guest"], 
                  "warnings": ["Poor for transition metals", "High HF exchange"]}
    }
    
    # Medium-quality functionals (score 6-8)
    medium_quality = {
        "BP86": {"score": 7.0, "cost": 3, "applications": ["Geometry Optimization", "Transition Metals"], 
                 "warnings": ["Poor barrier heights", "Overbinding"]},
        "BLYP": {"score": 7.2, "cost": 3, "applications": ["Organic Chemistry", "Conformational Analysis"], 
                 "warnings": ["Poor barrier heights", "Requires dispersion"]},
        "PBE": {"score": 7.5, "cost": 3, "applications": ["Solid State", "Geometry Optimization"], 
                "warnings": ["Underestimates barriers", "Requires dispersion"]},
        "TPSS": {"score": 7.8, "cost": 4, "applications": ["Transition Metals", "General Purpose"], 
                 "warnings": ["More expensive than GGAs"]},
        "M06": {"score": 7.6, "cost": 5, "applications": ["Organometallics", "Thermochemistry"], 
                "warnings": ["Numerical instability", "Fine grids required"]},
        "TPSSH": {"score": 7.4, "cost": 5, "applications": ["Transition Metals", "Conservative Hybrid"], 
                  "warnings": ["Lower accuracy than higher-HF hybrids"]},
        "OLYP": {"score": 7.1, "cost": 3, "applications": ["Organic Chemistry"], 
                 "warnings": ["Less tested than BLYP", "Requires dispersion"]},
        "PW91": {"score": 7.0, "cost": 3, "applications": ["Historical Reference"], 
                 "warnings": ["Superseded by PBE", "Overbinding"]},
        "SCANFUNC": {"score": 7.9, "cost": 5, "applications": ["General Purpose", "Solid State"], 
                     "warnings": ["Can be numerically unstable"]},
        "M06L": {"score": 7.3, "cost": 4, "applications": ["Thermochemistry", "Kinetics"], 
                 "warnings": ["Poor for transition metals", "Fine grids needed"]}
    }
    
    # Low-quality functionals (score 3-6)
    low_quality = {
        "LDA": {"score": 4.0, "cost": 1, "applications": ["Educational", "Solid State Reference"], 
                "warnings": ["Very poor accuracy", "Severe overbinding"]},
        "HFS": {"score": 3.0, "cost": 1, "applications": ["Educational"], 
                "warnings": ["No correlation", "Very poor accuracy"]},
        "LSD": {"score": 4.2, "cost": 1, "applications": ["Magnetic Systems", "Educational"], 
                "warnings": ["Poor molecular accuracy", "Overbinding"]},
        "VWN": {"score": 4.1, "cost": 1, "applications": ["Component of Hybrids"], 
                "warnings": ["Not for standalone use", "LDA limitations"]},
        "AM1": {"score": 5.5, "cost": 1, "applications": ["Large Systems", "Screening"], 
                "warnings": ["Semiempirical limitations", "Poor for charged species"]},
        "PM3": {"score": 5.7, "cost": 1, "applications": ["Large Systems", "Drug Design"], 
                "warnings": ["Inconsistent performance", "Poor for metals"]},
        "MNDO": {"score": 5.0, "cost": 1, "applications": ["Large Systems"], 
                 "warnings": ["Semiempirical limitations", "Poor for charged species"]}
    }
    
    # Check functional category
    if functional in high_quality:
        return high_quality[functional]
    elif functional in medium_quality:
        return medium_quality[functional]
    elif functional in low_quality:
        return low_quality[functional]
    else:
        # Default assessment for unlisted functionals
        return {"score": 6.0, "cost": 4, "applications": ["General Purpose"], 
                "warnings": ["Limited testing data"]}

def _assess_basis_quality(basis_set):
    """Assess the quality of a basis set."""
    # Excellent basis sets (score 8-10)
    excellent = {
        "def2-TZVP": {"score": 8.5, "cost": 6, "applications": ["General Purpose", "Production Calculations"], "warnings": []},
        "def2-TZVPP": {"score": 8.8, "cost": 7, "applications": ["Properties", "High Accuracy"], "warnings": []},
        "aug-cc-pVTZ": {"score": 9.0, "cost": 8, "applications": ["Benchmark", "Excited States"], "warnings": ["Can have linear dependence issues"]},
        "def2-QZVP": {"score": 9.2, "cost": 9, "applications": ["Benchmark", "Extrapolation"], "warnings": ["Very expensive"]},
        "aug-cc-pVQZ": {"score": 9.5, "cost": 10, "applications": ["Benchmark", "Reference"], "warnings": ["Extremely expensive", "Linear dependence issues"]},
        "cc-pVTZ": {"score": 8.7, "cost": 7, "applications": ["Correlated Methods", "Benchmark"], "warnings": ["Poor for DFT without tight functions"]},
        "cc-pVQZ": {"score": 9.0, "cost": 9, "applications": ["Benchmark", "Correlated Methods"], "warnings": ["Very expensive"]},
        "def2-TZVPD": {"score": 8.9, "cost": 8, "applications": ["Properties", "Excited States"], "warnings": ["Expensive"]},
        "ma-def2-TZVP": {"score": 8.6, "cost": 7, "applications": ["General Purpose", "Cost-Effective"], "warnings": []},
        "ANO-pVTZ": {"score": 9.1, "cost": 8, "applications": ["Benchmark", "Correlated Methods"], "warnings": ["Expensive integrals", "Specialized algorithms needed"]},
        "def2-TZVP(-f)": {"score": 8.3, "cost": 6, "applications": ["General Purpose", "Reduced f-functions"], "warnings": ["Missing f-functions on main group"]},
        "def2-QZVPP": {"score": 9.3, "cost": 10, "applications": ["Benchmark", "Very High Accuracy"], "warnings": ["Extremely expensive"]},
        "def2-QZVPD": {"score": 9.4, "cost": 10, "applications": ["Benchmark", "Properties"], "warnings": ["Extremely expensive"]},
        "def2-QZVPPD": {"score": 9.5, "cost": 10, "applications": ["Benchmark", "Ultimate Accuracy"], "warnings": ["Extremely expensive"]},
        "ma-def2-SV(P)": {"score": 6.9, "cost": 3, "applications": ["Large Systems", "Cost-Effective"], "warnings": ["Limited accuracy"]},
        "ma-def2-mSVP": {"score": 6.8, "cost": 3, "applications": ["Large Systems", "Minimal Augmentation"], "warnings": ["Limited accuracy"]},
        "ma-def2-TZVP(-f)": {"score": 8.4, "cost": 7, "applications": ["General Purpose", "Cost-Effective"], "warnings": ["Missing f-functions"]},
        "ma-def2-TZVPP": {"score": 8.7, "cost": 8, "applications": ["High Accuracy", "Cost-Effective"], "warnings": ["Expensive"]},
        "ma-def2-QZVPP": {"score": 9.1, "cost": 9, "applications": ["Benchmark", "Cost-Effective"], "warnings": ["Very expensive"]}
    }
    
    # Good basis sets (score 6-8)
    good = {
        "6-31G(d,p)": {"score": 7.0, "cost": 3, "applications": ["Organic Chemistry", "Routine Calculations"], "warnings": ["Poor for anions", "No diffuse functions"]},
        "6-311G(d,p)": {"score": 7.5, "cost": 4, "applications": ["Thermochemistry", "Medium Systems"], "warnings": ["Poor for anions"]},
        "def2-SVP": {"score": 6.8, "cost": 3, "applications": ["Large Systems", "Geometry Optimization"], "warnings": ["Limited accuracy for energetics"]},
        "cc-pVDZ": {"score": 6.5, "cost": 4, "applications": ["Correlated Methods", "Extrapolation"], "warnings": ["Poor for DFT", "Small for production work"]},
        "pc-2": {"score": 7.2, "cost": 4, "applications": ["General Purpose", "Systematic Studies"], "warnings": []},
        "6-31+G(d,p)": {"score": 7.3, "cost": 4, "applications": ["Anions", "Excited States"], "warnings": ["Linear dependence possible"]},
        "6-311++G(d,p)": {"score": 7.8, "cost": 5, "applications": ["High Accuracy", "Anions"], "warnings": ["Linear dependence issues"]},
        "def2-SVPD": {"score": 7.1, "cost": 4, "applications": ["Anions", "Large Systems"], "warnings": []},
        "aug-cc-pVDZ": {"score": 7.4, "cost": 5, "applications": ["Anions", "Extrapolation"], "warnings": ["Small for production"]},
        "pc-3": {"score": 7.9, "cost": 6, "applications": ["High Accuracy", "Systematic"], "warnings": []},
        "ma-def2-SVP": {"score": 7.0, "cost": 3, "applications": ["Large Systems", "Cost-Effective"], "warnings": []}
    }
    
    # Poor basis sets (score 3-6)
    poor = {
        "STO-3G": {"score": 3.0, "cost": 1, "applications": ["Educational", "Very Large Systems"], "warnings": ["Very poor accuracy", "Qualitative results only"]},
        "3-21G": {"score": 4.0, "cost": 1, "applications": ["Screening", "Very Large Systems"], "warnings": ["Poor accuracy", "Not for quantitative work"]},
        "3-21GSP": {"score": 4.2, "cost": 1, "applications": ["Screening", "Large Systems"], "warnings": ["Poor accuracy", "Limited element coverage"]},
        "4-22GSP": {"score": 4.3, "cost": 1, "applications": ["Screening", "Large Systems"], "warnings": ["Poor accuracy", "Limited testing"]},
        "6-31G": {"score": 5.5, "cost": 2, "applications": ["Preliminary Studies"], "warnings": ["No polarization functions", "Poor energetics"]},
        "6-31G(d)": {"score": 6.2, "cost": 2, "applications": ["Basic Calculations"], "warnings": ["Missing H polarization", "Poor for anions"]},
        "6-31G*": {"score": 6.2, "cost": 2, "applications": ["Basic Calculations"], "warnings": ["Missing H polarization", "Poor for anions"]},
        "6-31G**": {"score": 7.0, "cost": 3, "applications": ["Organic Chemistry", "Routine Calculations"], "warnings": ["Poor for anions", "No diffuse functions"]},
        "6-31G(d,p)": {"score": 7.0, "cost": 3, "applications": ["Organic Chemistry", "Routine Calculations"], "warnings": ["Poor for anions", "No diffuse functions"]},
        "6-31G(2d)": {"score": 6.5, "cost": 3, "applications": ["Enhanced Polarization"], "warnings": ["Missing H polarization", "Poor for anions"]},
        "6-31G(2d,p)": {"score": 6.8, "cost": 3, "applications": ["Enhanced Polarization"], "warnings": ["Poor for anions", "Moderate accuracy"]},
        "6-31G(2d,2p)": {"score": 6.9, "cost": 4, "applications": ["High Polarization"], "warnings": ["Poor for anions", "Expensive for size"]},
        "6-31G(2df)": {"score": 6.7, "cost": 4, "applications": ["Enhanced Polarization"], "warnings": ["Missing H polarization", "Poor for anions"]},
        "6-31G(2df,2p)": {"score": 7.0, "cost": 4, "applications": ["High Polarization"], "warnings": ["Poor for anions", "Expensive"]},
        "6-31G(2df,2pd)": {"score": 7.1, "cost": 5, "applications": ["Very High Polarization"], "warnings": ["Poor for anions", "Very expensive for size"]},
        "6-31+G*": {"score": 7.1, "cost": 3, "applications": ["Anions", "Basic Excited States"], "warnings": ["Missing H polarization"]},
        "6-31+G**": {"score": 7.3, "cost": 4, "applications": ["Anions", "Excited States"], "warnings": ["Linear dependence possible"]},
        "6-31+G(d)": {"score": 7.1, "cost": 3, "applications": ["Anions", "Basic Excited States"], "warnings": ["Missing H polarization"]},
        "6-31+G(d,p)": {"score": 7.3, "cost": 4, "applications": ["Anions", "Excited States"], "warnings": ["Linear dependence possible"]},
        "6-31+G(2d)": {"score": 7.0, "cost": 4, "applications": ["Anions", "Enhanced Polarization"], "warnings": ["Missing H polarization", "Linear dependence"]},
        "6-31+G(2d,p)": {"score": 7.2, "cost": 4, "applications": ["Anions", "Enhanced Polarization"], "warnings": ["Linear dependence possible"]},
        "6-31+G(2d,2p)": {"score": 7.3, "cost": 5, "applications": ["Anions", "High Polarization"], "warnings": ["Linear dependence", "Expensive"]},
        "6-31+G(2df)": {"score": 7.1, "cost": 5, "applications": ["Anions", "Enhanced Polarization"], "warnings": ["Missing H polarization", "Linear dependence"]},
        "6-31+G(2df,2p)": {"score": 7.3, "cost": 5, "applications": ["Anions", "High Polarization"], "warnings": ["Linear dependence", "Expensive"]},
        "6-31+G(2df,2pd)": {"score": 7.4, "cost": 6, "applications": ["Anions", "Very High Polarization"], "warnings": ["Linear dependence", "Very expensive"]},
        "6-31++G**": {"score": 7.4, "cost": 4, "applications": ["Anions", "Excited States"], "warnings": ["Linear dependence issues"]},
        "6-31++G(d,p)": {"score": 7.4, "cost": 4, "applications": ["Anions", "Excited States"], "warnings": ["Linear dependence issues"]},
        "6-31++G(2d,p)": {"score": 7.3, "cost": 5, "applications": ["Anions", "Enhanced Polarization"], "warnings": ["Linear dependence", "Expensive"]},
        "6-31++G(2d,2p)": {"score": 7.4, "cost": 5, "applications": ["Anions", "High Polarization"], "warnings": ["Linear dependence", "Expensive"]},
        "6-31++G(2df,2p)": {"score": 7.4, "cost": 6, "applications": ["Anions", "High Polarization"], "warnings": ["Linear dependence", "Very expensive"]},
        "6-31++G(2df,2pd)": {"score": 7.5, "cost": 6, "applications": ["Anions", "Very High Polarization"], "warnings": ["Linear dependence", "Very expensive"]},
        "6-311G": {"score": 6.8, "cost": 3, "applications": ["Medium Systems"], "warnings": ["No polarization", "Poor for anions"]},
        "6-311G*": {"score": 7.2, "cost": 4, "applications": ["Medium Systems"], "warnings": ["Missing H polarization", "Poor for anions"]},
        "6-311G**": {"score": 7.5, "cost": 4, "applications": ["Thermochemistry", "Medium Systems"], "warnings": ["Poor for anions"]},
        "6-311G(d)": {"score": 7.2, "cost": 4, "applications": ["Medium Systems"], "warnings": ["Missing H polarization", "Poor for anions"]},
        "6-311G(d,p)": {"score": 7.5, "cost": 4, "applications": ["Thermochemistry", "Medium Systems"], "warnings": ["Poor for anions"]},
        "6-311G(2d)": {"score": 7.3, "cost": 5, "applications": ["Enhanced Polarization"], "warnings": ["Missing H polarization", "Poor for anions"]},
        "6-311G(2d,p)": {"score": 7.6, "cost": 5, "applications": ["High Accuracy"], "warnings": ["Poor for anions", "Expensive"]},
        "6-311G(2d,2p)": {"score": 7.7, "cost": 5, "applications": ["High Accuracy"], "warnings": ["Poor for anions", "Expensive"]},
        "6-311G(2df)": {"score": 7.4, "cost": 5, "applications": ["Enhanced Polarization"], "warnings": ["Missing H polarization", "Poor for anions"]},
        "6-311G(2df,2p)": {"score": 7.7, "cost": 6, "applications": ["High Accuracy"], "warnings": ["Poor for anions", "Expensive"]},
        "6-311G(2df,2pd)": {"score": 7.8, "cost": 6, "applications": ["Very High Accuracy"], "warnings": ["Poor for anions", "Very expensive"]},
        "6-311G(3df)": {"score": 7.6, "cost": 6, "applications": ["Very High Polarization"], "warnings": ["Missing H polarization", "Very expensive"]},
        "6-311G(3df,3pd)": {"score": 7.9, "cost": 7, "applications": ["Benchmark Quality"], "warnings": ["Poor for anions", "Extremely expensive"]},
        "6-311+G*": {"score": 7.4, "cost": 4, "applications": ["Anions", "Medium Systems"], "warnings": ["Missing H polarization"]},
        "6-311+G**": {"score": 7.6, "cost": 5, "applications": ["High Accuracy", "Anions"], "warnings": ["Linear dependence possible"]},
        "6-311+G(d)": {"score": 7.4, "cost": 4, "applications": ["Anions", "Medium Systems"], "warnings": ["Missing H polarization"]},
        "6-311+G(d,p)": {"score": 7.6, "cost": 5, "applications": ["High Accuracy", "Anions"], "warnings": ["Linear dependence possible"]},
        "6-311+G(2d)": {"score": 7.5, "cost": 5, "applications": ["Anions", "Enhanced Polarization"], "warnings": ["Missing H polarization", "Linear dependence"]},
        "6-311+G(2d,p)": {"score": 7.7, "cost": 6, "applications": ["High Accuracy", "Anions"], "warnings": ["Linear dependence", "Expensive"]},
        "6-311+G(2d,2p)": {"score": 7.8, "cost": 6, "applications": ["Very High Accuracy", "Anions"], "warnings": ["Linear dependence", "Expensive"]},
        "6-311+G(2df)": {"score": 7.6, "cost": 6, "applications": ["Anions", "Enhanced Polarization"], "warnings": ["Missing H polarization", "Linear dependence"]},
        "6-311+G(2df,2p)": {"score": 7.8, "cost": 6, "applications": ["High Accuracy", "Anions"], "warnings": ["Linear dependence", "Expensive"]},
        "6-311+G(2df,2pd)": {"score": 7.9, "cost": 7, "applications": ["Very High Accuracy", "Anions"], "warnings": ["Linear dependence", "Very expensive"]},
        "6-311+G(3df)": {"score": 7.7, "cost": 7, "applications": ["Anions", "Very High Polarization"], "warnings": ["Missing H polarization", "Very expensive"]},
        "6-311+G(3df,2p)": {"score": 7.9, "cost": 7, "applications": ["Very High Accuracy", "Anions"], "warnings": ["Linear dependence", "Very expensive"]},
        "6-311+G(3df,3pd)": {"score": 8.0, "cost": 8, "applications": ["Benchmark Quality", "Anions"], "warnings": ["Linear dependence", "Extremely expensive"]},
        "6-311++G**": {"score": 7.7, "cost": 5, "applications": ["High Accuracy", "Anions"], "warnings": ["Linear dependence issues"]},
        "6-311++G(d,p)": {"score": 7.7, "cost": 5, "applications": ["High Accuracy", "Anions"], "warnings": ["Linear dependence issues"]},
        "6-311++G(2d,p)": {"score": 7.8, "cost": 6, "applications": ["Very High Accuracy", "Anions"], "warnings": ["Linear dependence", "Expensive"]},
        "6-311++G(2d,2p)": {"score": 7.9, "cost": 6, "applications": ["Very High Accuracy", "Anions"], "warnings": ["Linear dependence", "Expensive"]},
        "6-311++G(2df,2p)": {"score": 7.9, "cost": 7, "applications": ["Very High Accuracy", "Anions"], "warnings": ["Linear dependence", "Very expensive"]},
        "6-311++G(2df,2pd)": {"score": 8.0, "cost": 7, "applications": ["Benchmark Quality", "Anions"], "warnings": ["Linear dependence", "Very expensive"]},
        "6-311++G(3df,3pd)": {"score": 8.1, "cost": 8, "applications": ["Benchmark Quality", "Anions"], "warnings": ["Linear dependence", "Extremely expensive"]},
        "m6-31G": {"score": 6.8, "cost": 2, "applications": ["Transition Metals"], "warnings": ["Modified for 3d metals only", "Limited element coverage"]},
        "m6-31G*": {"score": 7.0, "cost": 3, "applications": ["Transition Metals"], "warnings": ["Modified for 3d metals only", "Missing H polarization"]},
        "pc-0": {"score": 5.8, "cost": 2, "applications": ["Large Systems"], "warnings": ["Limited accuracy"]},
        "pc-1": {"score": 6.3, "cost": 3, "applications": ["Screening"], "warnings": ["Small for production work"]},
        "def2-SV(P)": {"score": 6.7, "cost": 3, "applications": ["Large Systems", "Reduced Polarization"], "warnings": ["Limited accuracy for energetics"]},
        "cc-pV5Z": {"score": 9.3, "cost": 10, "applications": ["Benchmark", "Extrapolation"], "warnings": ["Extremely expensive"]},
        "cc-pV6Z": {"score": 9.4, "cost": 10, "applications": ["Benchmark", "Reference"], "warnings": ["Extremely expensive"]},
        "aug-cc-pV5Z": {"score": 9.4, "cost": 10, "applications": ["Benchmark", "Reference"], "warnings": ["Extremely expensive", "Linear dependence"]},
        "aug-cc-pV6Z": {"score": 9.5, "cost": 10, "applications": ["Benchmark", "Reference"], "warnings": ["Extremely expensive", "Linear dependence"]}
    }
    
    if basis_set in excellent:
        return excellent[basis_set]
    elif basis_set in good:
        return good[basis_set]
    elif basis_set in poor:
        return poor[basis_set]
    else:
        return {"score": 6.0, "cost": 4, "applications": ["General Purpose"], "warnings": ["Limited testing data"]}

def _assess_dispersion_quality(dispersion, functional):
    """Assess the appropriateness of dispersion correction."""
    # Check if functional has built-in dispersion
    builtin_dispersion = ["B97M-V", "WB97M-V", "WB97X-V"]
    
    if functional in builtin_dispersion and dispersion != "None":
        return {"score": 7.0, "warnings": ["Functional already includes dispersion - additional correction may double-count"]}
    elif functional in builtin_dispersion and dispersion == "None":
        return {"score": 9.0, "warnings": []}
    elif dispersion == "D4":
        return {"score": 9.5, "warnings": []}
    elif dispersion == "D3BJ":
        return {"score": 9.0, "warnings": []}
    elif dispersion == "D3":
        return {"score": 8.0, "warnings": ["D3BJ often more accurate"]}
    elif dispersion == "None":
        return {"score": 6.0, "warnings": ["Consider adding dispersion correction for non-covalent interactions"]}
    else:
        return {"score": 7.0, "warnings": []}

def _generate_improvements(functional, basis_set, dispersion):
    """Generate improvement suggestions for the method combination."""
    improvements = []
    
    # Basis set improvements
    if basis_set in ["STO-3G", "3-21G", "6-31G"]:
        improvements.append("Consider upgrading to 6-31G(d,p) or def2-SVP for better accuracy")
    elif basis_set == "6-31G(d,p)":
        improvements.append("For higher accuracy, consider def2-TZVP or 6-311G(d,p)")
    elif basis_set == "def2-SVP":
        improvements.append("For production calculations, consider def2-TZVP")
    
    # Dispersion improvements
    if dispersion == "None" and functional not in ["B97M-V", "WB97M-V", "WB97X-V"]:
        improvements.append("Add D3BJ or D4 dispersion correction for better non-covalent interactions")
    elif dispersion == "D3":
        improvements.append("Consider D3BJ for better short-range behavior")
    elif dispersion in ["D3", "D3BJ"]:
        improvements.append("For highest accuracy, consider D4 dispersion correction")
    
    # Functional improvements
    if functional in ["LDA", "HFS"]:
        improvements.append("Consider upgrading to PBE or B3LYP for much better accuracy")
    elif functional in ["BP86", "BLYP", "PBE"]:
        improvements.append("Consider PBE0 or B3LYP for better barrier heights")
    elif functional == "B3LYP":
        improvements.append("For non-covalent interactions, consider wB97X-D3 or B97M-V")
    
    return improvements
