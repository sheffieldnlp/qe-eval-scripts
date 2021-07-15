# WMT'21 QE shared task

All information about the shared task is [here](https://www.statmt.org/wmt21/quality-estimation-task21.html).

### Scoring programs
All written in Python, use `requirements.txt` to install the required modules.
Then, 

for **Task 1**, use the following scripts:
* sentence-level DA:  `python sent_evaluate.py -h` 
* sentence-level DA **multilingual**:  `python sent-multi_evaluate.py -h` 

for **Task 2**, use the following scripts:
* sentence-level HTER:  `python sent_evaluate.py -h` 
* sentence-level HTER **multilingual**:  `python sent-multi_evaluate.py -h` 
* word-level HTER:  `python word_evaluate.py -h`

for **Task 3**, use the following script: 
* sentence-level Critical Error Detection**: `python sent_evaluate_CED.py -h`

Once you have checked that your system output on the dev data is correctly read by the right script, you can submit it using the CODALAB page corresponding to your subtask (see below).

### Submission platforms

Predictions should be submitted to a CODALAB page for each subtask:

Task 1, [sentence-level DA](https://competitions.codalab.org/competitions/33411)  
Task 1, [sentence-level DA **multilingual**](https://competitions.codalab.org/competitions/33411)

Task 2, [sentence-level HTER](https://competitions.codalab.org/competitions/33412)  
Task 2, [sentence-level HTER **multilingual**](https://competitions.codalab.org/competitions/33412)  
Task 2, [word-level HTER](https://competitions.codalab.org/competitions/33413)

Task 3, [sent-level Critical Error Detection](https://competitions.codalab.org/competitions/33414)  
