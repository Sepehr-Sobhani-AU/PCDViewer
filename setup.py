from setuptools import setup, find_packages

setup(
    name='PCDViewer',
    version='1.0.0',
    description='A Qt-based OpenGL viewer for point cloud data (PCD)',
    author='Sepehr Sobhani',
    author_email='sepehr.sobhani@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
        'numpy>=1.18.0',
        'PyOpenGL>=3.1.0',
        'Open3D',
    ],
    entry_points={
        'console_scripts': [
            'pcdviewer=PCDViewer:main',  # Assuming you create a `main()` function to start the app.
        ],
    },
    include_package_data=True,
    zip_safe=False
)
