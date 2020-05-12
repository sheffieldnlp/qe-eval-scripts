# WMT'20 QE shared task

All information about the shared task is [here](http://www.statmt.org/wmt20/quality-estimation-task.html).

### Scoring programs
All written in Python, use `requirements.txt` to install the required modules.
Then, 

for **Task 1**, use the following scripts:
* sentence-level DA:  `python sent_evaluate.py -h` 
* sentence-level DA **multilingual**:  `python sent-multi_evaluate.py -h` 

for **Task 2**, use the following scripts:
* sentence-level HTER:  `python sent_evaluate.py -h` 
* word-level HTER:  `python word_evaluate.py -h`

for **Task 3**, use the following scripts[^1]:
* MQM **score**: `python eval_document_mqm.py -h`
* MQM **annotations**: `python eval_document_annotations.py -h`

Once you have checked that your system output on the dev data is correctly read by the right script, you can submit it using the CODALAB page corresponding to your subtask.

### Submission platforms

Predicitons should be submitted to a CODALAB page for each subtask:

Task 1,  [sentence-level DA](https://competitions.codalab.org/competitions/24447)
Task 1, [sentence-level DA **multilingual**](https://competitions.codalab.org/competitions/24447)

Task 2, [sentence-level HTER](https://competitions.codalab.org/competitions/24515)
Task 2, [word-level HTER](https://competitions.codalab.org/competitions/24728)

Task 3, [doc-level MQM **score**](https://competitions.codalab.org/competitions/24762)
Task 3, [doc-level **annotations**](https://competitions.codalab.org/competitions/24763)

[^1]:  under MT License (source: [Deep-Spin](https://github.com/deep-spin/qe-evaluation))

