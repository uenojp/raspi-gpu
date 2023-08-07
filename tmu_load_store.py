#!/bin/env python3

from videocore6.assembler import qpu
from videocore6.driver import Driver


@qpu
def kernel(asm):
    # input: r0, output: r1
    nop(sig=ldunifrf(r0))
    nop(sig=ldunifrf(r1))

    # index
    eidx(r2)
    shl(r2, r2, 2)
    add(r0, r0, r2)
    add(r1, r1, r2)

    # H->D: r3
    mov(tmua, r0, sig=thrsw)
    nop()
    nop()
    nop(sig=ldtmu(r3))

    # twice
    shl(r3, r3, 1)

    # D->H: r3
    mov(tmud, r3)
    mov(tmua, r1)
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
        data = drv.alloc(16, 'uint32')
        out = drv.alloc(16, 'uint32')
        data[:] = list(range(16))
        out[:] = 0

        unif = drv.alloc(2, 'uint32')
        unif[0] = data.addresses()[0]
        unif[1] = out.addresses()[0]

        print(' before: in  '.center(80, '='))
        print(data)
        print(' before: out '.center(80, '='))
        print(out)

        kernel_code = drv.program(kernel)
        nqpus = 1
        drv.execute(kernel_code, uniforms=unif.addresses()[0], thread=nqpus)

        print(' after:  out '.center(80, '='))
        print(out)


if __name__ == '__main__':
    main()
