DATA=raw_file
JSON=data.json

if [ -d $DATA ]; then
    echo "Raw data exist."
else
    echo "Raw data not exist."
    mkdir -p $DATA
    echo "Downloading raw data."
    for i in {74800..74807}; do
        wget https://www.bridgebase.com/tools/vugraph_linfetch.php?id=$i -O $DATA/$i.lin
    done
    echo "Downloading finish."
fi

if [ -f $JSON ]; then
    echo "Json data exist."
else
    echo "Json data not exist."
    touch $JSON
    echo "Begin convert lin file to json file."
    python ./lin2json.py
    echo "Successfully "
fi
