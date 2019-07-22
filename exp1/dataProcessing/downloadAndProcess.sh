scp -P 18765 davebrau@ns1.us69.siteground.us:~/public_html/turk/data/dissertation/dissertationExperiment1/*.txt ./txtData/pilot/real/
./dataProcessing.py txtData/pilot/**/*.txt
Rscript --vanilla /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/analysis/exp1/scripts/preprocessing/knitAnalysis.r
firefox /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/analysis/exp1/scripts/preprocessing/index.html