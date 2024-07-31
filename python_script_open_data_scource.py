import hepunits
import fastjet
from hepunits import GeV
import particle
from mpl_toolkits.mplot3d import Axes3D
import vector
import zfit
import iminuit.cost
import matplotlib.pyplot as plt
import boost_histogram as bh
import skhep_testdata
import awkward as ak
import numpy as np
import hist
import uproot


try:
    from fsspec_xrootd import XRootDFileSystem

    print("XRootDFileSystem imported successfully.")
except ImportError as e:
    print(f"Error importing XRootDFileSystem: {e}")
file = uproot.open(
    "root://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root"
)  # this is puled out from the internet
file.classnames()
tree = file["Events"]
tree.show()
tree["nMuon"].array()
tree["Muon_pt"].array(entry_start=1000, entry_stop=2000)
muons = tree.arrays(
    ["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"], entry_stop=1000
)
muons["Muon_pt"]
muons["Muon_eta"]
muons["Muon_phi"]  # and so on.
tree.keys(filter_name="Muon_*")
tree.arrays(filter_name="Muon_*", entry_stop=1000)
muons = tree.arrays(entry_stop=1000)
cut = muons["nMuon"] == 2
pt0 = muons["Muon_pt", cut, 0]
pt1 = muons["Muon_pt", cut, 1]
eta0 = muons["Muon_eta", cut, 0]
eta1 = muons["Muon_eta", cut, 1]
phi0 = muons["Muon_phi", cut, 0]
phi1 = muons["Muon_phi", cut, 1]
mass = np.sqrt(2 * pt0 * pt1 * (np.cosh(eta0 - eta1) - np.cos(phi0 - phi1)))
masshist = hist.Hist(hist.axis.Regular(120, 0, 120, label="mass [GeV]"))
masshist.fill(mass)
masshist.plot()
tree.keys(filter_name=["nMuon", "/Muon_(pt|eta|phi)/"])
masshist = hist.Hist(hist.axis.Regular(120, 0, 120, label="mass [GeV]"))
for muons in tree.iterate(filter_name=["nMuon", "/Muon_(pt|eta|phi)/"]):
    cut = muons["nMuon"] == 2
    pt0 = muons["Muon_pt", cut, 0]
    pt1 = muons["Muon_pt", cut, 1]
    eta0 = muons["Muon_eta", cut, 0]
    eta1 = muons["Muon_eta", cut, 1]
    phi0 = muons["Muon_phi", cut, 0]
    phi1 = muons["Muon_phi", cut, 1]
    mass = np.sqrt(2 * pt0 * pt1 *
                   (np.cosh(eta0 - eta1) - np.cos(phi0 - phi1)))
    masshist.fill(mass)
    print(masshist.sum() / tree.num_entries)
masshist.plot()
tree["nMuon"].array(library="np", entry_stop=1000)
tree.arrays(library="np", entry_stop=1000)
tree.arrays(library="pd", entry_stop=1000)
cut = muons["nMuon"] == 2
pt0 = muons["Muon_pt", cut, 0]
ak.Array([[0.0, 1.1, 2.2], [], [3.3, 4.4], [5.5], [6.6, 7.7, 8.8, 9.9]])
array = ak.Array([[0.0, 1.1, 2.2], [], [3.3, 4.4],
                 [5.5], [6.6, 7.7, 8.8, 9.9]])
array.tolist()
array
print(array[[True, False, True, False, True], 1])
print(array[[2, 3, 3, 1]])
print(ak.num(array))
print(ak.num(array) > 0)
print(array[ak.num(array) > 0, 0])
array[ak.num(array) > 1, 1]
cut = array * 10 % 2 == 0
array[cut]
file = uproot.open(
    "root://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root"
)
tree = file["Events"]
muon_pt = tree["Muon_pt"].array(entry_stop=10)
particle_cut = muon_pt > 20
print(muon_pt[particle_cut])
print(muon_pt)
event_cut = ak.any(muon_pt > 20, axis=1)
muon_pt[event_cut]
cleaned = muon_pt[particle_cut]
numbers = ak.Array([[1, 2, 3], [], [5, 7], [11]])
letters = ak.Array([["a", "b"], ["c"], ["d"], ["e", "f"]])
pairs = ak.cartesian((numbers, letters))
pairs
pairs["0"]
pairs["1"]
lefts, rights = ak.unzip(pairs)
lefts
rights
pairs = ak.combinations(numbers, 2)
print(pairs)
lefts, rights = ak.unzip(pairs)
lefts * rights  # they line up, so we can compute formulas
lefts
rights
pairs = ak.combinations(numbers, 2)
print(pairs)
lefts, rights = ak.unzip(pairs)
lefts * rights  # they line up, so we can compute formulas
file = uproot.open(
    "root://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root"
)
tree = file["Events"]
arrays = tree.arrays(
    filter_name="/Muon_(pt|eta|phi|charge)/", entry_stop=10000)
