import os
####################################################################################################
def hard(fname, s, freq,
         ba_pos=0.5,
         t=0,
         Ne=20000,
         n=200,
         theta=100,
         rho=50,
         window_size=50e3,
         run=True,
         num_floating_point = 10,
         rep=10
         ):
    msms = "java -Xmx20G -jar ../../assign_3/msms/lib/msms.jar"
    cmd = "%s -N %g -ms %g %s -t %s -r %s -SAA %s -SaA %s -SF %s %s -Sp %s>%s" % \
          (msms, Ne, n, rep, theta, rho, Ne * s, Ne * s / 2, t, freq, ba_pos, fname)
    print cmd
    if run:
        os.system(cmd)
    #     # print cmd
    # return read_msms_file_info(fname)

hard('hard.txt', s=0.05, freq=0.8)


####################################################################################################
def soft(fname, s, start_freq,
         ba_pos=0.5,
         t=0,
         Ne=10000,
         n=200,
         theta=50,
         rho=25,
         window_size=50e3,
         run=True,
         num_floating_point = 10
         ):
    msms = "java -jar /home/alek/msms/lib/msms.jar"
    cmd = "%s -N %g -ms %g 1 -t %s -r %s %i -SAA %s -SaA %s -SI %s 1 %s -Sp %s -oOC -Smark -oFP 0.%sE00 >%s" % \
          (msms, Ne, n, theta, rho, window_size, 2 * Ne * s, Ne * s, t, start_freq, ba_pos,"0"*num_floating_point, fname)
    # print cmd
    if run:
        os.system(cmd)
    return read_msms_file_info(fname)


####################################################################################################
def neutral(fname,
            Ne=10000,
            n=200,
            theta=50,
            rho=25,
            window_size=50e3,
            run=True,
            num_floating_point = 10,
            rep=10
            ):
    msms = "java -Xmx20G -jar ../../assign_3/msms/lib/msms.jar"
    # cmd = "%s -N %g -ms %g 1 -t %s -r %s %g -oFP 0.%sE00 >%s" % (msms, Ne, n, theta, rho, 999999, "0"*num_floating_point,fname)
    cmd = "%s -N %g -ms %g %d -t %s -r %s -oFP 0.%sE00 >%s" % (msms, Ne, n, rep, theta, rho, "0"*num_floating_point,fname)
    print cmd
    if run:
        os.system(cmd)
    # return read_msms_file_info(fname)

neutral('neutral.txt', Ne=20000, n=200, theta=100, rho=50)
####################################################################################################
