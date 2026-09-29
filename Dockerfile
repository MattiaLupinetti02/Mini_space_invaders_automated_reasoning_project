FROM continuumio/miniconda3:latest

# Crea l'ambiente conda "ASP" (stesso nome del kernel richiesto dal notebook)
# con clingo (solver ASP: CLI + binding Python) e le librerie usate nel notebook
RUN conda create -y -n ASP -c conda-forge \
        python=3.12 \
        clingo \
        jupyterlab \
        notebook \
        ipykernel \
        pandas \
        matplotlib \
    && conda clean -afy

# Registra il kernel "ASP" per Jupyter (combacia col kernelspec del notebook,
# cosi' si seleziona da solo aprendo test_space_invaders.ipynb)
RUN /opt/conda/envs/ASP/bin/python -m ipykernel install \
        --name ASP --display-name "ASP" --sys-prefix

# Rende l'ambiente ASP quello di default (clingo, jupyter, ... in PATH)
ENV PATH=/opt/conda/envs/ASP/bin:$PATH

WORKDIR /work
EXPOSE 8888

CMD ["jupyter", "notebook", \
     "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