muons = ak.zip(
    {
        "pt": arrays["Muon_pt"],
        "eta": arrays["Muon_eta"],
        "phi": arrays["Muon_phi"],
        "charge": arrays["Muon_charge"],
    }
)
arrays.type
print(arrays[:5])
print(muons[:5])
pairs = ak.combinations(muons, 2)
pairs.type
mu1, mu2 = ak.unzip(pairs)
mass = np.sqrt(
    2 * mu1.pt * mu2.pt * (np.cosh(mu1.eta - mu2.eta) -
                           np.cos(mu1.phi - mu2.phi))
)
mass
hist.Hist(hist.axis.Regular(120, 0, 120, label="mass [GeV]")).fill(
    ak.ravel(mass)
).plot()
ak.max(mass, axis=1)
ak.flatten(ak.max(mass, axis=1), axis=0)
ak.max(mass[ak.num(mass) > 0], axis=1)
zmass = particle.Particle.findall("Z0")[0].mass / hepunits.GeV
zmass
tree = uproot.open(skhep_testdata.data_path("uproot-Zmumu.root"))["events"]
np.histogram(tree["M"].array())
plt.hist(tree["M"].array())
h = hist.Hist(hist.axis.Regular(120, 60, 120, name="mass"))
h.fill(tree["M"].array())
h.plot()
h[10:110].plot()
h[hist.loc(90):].plot()
h[:: hist.rebin(2)].plot()
h[hist.loc(80): hist.loc(100): sum]
picodst = uproot.open(
    "https://pivarski-princeton.s3.amazonaws.com/pythia_ppZee_run17emb.picoDst.root:PicoDst"
)
vertexhist = hist.Hist(
    hist.axis.Regular(600, -1, 1, label="x"),
    hist.axis.Regular(600, -1, 1, label="y"),
    hist.axis.Regular(40, -200, 200, label="z"),
)
vertex_data = picodst.arrays(filter_name="*mPrimaryVertex[XYZ]")
vertexhist.fill(
    ak.flatten(vertex_data["Event.mPrimaryVertexX"]),
    ak.flatten(vertex_data["Event.mPrimaryVertexY"]),
    ak.flatten(vertex_data["Event.mPrimaryVertexZ"]),
)
vertexhist[:, :, sum].plot2d_full()
vertexhist[
    hist.loc(-0.25): hist.loc(0.25), hist.loc(-0.25): hist.loc(0.25), sum
].plot2d_full()
vertexhist[sum, sum, :].plot()
vertexhist[
    hist.loc(-0.25): hist.loc(0.25): sum, hist.loc(-0.25): hist.loc(0.25): sum, :
].plot()
norm = len(h.axes[0].widths) / \
    (h.axes[0].edges[-1] - h.axes[0].edges[0]) / h.sum()


def f(x, background, mu, gamma):
    return (
        background
        + (1 - background) * gamma**2 /
        ((x - mu) ** 2 + gamma**2) / np.pi / gamma
    )


loss = iminuit.cost.LeastSquares(
    h.axes[0].centers, h.values() * norm, np.sqrt(h.variances()) * norm, f
)
loss.mask = h.variances() > 0
minimizer = iminuit.Minuit(loss, background=0, mu=91, gamma=4)
minimizer.migrad()
minimizer.hesse()
(h * norm).plot()
plt.plot(loss.x, f(loss.x, *minimizer.values))
binned_data = zfit.data.BinnedData.from_hist(h)
binning = zfit.binned.RegularBinning(120, 60, 120, name="mass")
space = zfit.Space("mass", binning=binning)
background = zfit.Parameter("background", 0)
mu = zfit.Parameter("mu", 91)
gamma = zfit.Parameter("gamma", 4)
unbinned_model = zfit.pdf.SumPDF(
    [zfit.pdf.Uniform(60, 120, space), zfit.pdf.Cauchy(
        mu, gamma, space)], [background]
)
model = zfit.pdf.BinnedFromUnbinnedPDF(unbinned_model, space)
loss = zfit.loss.BinnedNLL(model, binned_data)
minimizer = zfit.minimize.Minuit()
result = minimizer.minimize(loss)
binned_data.to_hist().plot(density=1)
model.to_hist().plot(density=1)
# Define two vectors
one = vector.obj(px=1, py=0, pz=0)
two = vector.obj(px=0, py=1, pz=1)
# Perform vector addition
result = one + two
# Calculate deltaR (a measure of angular distance)
delta_r = one.deltaR(two)
# Convert to cylindrical coordinates (rho, phi, eta)
one_rhophieta = one.to_rhophieta()
two_rhophieta = two.to_rhophieta()
# Print results
print("Vector one in (px, py, pz):", one)
print("Vector two in (px, py, pz):", two)
print("Result of addition (px, py, pz):", result)
print("DeltaR between one and two:", delta_r)
print("Vector one in (rho, phi, eta):", one_rhophieta)
print("Vector two in (rho, phi, eta):", two_rhophieta)
fig = plt.figure(figsize=(12, 6))
# Plot the vectors in Cartesian coordinates
ax = fig.add_subplot(121, projection="3d")
ax.quiver(0, 0, 0, one.px, one.py, one.pz, color="r", label="Vector one")
ax.quiver(0, 0, 0, two.px, two.py, two.pz, color="b", label="Vector two")
ax.quiver(
    0, 0, 0, result.px, result.py, result.pz, color="g", label="Result (one + two)"
)
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_xlabel("Px")
ax.set_ylabel("Py")
ax.set_zlabel("Pz")
ax.legend()
ax.set_title("Vectors in Cartesian Coordinates")
# Convert cylindrical coordinates to Cartesian for plotting
one_cylindrical = (
    one_rhophieta.rho * np.cos(one_rhophieta.phi),
    one_rhophieta.rho * np.sin(one_rhophieta.phi),
    one_rhophieta.eta,
)
two_cylindrical = (
    two_rhophieta.rho * np.cos(two_rhophieta.phi),
    two_rhophieta.rho * np.sin(two_rhophieta.phi),
    two_rhophieta.eta,
)
# Plot the vectors in Cylindrical coordinates
ax = fig.add_subplot(122, projection="3d")
ax.quiver(0, 0, 0, *one_cylindrical, color="r", label="Vector one")
ax.quiver(0, 0, 0, *two_cylindrical, color="b", label="Vector two")
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_xlabel("Rho cos(Phi)")
ax.set_ylabel("Rho sin(Phi)")
ax.set_zlabel("Eta")
ax.legend()
ax.set_title("Vectors in Cylindrical Coordinates")
# Add annotation for deltaR in the Cartesian plot
midpoint = ((one.px + two.px) / 2, (one.py + two.py) /
            2, (one.pz + two.pz) / 2)
