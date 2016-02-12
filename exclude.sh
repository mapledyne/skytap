#!/usr/bin/env bash
#
#

REPO=/Users/thewellington/Development/skytap-control
BRANCH='master'
RUNTYPE=$1
RUNTIME=$(date '+%Y-%m-%d %H:%M:%S')
EXCLUDESPATH="${REPO}/exclusions-final.conf"


function pull_repo {
    cd $REPO && git checkout $BRANCH && git pull
}

function exclude {
if [ "$RUNTYPE" == "evening" ]    # this is the evening run
then
    cat ${REPO}/permanent-exclusions.conf > ${EXCLUDESPATH}
    cat ${REPO}/daily-exclusions.conf >> ${EXCLUDESPATH}
    cat ${REPO}/evening-exclusions.conf >> ${EXCLUDESPATH}

elif [ "$RUNTYPE" == "daily" ]      # full midnight run
then
    cat ${REPO}/permanent-exclusions.conf > ${EXCLUDESPATH}
    cat ${REPO}/daily-exclusions.conf >> ${EXCLUDESPATH}

else
    echo "we need an argument"

fi
}

function push_repo {
    cd $REPO && git checkout $BRANCH && git add . && git commit -m "nightly cleanup" && git push
}

# making it happen

if [ "$RUNTYPE" == "cleanup" ]    # cleanup run?
then
    echo "# This file lists the Skytap Configuration IDs that should be excluded from
# blanket Skynet suspend commands,

# Configurations noted here will be excluded from the evening run only.
# The result will be a configuration that will run past 7:00 PM but be suspended at midnight.

# This file is purged automatically after the midnight run.

# Last purged: ${RUNTIME}

#### Begin Evening Exclusions ##############################################
# CONFIG ID # CONFIG NAME           # WHO           # WHY


#### End Evening Exclusions ################################################

" > ${REPO}/evening-exclusions.conf

    echo "# This file lists the Skytap Configuration IDs that should be excluded from
# blanket Skynet suspend commands,

# Configurations noted here will be excluded from the evening run and from the midnight run.
# The result will be a configuration that will run all night long.

# This file is purged after the midnight run.

# Last purged: ${RUNTIME}

#### Begin Daily Exclusions ##############################################
# CONFIG ID # CONFIG NAME           # WHO           # WHY


#### End Daily Exclusions ################################################

" > ${REPO}/daily-exclusions.conf

push_repo

else
    pull_repo
    exclude
fi
