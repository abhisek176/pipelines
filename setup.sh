dir=$(dirname $BASH_SOURCE)/processMeerKAT
export PATH=$PATH:$dir
export PYTHONPATH=$PYTHONPATH:$dir
export SINGULARITYENV_PYTHONPATH=$PYTHONPATH:/opt/casaaddons
