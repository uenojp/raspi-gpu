#!/bin/env python3

from videocore6.assembler import qpu
from videocore6.driver import Driver


@qpu
def kernel(asm):
    nop(sig=ldunifrf(r0))   # r0=[2 x16]
    nop(sig=ldunifrf(r1))   # r1=[3 x16]
    nop(sig=ldunifrf(r2))   # r2=[base-addr x16]

    add(r0, r0, r1)

    mov(tmud, r0)
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
        out = drv.alloc(16, 'uint32')
        out[:] = 0.0

        unif = drv.alloc(3, 'uint32')
        unif[0] = 2
        unif[1] = 3
        unif[2] = out.addresses()[0]

        print(' before: out '.center(80, '='))
        print(out)

        kernel_code = drv.program(kernel)
        nqpus = 1
        drv.execute(kernel_code, uniforms=unif.addresses()[0], thread=nqpus)

        print(' after:  out '.center(80, '='))
        print(out)

        print(' uniform '.center(80, '='))
        print(unif)


if __name__ == '__main__':
    main()
