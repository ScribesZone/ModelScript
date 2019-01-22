#!/usr/bin/env bash

# Create a database with optionally a dataset loaded.
# usage:  create-database.sh [ dsX ]
#     Create the database.sqlite3
#     Optionaly load the dataseet dsX
#
# This script basically execute :
#
#     sqlite3 database.sqlite3 < schema.sql
#     sqlite3 database.sqlite3 < datasets/dsX.sql
#
# The location of the database file can be changed through
# the $DATABASE variable below.

DATASET=$1

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# The path to the database can be changed below
DATABASE=${THISDIR?}/database.sqlite3

# Path to the schema. Not reason to change it
SCHEMA=${THISDIR?}/schema/schema.sql

# Path to the dataset file.
DATASET_FILE=${THISDIR?}/datasets/${DATASET?}.sql

DATASET_ERRORS=${DATASET_FILE?}.err.txt

echo -n "Clearing database ... "
rm -f ${DATABASE?}
echo "done."

echo -n "Creating database schema ... "
sqlite3 ${DATABASE?} < ${SCHEMA?}
echo "done."

if [ "${DATASET}" = "" ]; then
    echo "Empty database created."
else
    if [ -f "${DATASET_FILE}" ]; then
        echo -n "Loading dataset ${DATASET} ..."
        sqlite3 ${DATABASE?} <  ${DATASET_FILE?}
        echo " done."
        echo "Dataset ${DATASET} loaded in database."
    else
        echo "Dataset '${DATASET?}' does not exist." >/dev/stderr
        echo "No file ${DATASET_FILE?}."  >/dev/stderr
        echo "Database is empty"
        exit 1
    fi
fi