#!/bin/env python3

from videocore6.assembler import qpu
from videocore6.driver import Driver


@qpu
def kernel(asm):
    # input: rf0,rf1 output: rf2,rf3
    nop(sig=ldunifrf(rf0))
    nop(sig=ldunifrf(rf1))
    nop(sig=ldunifrf(rf2))
    nop(sig=ldunifrf(rf3))

    eidx(r0)
    shl(r0, r0, 2)
    add(rf0, rf0, r0)
    add(rf1, rf1, r0)
    add(rf2, rf2, r0)
    add(rf3, rf3, r0)

    # H->D: rf10,r11
    mov(tmua, rf0, sig=thrsw)
    nop()
    nop()
    nop(sig=ldtmu(rf10))

    mov(tmua, rf1, sig=thrsw)
    nop()
    nop()
    nop(sig=ldtmu(rf11))

    # D->H: rf11,rf10(swapped)
    mov(tmud, rf11)
    mov(tmua, rf2)
    tmuwt()

    mov(tmud, rf10)
    mov(tmua, rf3)
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
        in_a = drv.alloc(16, 'float32')
        rf1 = drv.alloc(16, 'float32')
        rf2 = drv.alloc(16, 'float32')
        rf3 = drv.alloc(16, 'float32')

        in_a[:] = 2.0
        rf1[:] = 3.0
        rf2[:] = 0.0
        rf3[:] = 0.0

        unif = drv.alloc(4, 'uint32')
        unif[0] = in_a.addresses()[0]
        unif[1] = rf1.addresses()[0]
        unif[2] = rf2.addresses()[0]
        unif[3] = rf3.addresses()[0]

        kernel_code = drv.program(kernel)
        nqpus = 1
        drv.execute(kernel_code, uniforms=unif.addresses()[0], thread=nqpus)

        print(' in_a, rf1 '.center(80, '='))
        print(in_a)
        print(rf1)
        print(' rf2, rf3 '.center(80, '='))
        print(rf2)
        print(rf3)


if __name__ == '__main__':
    main()
