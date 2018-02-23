import os
import numpy as np
import matplotlib.pyplot as plt

def EAS_EUR_AFR(fname, rep, nsamp, seed, mode=0):

    N_A=7310.0
    N_AF=14474.0
    N_B=1861.0
    N_EU0=1032.0
    N_AS0=554.0



    Ne=N_A

    T_AF=148e3
    T_B=51e3
    T_EuAs=23e3

    m_AFB=15e-5
    m_AfAs=0.78e-5
    m_AfEu=2.5e-5
    m_EuAs=3.1e-5

    m12=m_AfEu*4*Ne
    m13=m_AfAs*4*Ne
    m23=m_EuAs*4*Ne
    m12_t1=m_AFB*4*Ne

    gen_age=25.0

    t1=T_EuAs/(gen_age*4.0*Ne)
    t2=T_B/(gen_age*4.0*Ne)
    t3=T_AF/(gen_age*4.0*Ne)
    if mode==0:
        ts = (np.random.rand()*0.16+0.25) * t1
        start_freq=0.001
        s=0.05
    else:
        ts=(0.1+0.8*np.random.rand(1))*(t2-t1)+t1
        start_freq=0.01
        s=0.005

    r_AS=0.48e-2
    r_EU=0.38e-2
    growth_AS=r_AS*4*Ne
    growth_EU=r_EU*4*Ne

    N2= N_EU0*np.exp(growth_EU*t1)
    N3= N_AS0*np.exp(growth_AS*t1)
    n=200
    Smu=0.0
    # rep=1

    ba_pos = np.round(np.random.rand(), 2)
    window_size=50e3
    theta=4*Ne*window_size*2.5e-8 # http://www.genetics.org/content/156/1/297.full.pdf
    rho=4*Ne*window_size*1.25e-8 # http://www.ncbi.nlm.nih.gov/pmc/articles/PMC383296/pdf/0140528.pdf

    if nsamp == 1:
        icmd = "-I 3 %g 0 0 0" %(n)
    elif nsamp == 2:
        icmd = "-I 3 0 %g 0 0" %(n)
    elif nsamp == 3:
        icmd = "-I 3 0 0 %g 0" %(n)
    elif nsamp == 123:
        n *= 3
        icmd = "-I 3 %g %g %g 0" %(n/3, n/3, n/3)


    msms="java -jar ./msms/lib/msms.jar"
    cmd="%s"%(msms) + " -N %g"%(Ne) +" -ms %g %g "%(n, rep) + icmd +" -t %.2f -r %.2f"%(theta,rho)
    cmd=cmd+" -g 2 %.2f -g 3 %.2f"%(growth_EU,growth_AS)+" -n 1 %.5f -n 2 %.5f -n 3 %.5f"%(N_AF/Ne,N2/Ne,N3/Ne)
    cmd=cmd+" -m 1 2 %.5f -m 2 1 %.5f"%(m12,m12)+" -m 1 3 %.5f -m 3 1 %.5f"%(m13,m13)+" -m 2 3 %.5f -m 3 2 %.5f"%(m23,m23)
    cmd=cmd+" -ej %.5f 3 2"%(t1)+" -en %.5f 2 %.5f"%(t1,N_B/Ne)+" -em %.5f 1 2 %.5f -em %.5f 2 1 %.5f"%(t1,m12_t1,t1,m12_t1)
    cmd=cmd+" -ej %.5f 2 1"%(t2)+" -en %.5f 1 1"%(t3)
    cmd=cmd+" -seed %d"%(seed)
    # cmd=cmd+" -SI %.5f 3 0 %.5f 0"%(ts,start_freq)+" -Sc 0 2 %.5f %.5f 0"%(2*Ne*s,Ne*s)+" -Smark -oOC"+" -Smu %.5f -Sp %s -oFP 0.0000000000E00 -SFC"%(Smu,ba_pos)
    cmd=cmd+" -oAFS onlySummary >%s"%(fname)#+" | grep -c '^O.*[1]$'"
    os.system(cmd)
    print(cmd)
    return fname, ts


samp1_fn = '3_1.txt'
samp2_fn = '3_2.txt'
samp3_fn = '3_3.txt'
samp4_fn = '4.txt'
rep = 100

print(EAS_EUR_AFR(samp1_fn, rep=rep, seed=1, nsamp=1))
print(EAS_EUR_AFR(samp2_fn, rep=rep, seed=1, nsamp=2))
print(EAS_EUR_AFR(samp3_fn, rep=rep, seed=1, nsamp=3))
print(EAS_EUR_AFR(samp4_fn, rep=rep, seed=1, nsamp=123))

with open(samp1_fn, 'r') as f:
    samp1 = np.array([int(x) for x in f.readlines()[-1][12:].split(' ')]) / rep

with open(samp2_fn, 'r') as f:
    samp2 = np.array([int(x) for x in f.readlines()[-1][12:].split(' ')]) / rep

with open(samp3_fn, 'r') as f:
    samp3 = np.array([int(x) for x in f.readlines()[-1][12:].split(' ')]) / rep

def draw_afs(samp, filename, name):
    rmax = 50
    rrange = range(1, rmax + 1)
    plt.bar(rrange, samp[:rmax], color='g')
    plt.title('AFS for ' + name)
    plt.savefig(filename, format='pdf')
    plt.close()


draw_afs(samp1, '3_1_AFS.pdf', name="AFR")
draw_afs(samp2, '3_2_AFS.pdf', name="EUR")
draw_afs(samp3, '3_3_AFS.pdf', name="EAS")
