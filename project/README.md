`real_sorted_labels.txt` -- is prepared ground truth to run a script

Admixture output got from @seryrzu (ran on chihua, located in `/home/abzikadze/phd/cse280a`)
Structure output got from @andreabc (https://drive.google.com/file/d/1gYPq-VA-hufojm2bEDhg1VHgDf83xTv6/view?usp=sharing), filtered that now contains only 1092 individuals from original Phase1 VCF from 1000genomes.


Command lines to plot confustion matrices (and other benchmarking that will possibly be added soon)

```
python benchmark.py -i admixture_output/chr22_phase1.14.Q -a real_sorted_labels.txt -o admixture_output --tool-name Admixture
```

```
python benchmark.py -i structure_output/chr22_phase1.14.Q -a real_sorted_labels.txt -o structure_output --tool-name Structure
```
