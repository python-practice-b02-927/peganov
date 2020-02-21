from distutils.core import setup  
from distutils.extension import Extension  
from Cython.Build import cythonize  


setup(
    ext_modules = cythonize(
        [
            Extension(
                "cblas_matmul",
                ["cblas_matmul.pyx"],
                libraries=["openblasp-r0-2ecf47d5.3.7.dev"],
                extra_link_args=[ 
                    "-L/home/anton/anaconda3/lib/python3.6/site-packages/numpy/.libs"
                ]
            )
        ]
    )
)

