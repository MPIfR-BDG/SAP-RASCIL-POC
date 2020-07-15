#! /bin/bash -f

FULLPATH=$(realpath $0)
DIRONLY=$(dirname $FULLPATH)
LIBLOCAL="${DIRONLY}/../local_lib/"
echo $LIBLOCAL

echo $PYTHONPATH

if [ -z "$PYTHONPATH" ]
then
	echo "PYTHONPATH empty: adding LIBLOCAl path"
	export PYTHONPATH=${LIBLOCAL}
else

	if [[ $PYTHONPATH == *"${LIBLOCAL}"* ]]
	then
		echo "PYTHONPATH already contains LIBLOCAL path: $LIBLOCAL."
	else
		echo "adding LIBLOCAL path to PYTHONPATH"
		export PYTHONPATH=$PYTHONPATH:$LIBLOCAL
	fi

fi

echo "PYTHONPATH = $PYTHONPATH"