ax.text(
    midpoint[0],
    midpoint[1],
    midpoint[2],
    f"ΔR = {delta_r:.2f}",
    color="purple",
    fontsize=12,
    weight="bold",
)


def plot_arc(ax, v1, v2, n_points=100):
    angle = delta_r
    t = np.linspace(0, angle, n_points)
    axis = np.cross([v1.px, v1.py, v1.pz], [v2.px, v2.py, v2.pz])
    axis = axis / np.linalg.norm(axis)

    arc = []
    for ti in t:
        R = rotation_matrix(axis, ti)
        arc.append(R @ [v1.px, v1.py, v1.pz])

    arc = np.array(arc)
    ax.plot(arc[:, 0], arc[:, 1], arc[:, 2], "purple", label="DeltaR Arc")


def rotation_matrix(axis, theta):
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array(
        [
            [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
            [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
            [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc],
        ]
    )


plot_arc(ax, one, two)
plt.tight_layout()
plt.show()
tree = uproot.open(skhep_testdata.data_path("uproot-Zmumu.root"))["events"]
one = ak.to_numpy(tree.arrays(filter_name=["E1", "p[xyz]1"]))
two = ak.to_numpy(tree.arrays(filter_name=["E2", "p[xyz]2"]))
one.dtype.names = ("E", "px", "py", "pz")
two.dtype.names = ("E", "px", "py", "pz")
one = one.view(vector.MomentumNumpy4D)
two = two.view(vector.MomentumNumpy4D)
one + two
one.deltaR(two)
one.to_rhophieta()
two.to_rhophieta()
vector.register_awkward()
tree = uproot.open(skhep_testdata.data_path("uproot-HZZ.root"))["events"]
array = tree.arrays(filter_name=["Muon_E", "Muon_P[xyz]"])
muons = ak.zip(
    {"px": array.Muon_Px, "py": array.Muon_Py,
        "pz": array.Muon_Pz, "E": array.Muon_E},
    with_name="Momentum4D",
)
mu1, mu2 = ak.unzip(ak.combinations(muons, 2))
mu1 + mu2
mu1.deltaR(mu2)
muons.to_rhophieta()
particle.Particle.findall("pi")
z_boson = particle.Particle.from_name("Z0")
z_boson.mass / GeV, z_boson.width / GeV
print(z_boson.describe())
particle.Particle.from_pdgid(111)
particle.Particle.findall(
    lambda p: p.pdgid.is_meson and p.pdgid.has_strange and p.pdgid.has_charm
)
print(particle.PDGID(211).info())
pdgid = particle.Corsika7ID(11).to_pdgid()
particle.Particle.from_pdgid(pdgid)
vector.register_awkward()
picodst = uproot.open(
    "https://pivarski-princeton.s3.amazonaws.com/pythia_ppZee_run17emb.picoDst.root:PicoDst"
)
px, py, pz = ak.unzip(
    picodst.arrays(filter_name=["Track/Track.mPMomentum[XYZ]"], entry_stop=100)
)
probable_mass = particle.Particle.from_pdgid(211).mass / GeV
pseudojets = ak.zip(
    {"px": px, "py": py, "pz": pz, "mass": probable_mass}, with_name="Momentum4D"
)
good_pseudojets = pseudojets[pseudojets.pt > 0.1]
jetdef = fastjet.JetDefinition(fastjet.antikt_algorithm, 1.0)
clusterseq = fastjet.ClusterSequence(good_pseudojets, jetdef)
clusterseq.inclusive_jets()
ak.num(good_pseudojets), ak.num(clusterseq.inclusive_jets())