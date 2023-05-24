# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.0/containers/python-3-miniconda/.devcontainer/base.Dockerfile

FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
RUN mkdir /tmp/conda-tmp/
RUN chmod 777 /tmp/conda-tmp/
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

ENV PYTHONPATH "${PYTHONPATH}:/workspaces/simple_lang_compiler/src"

# ensures that the python output i.e. the stdout and stderr streams are sent straight to terminal
ARG pythonunbuffered_value=1
ENV PYTHONUNBUFFERED=$pythonunbuffered_value

# to install java 11 and add it to the path
RUN sudo apt-get update && \
    sudo apt-get install -y openjdk-11-jdk
ENV PATH="/usr/lib/jvm/java-11-openjdk-amd64/bin:${PATH}"