# Reading List
- [Connectionist Temporal Classification](http://www.machinelearning.org/proceedings/icml2006/047_Connectionist_Tempor.pdf)
- [Deep Speech](http://arxiv.org/pdf/1412.5567v2.pdf)
- [Reddit Rant](http://www.reddit.com/r/gadgets/comments/2m6anu/review_thalmic_labs_myo_armband_tldr_dont_buy/)

# Usage
## Collecting Data
From the project's root directory, invoke 

    python -m myoasl.collect data.txt

This will create a start a Tkinter application which collects data from a connected Myo Armband. To record a data point, press and hold a key, perform the sign, then release the key. EMG and IMU data will be recorded while the key is pressed and the time series will be written to the file **data.txt** along with a numerical represenation of the label.

## Evaluating models
Once you have a data file, you can run

    python evaluate-linear-models.py data.txt

to evaluate a broad range of linear classifiers. Results will be written to a log file in the current directory. The file lists all relevant parameters of the model and the final validation accuracy.

## Running Live Application
(TODO). 
