NAME=arcospyu
PREFIX ?= ${HOME}/local/DIR/${NAME}
DEB_TARGET=python-arcospyu_0.1-1_all.deb

all:
	echo "Does nothing, try make install"

install:
	PYTHONPATH=${HOME}/local/DIR/arcospyu/lib/python2.7/site-packages/ python setup.py install --prefix=${PREFIX}

install_py3:
	PYTHONPATH=${HOME}/local/DIR/arcospyu/lib/python3.6/site-packages/ python setup.py install --prefix=${PREFIX}

xstow_install: install
	cd ${PREFIX}/../ && xstow ${NAME}

xstow_uninstall:
	cd ${PREFIX}/../ && xstow -D ${NAME} && rm -rf ${NAME}

%.deb:
	python setup.py --command-packages=stdeb.command bdist_deb

deb: deb_dist/${DEB_TARGET}

deb_install: deb_dist/${DEB_TARGET}
	cd deb_dist && sudo dpkg -i *.deb

clean:
	python setup.py clean
	rm -rf build/ deb_dist/
