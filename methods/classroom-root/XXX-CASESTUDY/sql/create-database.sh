#!/usr/bin/env bash

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCHEMA=${THISDIR?}/database.sql3

# The path to the database can be changed below
DATABASE=${THISDIR?}/database.sql3

echo -n "Removing database ... "
rm ${DATABASE?}
echo "done."

echo -n "Creating schema ... "
sqlite3 ${DATABASE?} < ${SCHEMA?}
echo "done."


