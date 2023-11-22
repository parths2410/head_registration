1. Create conda environment using environment.yml file

    ```bash
    conda env create -f environment.yml
    ```

2. Activate the environment

    ```bash
    conda activate hair
    ```

3. Run the code

    ```bash
    python main.py
    ```


Dependencies -
0. numpy, scipy

    ```bash
    pip install numpy scipy
    ```

1. open3d

    ```bash
    pip install opend3d
    ```

2. cupy

    ```bash
    pip install cupy
    ```

3. probreg - https://github.com/neka-nat/probreg

    ```bash
    pip install probreg
    ```

4. scikit-sparse
    With pip
    For pip installs of scikit-sparse depend on the suite-sparse library which can be installed - 
    ```bash
    # mac
    brew install suite-sparse

    # debian
    sudo apt-get install libsuitesparse-dev
    ```
    after that -
    ```bash
    pip install scikit-sparselp
    ```

    With conda
    ```bash
    conda install -c conda-forge scikit-sparse
    ```
