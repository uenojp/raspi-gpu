#!/bin/env python3

from videocore6.assembler import qpu
from videocore6.driver import Driver


@qpu
def kernel(asm):
    # r0 contains the address of array `out`. 
    nop(sig=ldunifrf(r0))

    # Data to be written back.
    mov(r1, 7)

    # Generate the addresses of each element of array `out`.
    eidx(r2)            # r2=[0..=15]
    shl(r2, r2, 2)      # r2=4*[0..=15]
    add(r0, r0, r2)     # r0=base_addr[:]+4*[0..=15]

    # Write back r1 D->H via TMU
    # NOTE:
    #  Execute ` mov(tmud, r0)` to check the addresses of `out`.
    #  [1179648 1179652 1179656 ... 1179708]
    mov(tmud, r1)
    mov(tmua, r0)
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

        unif = drv.alloc(1, 'uint32')
        unif[0] = out.addresses()[0]

        print(' before: out '.center(80, '='))
        print(out)

        kernel_code = drv.program(kernel)
        nqpus = 1
        drv.execute(kernel_code, uniforms=unif.addresses()[0], thread=nqpus)

        print(' after:  out '.center(80, '='))
        print(out)


if __name__ == '__main__':
    main()
