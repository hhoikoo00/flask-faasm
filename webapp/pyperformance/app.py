from flask import Flask

from .lib.chaos import bench_chaos
from .lib.deltablue import bench_deltablue
from .lib.fannkuch import bench_fannkuch
from .lib.float_bm import bench_float_bm
from .lib.go import bench_go
from .lib.hexiom import bench_hexiom
from .lib.json_dumps import bench_json_dumps
from .lib.json_loads import bench_json_loads
from .lib.logging import bench_logging
from .lib.mdp import bench_mdp
from .lib.nbody import bench_nbody
from .lib.pidigits import bench_pidigits
from .lib.raytrace import bench_raytrace
from .lib.richards import bench_richards
from .lib.scimark import bench_scimark
from .lib.spectral_norm import bench_spectral_norm
from .lib.unpack_sequence import bench_unpack_sequence

app = Flask(__name__)


@app.post("/bm/chaos")
def chaos():
    bench_chaos()
    return "Success"


@app.post("/bm/deltablue")
def deltablue():
    bench_deltablue()
    return "Success"


@app.post("/bm/fannkuch")
def fannkuch():
    bench_fannkuch()
    return "Success"


@app.post("/bm/float_bm")
def float_bm():
    bench_float_bm()
    return "Success"


@app.post("/bm/go")
def go():
    bench_go()
    return "Success"


@app.post("/bm/hexiom")
def hexiom():
    bench_hexiom()
    return "Success"


@app.post("/bm/json_dumps")
def json_dumps():
    bench_json_dumps()
    return "Success"


@app.post("/bm/json_loads")
def json_loads():
    bench_json_loads()
    return "Success"


@app.post("/bm/logging")
def logging():
    bench_logging()
    return "Success"


@app.post("/bm/mdp")
def mdp():
    bench_mdp()
    return "Success"


@app.post("/bm/nbody")
def nbody():
    bench_nbody()
    return "Success"


@app.post("/bm/pidigits")
def pidigits():
    bench_pidigits()
    return "Success"


@app.post("/bm/raytrace")
def raytrace():
    bench_raytrace()
    return "Success"


@app.post("/bm/richards")
def richards():
    bench_richards()
    return "Success"


@app.post("/bm/scimark")
def scimark():
    bench_scimark()
    return "Success"


@app.post("/bm/spectral_norm")
def spectral_norm():
    bench_spectral_norm()
    return "Success"


@app.post("/bm/unpack_sequence")
def unpack_sequence():
    bench_unpack_sequence()
    return "Success"
