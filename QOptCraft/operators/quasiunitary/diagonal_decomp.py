"""Copyright 2021 Daniel Gómez Aguado

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""


import numpy as np


def D_decomposition(M, dim):
    DList = np.zeros((dim, dim, dim), dtype=complex)

    for i in range(0, dim):
        I = np.identity(dim, dtype=complex)
        # Matrix D_i creation consists on replacing the identity
        # matrix element [i,i] for D_i of the original matrix D (here, M)
        I[i, i] = M[i, i]
        DList[i, :, :] = I
    return DList
