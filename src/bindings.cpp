#include <pybind11/pybind11.h>
#include "fractalhash.h"

PYBIND11_MODULE(fractalcore, m) {
    m.def("calculate_fractal_hash", &generate_fractal_hash);
}
