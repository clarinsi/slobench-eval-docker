Build docker image:
    docker build -t eval-image .

Run scripts:
    % in practive rm parameter will be probably removed ??
    docker run -it --rm --name eval-container -v "$PWD/eval-script-NER.py":/scripts/eval_script.py -v "$PWD/input-files":/input-files eval-image python ./runner-script.py param1 param2
    