#!/bin/env python3

import numpy as np

from videocore6.assembler import qpu
from videocore6.driver import Driver


@qpu
def kernel(asm):
    # a, b, c
    nop(sig=ldunifrf(r0))
    nop(sig=ldunifrf(r1))
    nop(sig=ldunifrf(r2))

    # index
    eidx(r3)
    shl(r3, r3, 2)
    add(r0, r0, r3)
    add(r1, r1, r3)
    add(r2, r2, r3)

    # H->D: r3, r4
    mov(tmua, r0, sig=thrsw)
    nop()
    nop()
    nop(sig=ldtmu(r3))

    mov(tmua, r1, sig=thrsw)
    nop()
    nop()
    nop(sig=ldtmu(r4))

    # c <- a + b
    fadd(r4, r4, r3)

    # D->H: r1
    mov(tmud, r4)
    mov(tmua, r2)
    tmuwt()

    # epilogue for sync
    nop(sig=thrsw)
    nop(sig=thrsw)
    nop()
    nop()
    nop(sig=thrsw)
    nop()
    nop()
    nop()


def main():
    with Driver() as drv:
        a = np.random.random(16).astype('float32')
        b = np.random.random(16).astype('float32')

        device_a = drv.alloc(16, 'float32')
        device_b = drv.alloc(16, 'float32')
        device_c = drv.alloc(16, 'float32')

        device_a[:] = a
        device_b[:] = b

        unif = drv.alloc(3, 'uint32')
        unif[0] = device_a.addresses()[0]
        unif[1] = device_b.addresses()[0]
        unif[2] = device_c.addresses()[0]

        kernel_code = drv.program(kernel)
        nqpus = 1
        drv.execute(kernel_code, uniforms=unif.addresses()[0], thread=nqpus)

        print(' a '.center(80, '='))
        print(a)
        print(' b '.center(80, '='))
        print(b)
        print(' a+b '.center(80, '='))
        print(device_c)
        print(' error '.center(80, '='))
        print(np.abs(a + b - device_c))


if __name__ == '__main__':
    main()
