export PYTHONPATH='.'

if [ "$#" -gt "0" ]
  then
    python test_project/manage.py test $@
  else
    python test_project/manage.py test djangotransifex
fi
